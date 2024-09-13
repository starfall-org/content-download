import pyrogram
from bot import Content
from config import keys


app = Content()
app.add_token(keys.bot_token)

if __name__ == "__main__":
    app.start()
    print("Content Download")
    pyrogram.idle()
    app.stop()
