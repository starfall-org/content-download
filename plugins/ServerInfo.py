from pyrogram import Client, filters
from utils.functions import server_info
import platform, psutil

@Client.on_message(filters.command('info'))
def bot_server_info(c, m):
  ver = platform.version()
  name = platform.uname()
  system = platform.system()
  serverinfo = server_info()

  reply_text = (f'**SERVER:** \n`{serverinfo}`\n\n'
                f'**INFO:** \n`{name}`\n\n'
                f'**VERSION:** \n`{ver}`\n\n**OS:** `{system}`')

  m.reply(reply_text)
