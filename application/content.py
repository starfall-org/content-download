from data.secret import tokens
from pyrogram import Client, idle
import os

class Content(Client):
    def __init__(self):
        self.client = Client("Content Download",
        api_id=tokens()[0],
        api_hash=tokens()[1],
        bot_token=tokens()[2],
        plugins=dict(root="activity"),
        max_concurrent_transmissions=100)
    def run(self):
        self.client.start()
        os.system("echo Content Download")
        idle()