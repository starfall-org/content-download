from utils.db import session_string
import pyrogram, os

app = pyrogram.Client("Content Download", session_string=session_string
                      
                      ,plugins={"root":"plugins"},
                      max_concurrent_transmissions=100)


def runserver():
  app.start()
  os.system("echo Content Download")
  pyrogram.idle()
