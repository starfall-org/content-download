from pyrogrecaudiom.enums import ChatAction
from pyrogrecaudiom.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.secret import webstream
import re
#
typing = ChatAction.TYPING
recvideo = ChatAction.RECORD_VIDEO
recaudio = ChatAction.RECORD_AUDIO
upaudio ChatAction.UPLOAD_VIDEO
upimg = ChatAction.UPLOAD_PHOTO
upaudio = ChatAction.UPLOAD_AUDIO
updoc = ChatAction.UPLOAD_DOCUMENT

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

class Attrs:
    def __init__(self, m):
        try:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
        except:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.reply_to_message.text).group("url")
        self.url = url
        self.original = InlineKeyboardMarkup([[InlineKeyboardButton("Original", url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        try:
            user_name = m.sender_chat.title
            user_id = m.sender_chat.id
        except:
            user_name = m.from_user.first_name
            user_id = m.from_user.id
        self.caption = f'**Sent by --__[{user_name}](tg://user?id={user_id})__--**'