import hydrogram


def make_bot(token: str, content_api: str, database_url) -> hydrogram.Client:
    setattr(hydrogram, "API", content_api)
    setattr(hydrogram, "DATABASE_URL", database_url)
    return hydrogram.Client(
        __name__,
        6,
        "eb06d4abfb49dc3eeb1aeb98ae0f581e",
        bot_token=token,
        plugins={"root": "plugins"},
        max_concurrent_transmissions=100,
    )


async def serve(bot: hydrogram.Client, scheduled: callable) -> hydrogram.Client:
    await bot.start()
    scheduled(bot)
    bot_info = await bot.get_me()
    print(bot_info.first_name)
    await hydrogram.idle()
    return await bot.stop()
