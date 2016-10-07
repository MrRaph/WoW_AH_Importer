import yagmail
import json
import requests
import datetime
from nameko.timer import timer
from nameko.rpc import rpc, RpcProxy
import settings
import urllib.request
from datetime import datetime
import os

import pprint

# CONFIG = {'AMQP_URI': settings.ampq_uri}

# CONFIG = {'AMQP_URI': os.environ['AMQP_URI']}

class ahActions(object):
    name = "ahActions"

    dbAction = RpcProxy('dbActions')
    ahAction = RpcProxy('ahActions')

    @rpc
    #@timer(interval=1800)
    def get_ah_auction_file(self):
        url = 'https://'+ settings.region +'.api.battle.net/wow/auction/data/'+ settings.realm +'?locale='+ settings.locale +'&apikey=' + settings.apiKey

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
        }

        r = requests.get(url, headers=headers)

        global req
        req = json.loads(r.text)['files'][0]

        with urllib.request.urlopen(req['url']) as data:
            s = data.read().decode('utf-8')

            print(datetime.now())

            auctions = json.loads(str(s))['auctions']
            chunkSize = 5000
            for i in range(0, len(auctions), chunkSize):
                import_id = self.dbAction.insert_auction_import(
                    req['url'],
                    req['lastModified'],
                    settings.realm
                )

                self.dbAction.insert_auction_set.call_async(
                    req['url'],
                    req['lastModified'],
                    settings.realm,
                    import_id,
                    auctions[i:i+chunkSize]
                )

            print(datetime.now())
