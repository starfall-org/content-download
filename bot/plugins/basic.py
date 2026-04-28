from datetime import datetime

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import logger
from bot.telegram.sys_usage import show_usage

DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
WELCOME_TEXT = (
    "__Welcome to Content Download!\n\n"
    "This bot helps you download content from various sources.__"
)


def _support_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Channel", url="https://t.me/starfall_org"),
                InlineKeyboardButton("Group", url="https://t.me/starfall_community"),
                InlineKeyboardButton("StarChatter", url="https://t.me/StarChatterBot"),
            ],
            [
                InlineKeyboardButton(
                    "Discord Server",
                    url="https://discord.gg/9WF54BSc4s",
                ),
            ],
        ]
    )


def _log_start(message: Message) -> None:
    if message.from_user:
        sender = f"USER: [{message.from_user.id}] {message.from_user.first_name}"
    elif message.sender_chat:
        sender = f"SENDER: [{message.sender_chat.id}] {message.sender_chat.title}"
    else:
        sender = "SENDER: Unknown"

    logger.info(
        (
            f"[{datetime.now().strftime(DATE_FORMAT)}]\n"
            f"{sender}\n"
            f"CHAT: [{message.chat.id}] {message.chat.title}\n"
            "ACTION: start"
        )
    )


@Client.on_message(filters.command(["start", "help"]) & filters.private)
async def reply_start(_: Client, message: Message) -> None:
    await message.reply_chat_action(ChatAction.TYPING)
    await message.reply(
        f"**Content Download**\n\n{WELCOME_TEXT}\n{show_usage('idle')}",
        reply_markup=_support_keyboard(),
    )
    _log_start(message)


@Client.on_message(filters.command("rss"))
async def resource_usage(client: Client, message: Message) -> None:
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.reply(show_usage("idle"), quote=True)
