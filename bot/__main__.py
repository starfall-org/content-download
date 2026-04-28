import asyncio
from datetime import datetime

from hydrogram import Client, idle

from bot.config import BOT_TOKEN, logger
from bot.database import Database

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
BROADCAST_DELAY_SECONDS = 3


def _ensure_event_loop() -> None:
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


_ensure_event_loop()

app = Client(
    __name__,
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "bot/plugins"},
)


async def main() -> None:
    await app.start()
    bot_info = await app.get_me()
    logger.info(bot_info.first_name)
    await broadcast_online(app)
    await idle()
    await app.stop()


def _online_message() -> str:
    timestamp = datetime.now().strftime("%b %d, %Y - %H:%M:%S")
    return (
        f"__{timestamp}__\n"
        "**The bot has connected!**🟢"
        "\n```\nThis is an automated message, please do not reply.\n```"
    )


async def broadcast_online(client: Client) -> None:
    db = Database()
    content = _online_message()
    chats = [chat.id for chat in await db.all_chat()]

    for chat in chats:
        try:
            await client.send_message(chat, content)
        except Exception as error:
            logger.error(error)
        await asyncio.sleep(BROADCAST_DELAY_SECONDS)


if __name__ == "__main__":
    app.run(main())
