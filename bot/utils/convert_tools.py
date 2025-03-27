import io
from datetime import datetime
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from bot.schemas.api import ResponseItem


async def convert_url_to_io(
    url: str, ext: str, title: str = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
) -> io.BytesIO:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{title}.{ext}"
                return iofile


async def item_to_io(
    media: ResponseItem,
) -> ResponseItem:
    return ResponseItem(
        url=await convert_url_to_io(
            media.url,
            ext="mp4" if media.mediatype == "video" else "png",
            title=media.title,
        ),
        mediatype=media.mediatype,
    )


async def list_to_io(
    media: list[ResponseItem],
) -> list[ResponseItem]:
    return [
        ResponseItem(
            url=await convert_url_to_io(
                link.url,
                ext="mp4" if link.mediatype == "video" else "png",
                title=link.title,
            ),
            mediatype=link.mediatype,
        )
        for link in media
    ]
