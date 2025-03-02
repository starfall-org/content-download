import os

from aiohttp import ClientSession
from hydrogram.types import Message

from models.api_models import APIResult, APIResultGroup
from models.bot_models import (
    FilteredMessageAtributes,
    PreResponseAtributes,
)

from .util import get_attributes

API = os.environ["CONTENT_API"]


async def get_api_result(endpoint: str, m: Message) -> PreResponseAtributes:
    api_url = f"{API}/{endpoint}"
    attrs: FilteredMessageAtributes = get_attributes(m)
    url: str = attrs.url
    async with ClientSession() as session:
        async with session.get(api_url, params={"url": url}) as response:
            if response.status == 200:
                content = await response.json()
                await session.close()

    if isinstance(content["result"], list):
        result = []
        for link in content["result"]:
            match endpoint:
                case "instagram":
                    result.append(APIResult(is_video=link["is_video"], url=link["url"]))
                case _:
                    result.append(APIResult(is_video=False, url=link))
        result = APIResultGroup(standalone=False, content=result)
    else:
        link = APIResult(
            is_video=content.get("is_video", True),
            url=content["result"],
            title=content.get("title"),
        )
        result = APIResultGroup(standalone=True, content=link)
    return PreResponseAtributes(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )
