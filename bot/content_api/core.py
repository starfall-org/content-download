from aiohttp import ClientSession
from dacite import from_dict
from hydrogram.types import Message

from bot.config import CONTENT_API
from bot.schemas.bot import ResponseUtility
from bot.schemas.common_link import CommonLinks
from bot.schemas.youtube_link import YoutubeLinks
from bot.utils.regex_tools import parse_attributes


async def get_api_result(endpoint: str, m: Message) -> ResponseUtility:
    api_url = f"{CONTENT_API}/{endpoint}"
    attrs = parse_attributes(m)
    url = attrs.url
    async with ClientSession() as session:
        async with session.get(api_url, params={"url": url}) as response:
            content = await response.json()

    match endpoint:
        case "youtube":
            result = from_dict(data_class=YoutubeLinks, data=content)

        case _:
            result = from_dict(data_class=CommonLinks, data=content)
    return ResponseUtility(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )
