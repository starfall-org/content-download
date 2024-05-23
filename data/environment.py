import json
import os
from types import SimpleNamespace
import requests

secret = requests.get(os.getenv("SECRET")).text
res = json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))

WEB_COLLECTION = res.key.web_collection
DAPI = res.api.dapi
COLLECTON = res.api.collection
DATABASE_URL = res.data.cockroach


api_id = res.key.api_id
api_hash = res.key.api_hash
bot_token = res.bot.cd_tg
