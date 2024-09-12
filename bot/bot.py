import pyrogram


class Content(pyrogram.Client):
    def __init__(self):
        self.bot_token = None
        super().__init__(
            "Content Download",
            6,
            "eb06d4abfb49dc3eeb1aeb98ae0f581e",
            bot_token=self.bot_token,
            plugins={"root": "plugins"},
            max_concurrent_transmissions=100,
        )

    def add_token(self, token: str):
        self.bot_token = token
