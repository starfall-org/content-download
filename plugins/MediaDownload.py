from pyrogram import Client, filters
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.media.bytedance import tikdou
from plugins.media.meta import facebook, instagram
from plugins.media.youtube import youtube, music, other
from etc.util import save
from etc.var import t
import re

def getattrs(m):
  url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original", url=url)]])
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  return url, original, caption

@Client.on_message(filters.command("music"))
def music_handler(c, m):
  save(m)
  url, _, caption = getattrs(m)
  download = m.reply("**Downloading**`...`", quote=True)
  music(c, m, url, caption, download)
  try:
    m.delete()
  except:
    pass

@Client.on_message(filters.regex("https://|http://"))
def media_handler(c, m):
  url, original, caption= getattrs(m)
  media_group = ["youtube", "youtu.be", "tiktok", "douyin", "iesdouyin", "facebook", "fb", "instagram"]
  is_media = False
  if any(media in url for media in media_group):
    m.reply_chat_action(t)
    save(m)
    download = m.reply("**Downloading**`...`", quote=True)
    if any(reg in url for reg in ["youtube", "youtu.be"]):
      youtube(c, m, url, original, caption, download)
    elif any(reg in url for reg in ["facebook", "fb"]):
      facebook(c, m, url, original, caption, download)
    elif "instagram" in url:
      instagram(c, m, url, original, caption, download)
    else:
      tikdou(c, m, url, original, caption, download)
    is_media = True
  else:
    try:
      file, type = ODL(url)
      if file is None:
        return
    except Exception as e:
      logging.error(e)
      return
    save(m)
    m.reply_chat_action(t)
    download = m.reply("**Downloading**`...`", quote=True)
    other(c, m, file, type, original, caption, download)
    is_media = True
  if is_media:
    try:
      m.delete()
   except:
     pass