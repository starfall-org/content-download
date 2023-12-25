from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.ByteDance import TDDL
from etc.util import send_videos, send_photos, uploads, get_share_links
from etc.var import sv, rv
import re, logging

def tiktokuserlink(c, m, url, caption, download):
  original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",
                                                         url=url)]])
  m.reply_chat_action(rv)
  share_links = get_share_links(url)
  list_video = []
  list_file = []
  list_photo = []
  for sharelink in share_links:
    file, link, is_video = TDDL(sharelink)
    if is_video == True:
      list_video.append(link)
      list_file.append(file)
    else:
      list_photo.extend(link)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  if list_photo:
    try:
      send_photos(m, c, original, list_photo, caption)
    except Exception as e:
      logging.error(e)
  if list_video:
    try:
      send_videos(m, c, original, list_video, caption)
    except:
      send_videos(m, c, original, list_file, caption)
  c.delete_messages(m.chat.id, sending.id)
  
def tikdou(c, m, url, original, caption, download):
  m.reply_chat_action(rv)
  try:
    file, link, is_video = TDDL(url)
  except:
    tiktokuserlink(c, m, url, caption, download)
    return
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  if is_video == False:
    send_photos(m, c, original, file, caption)
  elif is_video == True:
    m.reply_chat_action(sv)
    try:
      m.reply_video(link, reply_markup=original, caption=caption)
    except:
      m.reply_video(file, reply_markup=original, caption=caption)
    if m.chat.username == "contentdownload":
      uploads(file)
  c.delete_messages(m.chat.id, sending.id)