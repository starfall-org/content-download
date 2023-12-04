from pyrogram import Client, filters
from utils.functions import server_info
import platform, psutil

@Client.on_message(filters.command('info'))
def bot_server_info(c, m):
  arch = platform.machine()
  ver = platform.version()
  name = platform.uname()
  system = platform.system()
  cpu_usage = psutil.cpu_percent()
  ram_info = psutil.virtual_memory()
  serverinfo = server_info()

  reply_text = (f'**SERVER:** \n`{serverinfo}`\n\n'
                f'**RAM:** \n`{ram_info}`\n\n**CPU:** \n`{cpu_usage}`\n\n'
                f'**INFO:** \n`{name}`\n\n**ARCHITECTURE:** \n`{arch}`\n\n'
                f'**VERSION:** \n`{ver}`\n**OS:** `{system}`')

  m.reply(reply_text)
