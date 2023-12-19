import os
from deta import Deta

upload_app = os.getenv("UPLOAD_APP")
api_url = os.getenv("API_URL")
deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base('telegram-sessions')

def tokens():
  api_id = db.get('API_ID')
  api_hash = db.get('API_HASH')
  bot_token = db.get('CD_TOKEN')
  return api_id['value'], api_hash['value'], bot_token['value']