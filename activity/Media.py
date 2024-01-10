from pyrogram import Client, filters
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from media.bytedance import tikdou, tdmusic
from media.meta import facebook, instagram
from media.youtube import youtube, music, other
from api.youtube import ODL
from ext.util import save
from ext.var import t, getattrs
import logging

@Client.on_message(filters.command("music"))
def music_handler(c, m):
  save(m)
  if any(match in m.text for match in ["tiktok", "douyin"]):
      tdmusic(c, m, getattrs)
  else:
      music(c, m, getattrs)
  try:
    m.delete()
  except:
    pass

@Client.on_message(filters.regex("https://|http://") & filters.incoming)
def media_handler(c, m):
  url, _, __ = getattrs(m=m)
  media_group = ["youtube", "youtu.be", "tiktok", "douyin", "iesdouyin", "facebook", "fb", "instagram"]
  is_media = False
  if any(media in url for media in media_group):
    m.reply_chat_action(t)
    save(m)
    if any(reg in url for reg in ["youtube", "youtu.be"]):
      youtube(c, m, getattrs)
    elif any(reg in url for reg in ["facebook", "fb"]):
      facebook(c, m, getattrs)
    elif "instagram" in url:
      instagram(c, m, getattrs)
    else:
      tikdou(c, m, getattrs)
    is_media = True
  else:
    try:
      file, tp = ODL(url)
      if file is None:
        return
    except Exception as e:
      logging.error(e)
      return
    save(m)
    m.reply_chat_action(t)
    other(c, m, file, tp,  getattrs)
    is_media = True
  if is_media:
    try:
      m.delete()
    except:
      pass