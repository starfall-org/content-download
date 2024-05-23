import os
from hydrogram import Client, idle
from data.environment import api_id, api_hash, bot_token


class Content(Client):
    def __init__(self):
        self.client = Client(
            "Content Download",
            api_id,
            api_hash,
            bot_token=bot_token,
            plugins=dict(root="plugins"),
            max_concurrent_transmissions=100,
        )

    def run(self):
        self.client.start()
        os.system("echo Content Download")
        idle()
