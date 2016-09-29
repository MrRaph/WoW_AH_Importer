import json
import datetime
from nameko.timer import timer
from nameko.rpc import rpc, RpcProxy
from datetime import datetime
import settings

from mongoengine import connect

## Debug imports
import pprint

from models import AuctionImports, AuctionData

CONFIG = {'AMQP_URI': settings.ampq_uri}

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

        bulk = AuctionData._get_collection().initialize_ordered_bulk_op()

        print(datetime.now())

        for auction in auctions:  # where users is a list of dicts containing data to work on
            bulk.find({ "auc": auction['auc'] }).upsert().replace_one(auction)

        result = bulk.execute()

        print(datetime.now())
