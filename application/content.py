from hydrogram import Client, idle
from data import Token
import os

class Content(Client):
    def __init__(self):
        self.client = Client("Content Download",
        api_id=Token().id,
        api_hash=Token().hash,
        bot_token=Token().token,
        plugins=dict(root="activity"),
        max_concurrent_transmissions=100)
    def run(self):
        self.client.start()
        os.system("echo Content Download")
        idle()