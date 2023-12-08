from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Youtube import YTDL
from utils.functions import save
from utils.variables import rv, sv
import re, os, logging, time


@Client.on_message(filters.regex(r"youtube.com|youtu.be"))
def handle_youtube(c, m):
  save(m)
  m.reply_chat_action(rv)
  text = m.text
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original",
                                                         url=url)]])
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  download = m.reply("**Downloading**`...`", quote=True)
  file = YTDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_video(file, reply_markup=original, caption=caption)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except Exception as e:
    delog = m.reply(e)
    time.sleep(5)
    c.delete_messages(m.chat.id, delog.id)
