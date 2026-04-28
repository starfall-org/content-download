from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.database import Database

db = Database()


@Client.on_message(filters.command("status"))
async def status(c: Client, m: Message):
    result = await db.count_chat()
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(
        f"**Chats:** `{result}`\n\n**Bot ID:** `{c.me.id}`",
        quote=True,
    )


@Client.on_message(filters.command("test"))
async def test_message(c: Client, m: Message):
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(f"{m}")
