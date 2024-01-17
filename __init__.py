import os
from deta import Deta

dapi = os.getenv("DAPI")
webstream = os.getenv("WEBSTREAM")
collection = os.getenv("COLLECTION")
detaspace = Deta(os.getenv('DETA_KEY'))

class Token:
    def __init__(self):
        db = deta.Base('telegram-sessions')
        self.id = db.get('API_ID')["value"]
        self.hash = db.get('API_HASH')["value"]
        self.cd = db.get('CD_TOKEN')["value"]