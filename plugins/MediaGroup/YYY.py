from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Other import DL
from utils.etc import save
from utils.var import t, sv, sp, sm
import re


@Client.on_message((filters.regex(r"https?://(\S+\.)?") or filters.command("download"))& filters.incoming)
def handle_other(c, m):
  text = m.text
  if text.startswith('/request'):
    return
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  file, type = DL(url)
  if file is None:
    return
  download = m.reply("**Downloading**`...`", quote=True)
  save(m)
  m.reply_chat_action(t)
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original",
                                                         url=url)]])
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  if type == "image":
    m.reply_chat_action(sp)
    m.reply_photo(file, reply_markup=original, caption=caption)
  elif type == "video":
    m.reply_chat_action(sv)
    m.reply_video(file, reply_markup=original, caption=caption)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  else:
    m.reply_chat_action(sv)
    m.reply_video(file, reply_markup=original, caption=caption)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass