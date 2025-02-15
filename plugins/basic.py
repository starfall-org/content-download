from datetime import datetime

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from db.client import Database

db = Database()


async def get_start_message():
    try:
        text = await db.get_preset("start_message")
        if text:
            return text
        else:
            raise Exception
    except Exception:
        await db.set_preset(
            "start_message", "Welcome! Send a link and I'll send you the content."
        )
        return "Welcome! Send a link and I'll send you the content."


@Client.on_message(filters.command(["start", "help"]) & filters.private)
async def reply_start(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    text = await get_start_message()
    panel_link = await db.get_preset("panel_link")
    await m.reply(
        f"**Content Downloa**\n\n{text}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group", url="https://t.me/contentdownload_group"
                    ),
                    InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
                    InlineKeyboardButton("Panel", url=panel_link),
                ],
            ]
        ),
    )
    print(
        (
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
            + f"USER: [{m.from_user.id}] {m.from_user.first_name}"
            if m.from_user
            else f"SENDER: [{m.sender_chat.id}] {m.sender_chat.title}"
            + f"CHAT: [{m.chat.id}] {m.chat.title}"
            + "ACTION: start"
        ),
        flush=True,
    )
