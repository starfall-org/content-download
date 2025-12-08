from datetime import datetime

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import logger
from bot.database.client import Database
from bot.utils.sys_usage import show_usage

db = Database()


@Client.on_message(filters.command(["start", "help"]) & filters.private)
async def reply_start(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    text = "__Welcome to Content Download!\n\nThis bot helps you download content from various sources.__"
    await m.reply(
        f"**Content Download**\n\n{text}\n{show_usage('idle')}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Channel", url="https://t.me/starfall_org"),
                    InlineKeyboardButton(
                        "Group", url="https://t.me/starfall_community"
                    ),
                    InlineKeyboardButton(
                        "StarChatter", url="https://t.me/StarChatterBot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Discord Server", url="https://discord.gg/9WF54BSc4s"
                    ),
                ],
            ]
        ),
    )
    logger.info(
        (
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
            + f"USER: [{m.from_user.id}] {m.from_user.first_name}"
            if m.from_user
            else f"SENDER: [{m.sender_chat.id}] {m.sender_chat.title}"
            + f"CHAT: [{m.chat.id}] {m.chat.title}"
            + "ACTION: start"
        )
    )


@Client.on_message(filters.command("rss") )
async def resource_usage(c: Client, m: Message):
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(show_usage("idle"), quote=True)