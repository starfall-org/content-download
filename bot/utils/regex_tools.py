import re

from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.schemas.bot import ParsedAtributes


def parse_attributes(m: Message) -> ParsedAtributes:
    text = m.reply_to_message.text if m.reply_to_message else m.text
    user_name = m.sender_chat.title if m.sender_chat else m.from_user.first_name
    user_id = m.sender_chat.id if m.sender_chat else m.from_user.id
    url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Original", url=url),
                InlineKeyboardButton("Discord", url="https://discord.gg/9WF54BSc4s"),
                InlineKeyboardButton("Channel", url="https://t.me/starfall_org"),
            ]
        ]
    )
    caption = f"**Sent by --__[{user_name}](tg://user?id={user_id})__--**"

    return ParsedAtributes(url=url, button=button, caption=caption)
