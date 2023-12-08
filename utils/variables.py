from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

upload_app = os.getenv("UPLOAD_APP")
api_url = os.getenv("API_URL")

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
    "video/mpeg"
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
