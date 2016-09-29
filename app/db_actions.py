import json
import datetime
from nameko.timer import timer
from nameko.rpc import rpc, RpcProxy
from datetime import datetime
import settings

from mongoengine import connect

## Debug imports
import pprint

# from .models import AuctionImports, DeclarativeBase
from models import AuctionImports, AuctionData

CONFIG = {'AMQP_URI': settings.ampq_uri}
# DeclarativeBase = declarative_base(cls=Base)
global connection
connect(host=settings.database_url, alias='default')

class dbActions(object):
    name = "dbActions"

    db_session = None

    @rpc
    def get_db_connection(self):
        db_session = connect('ah', settings.database_url)
        connection = db_session

    @rpc
    def insert_auction_set(self, url, lastModified, realm, auctions):

        # records = self.db_session.query(models.AuctionImports).filter_by(lastModified=lastModified).count()
        records = AuctionImports.objects(url=url, lastModified=lastModified, realm=realm)

        if len(records) == 0:
            import_date = datetime.now
            auction_import = AuctionImports(
                url = url,
                lastModified = lastModified,
                created = import_date,
                realm = realm
            )
            auction_import.save()
        else:
            print('Record already exists !')
            auction_import = records
            # return -1

        bulk = AuctionData._get_collection().initialize_ordered_bulk_op()

        # auction_clean = []

        # for auction in auctions:
        #     auction['import_ref'] = auction_import[0]
        #     auction_clean.append(auction)
        #     print (auction_import[0]._id)
        #     break
        datetime.now()

        for auction in auctions:  # where users is a list of dicts containing data to work on
            # auction['import_ref'] = AuctionImports(auction_import[0])
            # bulk.find({ "auc": auction['auc'], "import_ref": auction_import }).upsert().replace_one(auction)
            bulk.find({ "auc": auction['auc'] }).upsert().replace_one(auction)
            # print(auction)
            # break

        result = bulk.execute()

        datetime.now()
        # print(result)
