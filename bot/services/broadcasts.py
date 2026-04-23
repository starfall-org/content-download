import asyncio

from hydrogram import Client, enums

from bot.database.client import Database

AUTOMATED_FOOTER = "\n```\nThis is an automated message, please do not reply.\n```"


def build_automated_message(content: str) -> str:
    return f"{content}{AUTOMATED_FOOTER}"


async def broadcast_text(
    client: Client,
    content: str,
    *,
    with_typing: bool = False,
    initial_delay_seconds: int = 2,
    delay_between_messages: int = 3,
) -> int:
    chats = [chat.id for chat in await Database.all_chat()]

    for chat_id in chats:
        try:
            if with_typing:
                await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
                await asyncio.sleep(initial_delay_seconds)

            await client.send_message(chat_id, build_automated_message(content))
        except Exception as exc:
            print(exc)

        await asyncio.sleep(delay_between_messages)

    return len(chats)
