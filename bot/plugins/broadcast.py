import asyncio

from hydrogram import Client, enums, filters, types
from hydrogram.types import Message

from bot.config import logger
from bot.database import Database
from bot.services.alerts import generate_alert

ADMIN_ID = 7642104102
ACTION_DELAY_SECONDS = 2
BROADCAST_DELAY_SECONDS = 3
AUTOMATED_FOOTER = "\n```\nThis is an automated message, please do not reply.\n```"
LEGACY_ALERT_MESSAGE = (
    "Hello! I have lost my old account from last year and no longer have the "
    "authority to manage this bot. Therefore, this bot may cease to function "
    "in the future. To continue your experience, you should switch to using "
    "**Next Download (@nextdownload_bot)**. However, this does not mean I will "
    "shut down this bot, you can still continue to use it as usual."
)
TRANSLATED_BY_AI = "\n\n🤖`Translated by AI.`"

db = Database()


def _automated_message(content: str, italic: bool = False) -> str:
    body = f"__{content}__" if italic else content
    return f"{body}{AUTOMATED_FOOTER}"


async def _send_with_typing(client: Client, chat_id: int, content: str) -> None:
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(ACTION_DELAY_SECONDS)
    await client.send_message(chat_id, content)


@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))  # type: ignore
async def broadcast(client: Client, message: Message) -> None:
    content = message.text.split(" ", 1)[1]
    chats = [chat.id for chat in await db.all_chat()]

    for chat_id in chats:
        try:
            await _send_with_typing(
                client,
                chat_id,
                _automated_message(content),
            )
        except Exception as error:
            logger.error(error)
        await asyncio.sleep(BROADCAST_DELAY_SECONDS)

    await message.reply(f"Broadcasted to {len(chats)} chats")


@Client.on_message(filters.command("alert") & filters.user(ADMIN_ID))  # type: ignore
async def alert_users(client: Client, message: Message) -> None:
    chats = await db.all_chat()

    for chat in chats:
        if chat.is_group or chat.is_supergroup:
            await client.send_message(
                chat.id,
                _automated_message(LEGACY_ALERT_MESSAGE, italic=True),
            )
            await message.reply(f"Alerted group: {chat.id}")
        else:
            user = await client.get_users(chat.id)
            if user and isinstance(user, types.User):
                alert_message = await generate_alert(user.language_code or "en")
                await _send_with_typing(
                    client,
                    chat.id,
                    _automated_message(
                        f"{alert_message}{TRANSLATED_BY_AI}",
                        italic=True,
                    ),
                )
                await message.reply(f"Alerted user: {chat.id}")
        await asyncio.sleep(BROADCAST_DELAY_SECONDS)

    await message.reply(f"Alerted {len(chats)} users and groups")


@Client.on_message(filters.command("test_alert") & filters.user(ADMIN_ID))  # type: ignore
async def test_alert(client: Client, message: Message) -> None:
    await message.reply_chat_action(enums.ChatAction.TYPING)
    user = await client.get_users(message.chat.id)
    if user and isinstance(user, types.User):
        alert_message = await generate_alert(user.language_code or "English")
        await message.reply(
            _automated_message(
                f"{alert_message}\n🤖`Translated by AI.`",
                italic=True,
            )
        )
