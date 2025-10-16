import asyncio
from datetime import datetime

import uvloop
from hydrogram import Client, idle

from bot.config import BOT_TOKEN, logger
from bot.database.client import Database

app = Client(
    __name__,
    6,
    "eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=BOT_TOKEN,
    plugins={"root": "bot/plugins"},
)


async def main():
    await app.start()
    bot_info = await app.get_me()
    logger.info(bot_info.first_name)
    await broadcast_online(app)
    await idle()
    await app.stop()


def install_uvloop():
    if "uvloop" == asyncio.get_event_loop_policy().__module__:
        return
    try:
        uvloop.install()
    except ImportError as e:
        logger.error(f"Failed to install uvloop: {e}")
    policy = asyncio.get_event_loop_policy()
    logger.info(f"Current event loop policy: {policy.__class__.__name__}")


async def broadcast_online(client: Client):
    db = Database()
    now = datetime.now()
    content = (
        f"__{now.strftime('%b %d, %Y - %H:%M:%S')}__\n**The bot has connected!**🟢"
    )
    chats = [chat.id for chat in await db.all_chat()]

    for chat in chats:
        try:
            await client.send_message(chat, content)
        except Exception as e:
            print(e)
        await asyncio.sleep(3)


if __name__ == "__main__":
    install_uvloop()
    app.run(main())
