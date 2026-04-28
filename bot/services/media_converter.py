import io
from datetime import datetime
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from bot.schemas.download import CommonLinks, YoutubeLinks

MEDIA_EXTENSIONS = {
    "audio": "mp3",
    "video": "mp4",
    "image": "png",
}


async def convert_url_to_io(
    url: str | io.BytesIO,
    ext: str,
    title: str | None = None,
) -> io.BytesIO:
    if isinstance(url, io.BytesIO):
        return url

    filename = title or datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()

    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{filename}.{ext}"
                return iofile

    raise ValueError(f"Unable to download media from {url}")


def _extension(media_type: str) -> str:
    return MEDIA_EXTENSIONS.get(media_type, "bin")


async def convert_to_io(
    obj: CommonLinks | YoutubeLinks,
) -> CommonLinks | YoutubeLinks:
    if isinstance(obj, CommonLinks):
        for link in obj.links:
            link.url = await convert_url_to_io(
                link.url,
                ext=_extension(link.type),
                title=obj.title,
            )
    elif isinstance(obj, YoutubeLinks):
        obj.video.url = await convert_url_to_io(
            obj.video.url,
            ext=_extension(obj.video.type),
            title=obj.title,
        )
        obj.video_no_audio.url = await convert_url_to_io(
            obj.video_no_audio.url,
            ext=_extension(obj.video_no_audio.type),
            title=obj.title,
        )
        obj.audio.url = await convert_url_to_io(
            obj.audio.url,
            ext=_extension(obj.audio.type),
            title=obj.title,
        )
    return obj
