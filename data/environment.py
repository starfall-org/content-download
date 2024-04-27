import json
import os
from types import SimpleNamespace

import psycopg2
import requests
from deta import Deta


def res():
    secret = requests.get(os.getenv("SECRET")).text
    return json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))


res = res()
dapi = res.api.dapi
collection = res.api.collection
deta = Deta(res.key.web_collection)


def pg():
    conn = psycopg2.connect(res.data.cockroach)
    return conn, conn.cursor()


class Token:
    id = res.key.api_id
    hash = res.key.api_hash
    token = res.bot.cd_tg
