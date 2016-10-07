from mongoengine import *
from datetime import datetime

import settings

class AuctionImports(Document):
    id = SequenceField(required=True, primary_key=True)
    url = URLField()
    realm = StringField(max_length=250)
    created = DateTimeField(default=datetime.now)
    lastModified = IntField()

class AuctionData(Document):
    auc = IntField(required=True, primary_key=True)
    item = IntField()
    owner = StringField(max_length=250)
    ownerRealm = StringField(max_length=250)
    bid = IntField()
    buyout = IntField()
    quantity = IntField()
    timeLeft = StringField(max_length=50)
    rand = IntField()
    seed = IntField()
    context = IntField()
    import_ref = ReferenceField(AuctionImports)
