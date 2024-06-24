import os
import requests

res = requests.get(os.getenv("SECRET"), timeout=99).json()

DAPI = res["api"]["dapi"]
DATABASE_URL = res["postgres"]["cockroach"]
bot_token = res["bot"]["contentdownload"]
