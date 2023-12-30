from pyrogram.types import InputMediaVideo
from api_callback.Meta import FBDL, IGDL
from etc.util import send_videos, send_photos
from etc.var import rv, sv

def facebook(c, m, s, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files = FBDL(url)
  m.reply_chat_action(sv)
  s.edit("**Sending**`...`")
  m.reply_chat_action(sv)
  if not isinstance(files, list):
    st = m.reply_video(files, caption=caption, reply_markup=original)
  else:
    for file in files:
      st = m.reply_video(file, caption=caption, reply_markup=original)
  original = getattrs(m, st)
  st.edit_reply_markup(original)
  #send_videos(m, c, original, files, caption)

def instagram(c, m, s, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files, video = IGDL(url)
  s.edit("**Sending**`...`")
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    send_videos(m, c, original, files, caption)