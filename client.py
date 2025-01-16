import hydrogram


async def run(bot: hydrogram.Client) -> hydrogram.Client:
    await bot.start()
    bot_info = await bot.get_me()
    print(bot_info.first_name)
    await hydrogram.idle()
    return await bot.stop()


def make_bot(token: str, content_api: str, database_url) -> hydrogram.Client:
    setattr(hydrogram, "API", content_api)
    setattr(hydrogram, "DATABASE_URL", database_url)
    setattr(hydrogram.Client, "online", run)
    return hydrogram.Client(
        __name__,
        6,
        "eb06d4abfb49dc3eeb1aeb98ae0f581e",
        bot_token=token,
        plugins={"root": "plugins"},
        max_concurrent_transmissions=100,
    )
