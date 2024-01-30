from pymongo import MongoClient
from deta import Deta
import os

dapi = os.getenv("DAPI")
collection = os.getenv("COLLECTION")
mongo = MongoClient(os.getenv("MONGO_URL"))
deta = Deta(os.getenv("DETA_KEY"))

class Token:
    def __init__(self):
        db = mongo["tokens"]
        api = db.find_one("api")
        bot = db.find_one("bot")
        self.id = api["id"]
        self.hash = api["hash"]
        self.cd = bot["cd"]