from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from init import webstream 
import re

class Attrs:
    def __init__(self, m):
        try:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
        except:
            url = re.search(r"(?P<url>https?://[^\s]+)", m.reply_to_message.text).group("url")
        self.url = url
        self.button = InlineKeyboardMarkup([[InlineKeyboardButton("Original", url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        try:
            user_name = m.sender_chat.title
            user_id = m.sender_chat.id
        except:
            user_name = m.from_user.first_name
            user_id = m.from_user.id
        self.caption = f'**Sent by --__[{user_name}](tg://user?id={user_id})__--**'