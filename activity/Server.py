from pyrogram import Client, filters
from ext.util import server_info
import platform

@Client.on_message(filters.command('server'))
def bot_server_info(c, m):
  ver = platform.version()
  name = platform.uname()
  system = platform.system()
  server = server_info()
  reply_text = (f'```{system}'
                f'INFO:\n{name}\n'
                f'VERSION:\n{ver}\n'
                f'SERVER:\n{server}\'
                '```'
                )

  m.reply(reply_text)
