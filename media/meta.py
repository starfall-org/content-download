from pyrogram.types import InputMediaVideo
from api import FBDL, IGDL
from ext.util import send_videos, send_photos
from ext.var import rv, sv

def facebook(c, m, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files = FBDL(url)
  m.reply_chat_action(sv)
  if not isinstance(files, list):
    st = m.reply_video(files, caption=caption, reply_markup=original)
  else:
    for file in files:
      st = m.reply_video(file, caption=caption, reply_markup=original)
  original = getattrs(m, st)
  st.edit_reply_markup(original)

def instagram(c, m, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files, video = IGDL(url)
  if video == False:
    send_photos(m, files, original, caption)
  elif video == True:
    send_videos(m, files, original, caption)