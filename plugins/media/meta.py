from api_callback.Meta import FBDL, IGDL
from etc.util import send_videos, send_photos
from etc.var import rv, sv

def facebook(c, m, download, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files = FBDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_chat_action(sv)
  if not isinstance(files, list):
    s = m.reply_video(files, reply_markup=original, caption=caption)
  else:
    for file in files:
      s = m.reply_video(file, reply_markup=original, caption=caption)
  original = getattrs(m, s)
  c.edit_inline_reply_markup(s.id, original)
  #send_videos(m, c, original, files, caption)
  c.delete_messages(m.chat.id, sending.id)

def instagram(c, m, download, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  files, video = IGDL(url)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    send_videos(m, c, original, files, caption)
  c.delete_messages(m.chat.id, sending.id)