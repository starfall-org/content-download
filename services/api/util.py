import re

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from models.bot_models import FilteredMessageAtributes


def get_attributes(m: Message) -> FilteredMessageAtributes:
    text = m.reply_to_message.text if m.reply_to_message else m.text
    user_name = m.sender_chat.title if m.sender_chat else m.from_user.first_name
    user_id = m.sender_chat.id if m.sender_chat else m.from_user.id
    url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
    button = InlineKeyboardMarkup(
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
    caption = f"**Sent by --__[{user_name}](tg://user?id={user_id})__--**"

    return FilteredMessageAtributes(url=url, button=button, caption=caption)
