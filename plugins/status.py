from hydrogram import Client, filters
from hydrogram.types import Message
from hydrogram.enums import ChatAction
from db.client import Database

db = Database()


@Client.on_message(filters.command("status"))
async def status(c: Client, m: Message):
    result = await db.count_chat()
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(
        f"**Chats:** `{result[1]}`\n\n**Bot ID:** `{c.me.id}`",
        quote=True,
    )
