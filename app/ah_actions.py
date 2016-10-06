import yagmail
import json
import requests
import datetime
from nameko.timer import timer
from nameko.rpc import rpc, RpcProxy
import settings
import urllib.request
from datetime import datetime

import pprint

# CONFIG = {'AMQP_URI': settings.ampq_uri}

class ahActions(object):
    name = "ahActions"

    dbAction = RpcProxy('dbActions')
    ahAction = RpcProxy('ahActions')

    @rpc
    @timer(interval=1800)
    def get_ah_auction_file(self):
        url = 'https://'+ settings.region +'.api.battle.net/wow/auction/data/'+ settings.realm +'?locale='+ settings.locale +'&apikey=' + settings.apiKey

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
        }

        r = requests.get(url, headers=headers)

        with urllib.request.urlopen(json.loads(r.text)['files'][0]['url']) as data:
            s = data.read().decode('utf-8')

            print(datetime.now())

            auctions = json.loads(str(s))['auctions']
            chunkSize = 5000
            for i in range(0, len(auctions), chunkSize):
                self.dbAction.insert_auction_set.async(
                    json.loads(r.text)['files'][0]['url'],
                    json.loads(r.text)['files'][0]['lastModified'],
                    settings.realm,
                    auctions[i:i+chunkSize]
                )

            print(datetime.now())

    #
    # @rpc
    # def get_auctions(self, url, import_id):
    #     with urllib.request.urlopen(url) as data:
    #         s = data.read().decode('utf-8')
    #
    #     counter = 0
    #     for auction in json.loads(str(s))['auctions']:
    #         self.dbAction.insert_auction_data.async(
    #             auction, import_id
    #         )
    #         if counter < 1000:
    #             counter = counter + 1
    #         else:
    #             counter = 0
    #             self.dbAction.flush_and_commit()
