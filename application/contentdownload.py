from db.secret import tokens
import pyrogram, os

app = pyrogram.Client("Content Download",
                      api_id=tokens()[0],
                      api_hash=tokens()[1],
                      bot_token=tokens()[2],
                      plugins={"root": "plugins"},
                      max_concurrent_transmissions=100)


def runserver():
  app.start()
  os.system("echo Content Download")
  pyrogram.idle()
