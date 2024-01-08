from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.bytedance import TDDL
from ext.util import send_videos, send_photos, get_share_links
from ext.upload import upload
from ext.var import sv, rv
import logging

def tiktokuserlink(c, m, url, caption):
  original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",
                                                         url=url)]])
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
  if list_photo:
    try:
      send_photos(m, list_photo, original, caption)
    except Exception as e:
      logging.error(e)
  if list_video:
    try:
      send_videos(m, list_video, original, caption)
    except:
      send_videos(m, list_file, original, caption)
  
def tikdou(c, m, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  try:
    file, link, is_video = TDDL(url)
  except:
    tiktokuserlink(c, m, url, caption)
    return
  if is_video == False:
    send_photos(m, link, original, caption)
  elif is_video == True:
    m.reply_chat_action(sv)
    try:
      sf = m.reply_video(link, caption=caption, reply_markup=original)
    except:
      sf = m.reply_video(file, caption=caption, reply_markup=original)
    original = getattrs(m, sf) 
    sf.edit_reply_markup(original)
    if m.chat.username == "contentdownload":
      upload(file)