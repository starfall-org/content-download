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
        api = db.find_one({"_id":"api"})
        bot = db.find_one({"_id":"bot"})
        self.id = api["id"]
        self.hash = api["hash"]
        self.cd = bot["cd"]