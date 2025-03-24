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
        media.is_video,
        await convert_url_to_io(
            media.url, ext="mp4" if media.is_video else "png", title=media.title
        ),
    )


async def list_to_io(
    media: list[ResponseItem],
) -> list[ResponseItem]:
    return [
        ResponseItem(
            link.is_video,
            await convert_url_to_io(
                link.url, ext="mp4" if link.is_video else "png", title=link.title
            ),
        )
        for link in media
    ]
