from datetime import datetime

from hydrogram import Client, idle

from bot.config import BOT_TOKEN, logger
from bot.services.broadcasts import broadcast_text

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"


def create_app() -> Client:
    return Client(
        __name__,
        API_ID,
        API_HASH,
        bot_token=BOT_TOKEN,
        plugins={"root": "bot/plugins"},
    )


app = create_app()


async def main():
    await app.start()
    bot_info = await app.get_me()
    logger.info(bot_info.first_name)
    await broadcast_online(app)
    await idle()
    await app.stop()


async def broadcast_online(client: Client):
    now = datetime.now()
    content = (
        f"__{now.strftime('%b %d, %Y - %H:%M:%S')}__\n**The bot has connected!**🟢"
    )
    await broadcast_text(client, content)


if __name__ == "__main__":
    app.run(main())
