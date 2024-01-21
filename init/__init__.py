from deta import Deta
import os

dapi = os.getenv("DAPI")
collection = os.getenv("COLLECTION")
deta = Deta(os.getenv("DETA_KEY"))

class Token:
    def __init__(self):
        db = deta.Base("tokens")
        self.id = db.get("api")["id"]
        self.hash = db.get("api")["hash"]
        self.cd = db.get("bot")["cd"]