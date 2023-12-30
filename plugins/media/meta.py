from api_callback.Meta import FBDL, IGDL
from etc.util import send_videos, send_photos
from etc.var import rv, sv

def facebook(c, m, status, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files = FBDL(url)
  m.reply_chat_action(sv)
  status.edit("**Sending**`...`")
  m.reply_chat_action(sv)
  if not isinstance(files, list):
    s = m.reply_video(files, reply_markup=original, caption=caption)
  else:
    for file in files:
      s = m.reply_video(file, reply_markup=original, caption=caption)
  original = getattrs(m, s)
  s.edit_reply_markup(original)
  #send_videos(m, c, original, files, caption)
  status.delete()

def instagram(c, m, status, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files, video = IGDL(url)
  status.edit("**Sending**`...`")
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    send_videos(m, c, original, files, caption)
  status.delete()