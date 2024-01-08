from pyrogram import Client, filters
from ext.util import server_info
import platform

@Client.on_message(filters.command('server'))
def bot_server_info(c, m):
  ver = platform.version()
  name = platform.uname()
  system = platform.system()
  serverinfo = server_info()

  reply_text = (f'**INFO:** \n`{name}`\n\n'
                f'**VERSION:** \n`{ver}`\n**OS:** `{system}`\n\n'
                f'**HOSTING:** \n`{serverinfo}`\n\n')

  m.reply(reply_text)
