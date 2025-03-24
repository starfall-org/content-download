import asyncio

import uvloop
from hydrogram import Client, idle

from bot.config import BOT_TOKEN, logger

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


if __name__ == "__main__":
    install_uvloop()
    app.run(main())
