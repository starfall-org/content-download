from pyrogram import filters, Client
from utils.functions import save
from utils.variables import button
from utils.variables import t
from utils.basic_text import start_vn, start_en, help_vn, help_en


@Client.on_message(filters.command("start") & filters.private)
def handle_start(c, m):
  save(m)
  m.reply_chat_action(t)
  lan = m.from_user.language_code
  if lan == "vi":
    msg = start_vn
  else:
    msg = start_en
  m.reply(msg, reply_markup=button)


@Client.on_message(filters.command('help') & (filters.private | filters.mentioned))
def handle_help(c, m):
  save(m)
  m.reply_chat_action(t)
  lan = m.from_user.language_code
  if lan == "vi":
    msg = help_vn
  else:
    msg = help_en
  m.reply(msg, reply_markup=button)
