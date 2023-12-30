from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from api_callback.ByteDance import TDDL
from etc.util import send_videos, send_photos, uploads, get_share_links
from etc.var import sv, rv
import logging

def tiktokuserlink(c, m, url, caption, s):
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
  s.edit("**Sending**`...`")
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
  s.delete()
  
def tikdou(c, m, s, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  try:
    file, link, is_video = TDDL(url)
  except:
    tiktokuserlink(c, m, url, caption, download)
    return
  s.edit("**Sending**`...`")
  if is_video == False:
    send_photos(m, c, original, file, caption)
    s.delete()
  elif is_video == True:
    m.reply_chat_action(sv)
    try:
      s.edit_media(InputMediaVideo(link))
      s.edit_caption(caption=caption, reply_markup=original)
    except:
      s.edit_media(InputMediaVideo(file.getvalue()))
      s.edit_caption(caption=caption, reply_markup=original)
    original = getattrs(m, s) 
    s.edit_reply_markup(original)
    if s.chat.username == "contentdownload":
      uploads(file)