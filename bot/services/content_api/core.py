from aiohttp import ClientSession
from hydrogram.types import Message

from bot.config import CONTENT_API
from bot.schemas.api import ResponseGroup, ResponseItem
from bot.schemas.bot import ResponseUtility
from bot.utils.regex_tools import parse_attributes


async def get_api_result(endpoint: str, m: Message) -> ResponseUtility:
    api_url = f"{CONTENT_API}/{endpoint}"
    attrs = parse_attributes(m)
    url = attrs.url
    async with ClientSession() as session:
        async with session.get(api_url, params={"url": url}) as response:
            content = await response.json()

    if isinstance(content, list):
        result = []
        for link in content:
            match endpoint:
                case "instagram":
                    result.append(
                        ResponseItem(
                            url=link["result"],
                            mediatype="video" if link["is_video"] else "image",
                        )
                    )
                case _:
                    result.append(
                        ResponseItem(
                            url=link["result"],
                            mediatype="video" if link["is_video"] else "image",
                        )
                    )
        result = ResponseGroup(is_list=True, content=result)
    else:
        link = ResponseItem(
            url=content["result"],
            mediatype="video" if content["is_video"] else "image",
            title=content.get("title"),
        )
        result = ResponseGroup(is_list=False, content=link)
    return ResponseUtility(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )
