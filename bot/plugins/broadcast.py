import asyncio

from hydrogram import Client, enums, filters, types
from hydrogram.types import Message

from bot.database.client import Database
from bot.services.broadcasts import broadcast_text, build_automated_message
from bot.utils.ai import generate_alert

db = Database()


@Client.on_message(filters.command("broadcast") & filters.user(7642104102))  # type: ignore
async def broadcast(client: Client, message: Message):
    content = message.text.split(" ", 1)[1]
    count = await broadcast_text(client, content, with_typing=True)
    await message.reply(f"Broadcasted to {count} chats")


@Client.on_message(filters.command("alert") & filters.user(7642104102))  # type: ignore
async def alert_users(client: Client, message: Message):
    chats = await db.all_chat()
    for chat in chats:
        if chat.is_group or chat.is_supergroup:
            alert_message = "Hello! I have lost my old account from last year and no longer have the authority to manage this bot. Therefore, this bot may cease to function in the future. To continue your experience, you should switch to using **Next Download (@nextdownload_bot)**. However, this does not mean I will shut down this bot, you can still continue to use it as usual."
            await client.send_message(
                chat.id,
                build_automated_message(f"__{alert_message}__"),
            )
            await message.reply(f"Alerted group: {chat.id}")
        else:
            user = await client.get_users(chat.id)
            if user and isinstance(user, types.User):
                alert_message = await generate_alert(user.language_code or "en")
                alert_message = alert_message + "\n\n🤖`Translated by AI.`"
                await client.send_chat_action(chat.id, enums.ChatAction.TYPING)
                await asyncio.sleep(2)
                await client.send_message(
                    chat.id,
                    build_automated_message(f"__{alert_message}__"),
                )
                await message.reply(f"Alerted user: {chat.id}")
        await asyncio.sleep(3)

    await message.reply(f"Alerted {len(chats)} users and groups")


@Client.on_message(filters.command("test_alert") & filters.user(7642104102))  # type: ignore
async def test_alert(client: Client, message: Message):
    await message.reply_chat_action(enums.ChatAction.TYPING)
    user = await client.get_users(message.chat.id)
    if user and isinstance(user, types.User):
        alert_message = await generate_alert(user.language_code or "English")
        alert_message = alert_message + "\n🤖`Translated by AI.`"
        await message.reply(build_automated_message(f"__{alert_message}__"))
