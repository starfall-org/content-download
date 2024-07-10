import os
import requests

res = requests.get(os.getenv("SECRET"), timeout=99).json()

dapi = res["api"]["dapi"]
DATABASE_URL = res["postgres"]["cockroach"]
bot_token = res["bot"]["contentdownload"]
DAPI_YT = dapi['yt']
DAPI_YTM = dapi['ytm']
DAPI_FB = dapi['fb']
DAPI_IG = dapi['ig']
DAPI_TD = dapi['td']
