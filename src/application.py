import os
import uvloop
from pyrogram import Client, idle
from environment import bot_token


class Content(Client):
    def __init__(self):
        self.client = Client(
            "Content Download",
            21021245,
            "7b32ea92719781c5e22ede319c5dbde5",
            bot_token=bot_token,
            plugins={"root": "plugins"},
            max_concurrent_transmissions=100,
        )

    def run(self):
        self.client.start()
        os.system("echo Content Download")
        idle()


if __name__ == "__main__":
    uvloop.install()
    app = Content()
    app.run()
