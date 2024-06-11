import json
import os
from types import SimpleNamespace
import requests

secret = requests.get(os.getenv("SECRET"), timeout=99).text
res = json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))

WEB_COLLECTION = ""
DAPI = res.api.dapi
COLLECTON = ""
DATABASE_URL = res.database.contentdownload
bot_token = res.bot.contentdownload
