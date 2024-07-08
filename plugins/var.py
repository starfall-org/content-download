import re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

proxies = {"http": "http://127.0.0.1:8090", "https": "http://127.0.0.1:8090"}


class Attrs:
    def __init__(self, m):
        try:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
        except:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.reply_to_message.text).group(
                "url"
            )
        self.url = url
        self.button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Original", url=url),
                    InlineKeyboardButton(
                        "Youtube", url="https://youtube.com/@tiktokdouyin-share"
                    ),
                    InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
                ]
            ]
        )
        try:
            user_name = m.sender_chat.title
            user_id = m.sender_chat.id
        except Exception:
            user_name = m.from_user.first_name
            user_id = m.from_user.id
        self.caption = f"**Sent by --__[{user_name}](tg://user?id={user_id})__--**"


#
class Formats:
    def __init__(self):
        self.image = [
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/gif",
            "image/webp",
            "image/svg+xml",
            "image/bmp",
        ]

        self.video = [
            "video/mp4",
            "video/webm",
            "video/ogg",
            "video/avi",
            "video/mov",
            "video/mpeg",
            "video/x-flv",
            "video/3gpp",
            "video/h261",
            "video/h263",
        ]

        self.audio = [
            "audio/mpeg",
            "audio/ogg",
            "audio/aac",
            "audio/midi",
            "audio/wav",
            "audio/webm",
            "audio/mp3",
        ]

        self.skip = [
            "application/json",
            "text/plain",
            "text/plain; charset=utf-8",
            "text/html; charset=UTF-8",
        ]
