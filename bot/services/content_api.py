from aiohttp import ClientSession
from dacite import from_dict
from hydrogram.types import Message

from bot.config import CONTENT_API
from bot.schemas.download import CommonLinks, YoutubeLinks
from bot.schemas.telegram import ResponseUtility
from bot.telegram.parsing import parse_attributes

YOUTUBE_ENDPOINT = "youtube"


def _response_schema(endpoint: str):
    if endpoint == YOUTUBE_ENDPOINT:
        return YoutubeLinks

    return CommonLinks


async def get_api_result(endpoint: str, m: Message) -> ResponseUtility:
    attrs = parse_attributes(m)

    async with ClientSession() as session:
        async with session.get(
            f"{CONTENT_API}/{endpoint}",
            params={"url": attrs.url},
        ) as response:
            content = await response.json()

    result = from_dict(data_class=_response_schema(endpoint), data=content)
    return ResponseUtility(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )
