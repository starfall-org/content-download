from asyncer import asyncify
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import count


@Client.on_message(filters.command("status"))
async def status(c: Client, m: Message):
    result = await asyncify(count)()
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    await m.reply(
        f"**Chats:** `{result[0]}`\n**Users:** `{result[1]}`\n**Bot ID:** `{c.me.id}`",
        quote=True,
    )
