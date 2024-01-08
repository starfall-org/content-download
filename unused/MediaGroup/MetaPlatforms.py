from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Meta import FBDL, IGDL
from etc.util import save, send_videos, send_photos
from etc.var import rv, sv
import re


@Client.on_message(filters.regex(r"facebook.com|fb.watch|fb.gg"))
def handle_facebook(c, m):
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
  files = FBDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  send_videos(m, c, original, files, caption)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass


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
  download = m.reply("**Downloading**`...`", quote=True)
  files, video = IGDL(url)
  c.delete_messages(m.chat.id, download.id)
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    sending = m.reply("**Sending**`...`", quote=True)
    send_videos(m, c, original, files, caption)
    c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass