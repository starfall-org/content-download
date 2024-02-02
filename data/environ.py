from types import SimpleNamespace
from deta import Deta
import psycopg2, requests
import json, os

secret = requests.get(os.getenv("SECRET")).text
res = json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))

conn = psycopg2.connect(res.data.cr_pg)
cursor = conn.cursor()

class Token:
    id = res.key.api_id
    hash = res.key.api_hash
    token = res.bot.cd_tg