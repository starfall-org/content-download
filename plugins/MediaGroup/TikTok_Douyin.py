from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.TikTok_Douyin import TDDL
from utils.functions import save, send_photos, uploads
from utils.variables import sv, rv
import re, os, logging, time


@Client.on_message(filters.regex(r"douyin.com|tiktok.com|iesdouyin.com"))
def handle_tiktokdouyin(c, m):
  save(m)
  text = m.text
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original",
                                                         url=url)]])
  m.reply_chat_action(rv)
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  download = m.reply("**Downloading**`...`", quote=True)
  file, link, is_video = TDDL(url)
  c.delete_messages(m.chat.id, download.id)
  if is_video == False:
    send_photos(m, c, original, file, caption)
  elif is_video == True:
    sending = m.reply("**Sending**`...`", quote=True)
    m.reply_chat_action(sv)
    try:
      m.reply_video(link, reply_markup=original, caption=caption)
    except:
      m.reply_video(file, reply_markup=original, caption=caption)
    c.delete_messages(m.chat.id, sending.id)
    if m.chat.username == "contentdownload":
      uploads(file)
  try:
    m.delete()
  except:
    pass