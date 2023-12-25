from api_callback.Meta import FBDL, IGDL
from etc.util import save, send_videos, send_photos
from etc.var import rv, sv
import re

def facebook(c, m):
  m.reply_chat_action(rv)
  files = FBDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  send_videos(m, c, original, files, caption)
  c.delete_messages(m.chat.id, sending.id)

def instagram(c, m):
  m.reply_chat_action(rv)
  download = m.reply("**Downloading**`...`", quote=True)
  files, video = IGDL(url)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  if video == False:
    send_photos(m, c, original, files, caption)
  elif video == True:
    send_videos(m, c, original, files, caption)
  c.delete_messages(m.chat.id, sending.id)