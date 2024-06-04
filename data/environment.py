import json
import os
from types import SimpleNamespace
import requests

secret = requests.get(os.getenv("SECRET"), timeout=99).text
res = json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))

WEB_COLLECTION = res.deta.web_collection
DAPI = res.api.dapi
COLLECTON = res.api.collection
DATABASE_URL = res.postgres.cockroach
bot_token = res.bot.contentdownload
