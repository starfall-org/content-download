import hydrogram


def make_bot(token: str, content_api: str, database_url) -> hydrogram.Client:
    return hydrogram.Client(
        __name__,
        6,
        "eb06d4abfb49dc3eeb1aeb98ae0f581e",
        bot_token=token,
        plugins={"root": "plugins"},
        max_concurrent_transmissions=100,
    )
