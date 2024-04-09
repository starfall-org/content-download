from hydrogram import Client, filters
from ext import server_info
from hydrogram.enums import ChatAction
import platform

@Client.on_message(filters.command('server'))
def bot_server_info(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    ver = platform.version()
    name = platform.uname()
    system = platform.system()
    server = server_info()
    msg_text = (f"```{system}\n"
              f"INFO:\n{name}\n\n"
              f"VERSION:\n{ver}\n\n"
              f"SERVER:\n{server}\n"
              "```")
    m.reply(msg_text)
