import os
from deta import Deta

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
deta = Deta(os.getenv('DETA_KEY'))
upload_app = os.getenv("UPLOAD_APP")
api_url = os.getenv("API_URL")
