import asyncio
from hydrogram import Client, filters
from hydrogram.types import Message
from db.client import Database

db = Database()


@Client.on_message(filters.command("broadcast") & filters.user(7642104102))
async def broadcast(client: Client, message: Message):
    content = message.text.split(" ", 1)[1]
    chats = [chat.id for chat in await db.all_chat()]
    for chat in chats:
        try:
            await client.send_message(chat, content)
        except Exception as e:
            print(e)
        await asyncio.sleep(3)

    await message.reply(f"Broadcasted to {len(chats)} chats")
