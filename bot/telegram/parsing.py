import re

from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.schemas.telegram import ParsedAttributes

URL_PATTERN = re.compile(r"(?P<url>https?://[^\s]+)")


def _message_text(message: Message) -> str:
    if message.reply_to_message:
        return message.reply_to_message.text or message.reply_to_message.caption or ""
    return message.text or message.caption or ""


def _sender_identity(message: Message) -> tuple[str, int]:
    if message.sender_chat:
        return message.sender_chat.title, message.sender_chat.id

    user = message.from_user
    if user:
        name = user.first_name or user.last_name or "Unknown"
        return name, user.id

    return "Unknown", message.chat.id


def _extract_url(text: str) -> str:
    match = URL_PATTERN.search(text)
    if not match:
        raise ValueError("No URL found in message text.")

    return match.group("url").rstrip(".,!?)]}>")


def _link_buttons(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Original", url=url),
                InlineKeyboardButton("Discord", url="https://discord.gg/9WF54BSc4s"),
                InlineKeyboardButton("Channel", url="https://t.me/starfall_org"),
            ]
        ]
    )


def parse_attributes(message: Message) -> ParsedAttributes:
    url = _extract_url(_message_text(message))
    user_name, user_id = _sender_identity(message)
    caption = f"||**Sent by --__[{user_name}](tg://user?id={user_id})__--**||"

    return ParsedAttributes(url=url, button=_link_buttons(url), caption=caption)
