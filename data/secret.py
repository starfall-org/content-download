import os
from deta import Deta

DAPI = os.getenv("DAPI")
webstream = os.getenv("WEBSTREAM")
collection = os.getenv("COLLECTION")
deta = Deta(os.getenv('DETA_KEY'))

def tokens():
    db = deta.Base('telegram-sessions')
    api_id = db.get('API_ID')
    api_hash = db.get('API_HASH')
    bot_token = db.get('CD_TOKEN')
    return api_id['value'], api_hash['value'], bot_token['value']