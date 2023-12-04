from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Instagram import IGDL
from utils.functions import save, send_photos, send_videos
from utils.variables import rv, dl_ani, up_ani
import re, os, logging


@Client.on_message(filters.regex(r"instagram.com"))
def handle_instagram(c, m):
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
  dw = m.reply_animation(dl_ani, quote=True)
  files, video = IGDL(url)
  c.delete_messages(m.chat.id, dw.id)
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    uw = m.reply_animation(up_ani, quote=True)
    send_videos(m, c, original, files, caption)
    c.delete_messages(m.chat.id, uw.id)
  try:
    m.delete()
  except Exception as e:
    logging.critical(e)
