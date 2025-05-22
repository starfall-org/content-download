import io
from datetime import datetime
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from bot.schemas.api import ResponseItem
from bot.schemas.common_link import CommonLinks, CommonLink
from bot.schemas.youtube_link import YoutubeLinks, YoutubeLink


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


async def convert_to_io(
    obj: CommonLinks | YoutubeLinks,
) -> CommonLinks | YoutubeLinks:
    if isinstance(obj, CommonLinks):
        if len(obj.links) == 1:
            obj.links[0].url = await convert_url_to_io(
                obj.links[0].url,
                ext="mp4" if obj.links[0].type == "video" else "png",
                title=obj.title,
            )
        else:
            for link in obj.links:
                link.url = await convert_url_to_io(
                    link.url,
                    ext="mp4" if link.type == "video" else "png",
                    title=obj.title,
                )
    elif isinstance(obj, YoutubeLinks):
        obj.video.url = await convert_url_to_io(
            obj.video.url,
            ext="mp4",
            title=obj.title,
        )
        obj.video_no_audio.url = await convert_url_to_io(
            obj.video_no_audio.url,
            ext="mp4",
            title=obj.title,
        )
        obj.audio.url = await convert_url_to_io(
            obj.audio.url,
            ext="mp3",
            title=obj.title,
        )
    return obj
