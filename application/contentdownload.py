from utils.secret import api_id, api_hash, bot_token
from utils.variables import proxy
import pyrogram, os

app = pyrogram.Client("Content-Download",
                      api_id,
                      api_hash,
                      bot_token=bot_token,
                      plugins={"root":"plugins"},
                      max_concurrent_transmissions=100)


def runserver():
  app.start()
  os.system("echo Content Download")
  pyrogram.idle()
