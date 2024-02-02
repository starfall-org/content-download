from types import SimpleNamespace
from deta import Deta
import psycopg2, requests
import json, os

def res():
    secret = requests.get(os.getenv("SECRET")).text
    return json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))

deta = Deta(res().key.web_collection)
pg = psycopg2.connect(res().data.cr_pg)

class Token:
    id = res().key.api_id
    hash = res().key.api_hash
    token = res().bot.cd_tg