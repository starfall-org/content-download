from hydrogram import Client, filters
from hydrogram.types import Message
from hydrogram.enums import ChatAction
from db import count


@Client.on_message(filters.command("status"))
async def status(c: Client, m: Message):
    result = await count()
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(
        f"**Chats:** `{result[1]}`\n**Users:** `{result[0]}`\n**Bot ID:** `{c.me.id}`",
        quote=True,
    )
