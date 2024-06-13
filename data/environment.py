import os
import requests

res = requests.get(os.getenv("SECRET"), timeout=99).text

DAPI = res["api"]["dapi"]
DATABASE_URL = res["database"]["contentdownload"]
bot_token = res["bot"]["contentdownload"]
