from pymongo import MongoClient
from deta import Deta
import os

dapi = os.getenv("DAPI")
collection = os.getenv("COLLECTION")
mongo = MongoClient(os.getenv("MONGO_URL"))["mo9973_dash"]
deta = Deta(os.getenv("DETA_KEY"))

class Token:
    @staticmethod
    def initial():
        db = mongo["tokens"]
        api = db.find_one({"_id": "api"})
        bot = db.find_one({"_id": "bot"})
        return api["id"], api["hash"], bot["cd"]
    id, hash, token = staticmethod(initial())()