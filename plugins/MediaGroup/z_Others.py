from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Other import DL
from utils.functions import save
from utils.variables import t, rv, sv, sp, sm, sd, dl_ani, up_ani
import re, os, logging, time


@Client.on_message(filters.regex(r"https?://(\S+\.)?") & filters.incoming)
def handle_other(c, m):
  text = m.text
  if text.startswith('/request'):
    return
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  file, type = DL(url)
  if file is None:
    return
  dw = m.reply_animation(dl_ani, quote=True)
  save(m)
  m.reply_chat_action(rv)
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original",
                                                         url=url)]])
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  c.delete_messages(m.chat.id, dw.id)
  if type == "image":
    m.reply_chat_action(sp)
    m.reply_photo(file, reply_markup=original, caption=caption)
  elif type == "video":
    uw = m.reply_animation(up_ani, quote=True)
    m.reply_chat_action(sv)
    m.reply_video(file, reply_markup=original, caption=caption)
    c.delete_messages(m.chat.id, uw.id)
  elif type == "audio":
    uw = m.reply_animation(up_ani, quote=True)
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
    c.delete_messages(m.chat.id, uw.id)
  else:
    pass
  try:
    m.delete()
  except Exception as e:
    delog = m.reply(e)
    time.sleep(5)
    c.delete_messages(m.chat.id, delog.id)
