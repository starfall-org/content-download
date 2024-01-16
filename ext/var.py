from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.secret import webstream
import re
#
t = ChatAction.TYPING
rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sp = ChatAction.UPLOAD_PHOTO
sm = ChatAction.UPLOAD_AUDIO
sd = ChatAction.UPLOAD_DOCUMENT

image_formats = [
    "image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp",
    "image/svg+xml", "image/bmp"
]

video_formats = [
    "video/mp4", "video/webm", "video/ogg", "video/avi", "video/mov",
    "video/mpeg", "video/x-flv", "video/3gpp", "video/h261", "video/h263"
]

audio_formats = [
    "audio/mpeg", "audio/ogg", "audio/aac", "audio/midi", "audio/wav",
    "audio/webm", "audio/mp3"
]

skip_formats = [
    "application/json", "text/plain", "text/plain; charset=utf-8",
    "text/html; charset=UTF-8"
]

button = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton("Youtube",
                             url="https://youtube.com/@DouyinShare")
    ],
     [
         InlineKeyboardButton("Group",
                              url="https://t.me/contentdownload_group"),
         InlineKeyboardButton("Channel", url="https://t.me/contentdownload")
     ]])

def getattrs(m, sf=None):
  try:
      url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
  except:
      url = re.search(r"(?P<url>https?://[^\s]+)", m.reply_to_message.text).group("url")
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original", url=url)]])
  if sf:
    original = InlineKeyboardMarkup([[InlineKeyboardButton("Original", url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group")],[InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
    return original
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**Sender: --__[{user_name}](tg://user?id={user_id})__--**'
  return url, original, caption