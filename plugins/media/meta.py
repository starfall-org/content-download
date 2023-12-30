from pyrogram.types import InputMediaVideo
from api_callback.Meta import FBDL, IGDL
from etc.util import send_videos, send_photos
from etc.var import rv, sv

def facebook(c, m, stt, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files = FBDL(url)
  m.reply_chat_action(sv)
  stt.edit("**Sending**`...`")
  m.reply_chat_action(sv)
  if not isinstance(files, list):
    sf = m.reply_video(files, caption=caption, reply_markup=original)
  else:
    for file in files:
      sf = m.reply_video(file, caption=caption, reply_markup=original)
  original = getattrs(m, sf)
  sf.edit_reply_markup(original)
  #send_videos(m, files, original, caption)

def instagram(c, m, stt, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files, video = IGDL(url)
  stt.edit("**Sending**`...`")
  if video == False:
    send_photos(m, files, original, caption)
  elif video == True:
    send_videos(m, files, original, caption)