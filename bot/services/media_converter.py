import io
from datetime import datetime
from zoneinfo import ZoneInfo

from aiohttp import ClientSession, ClientTimeout

from bot.schemas.download import CommonLinks

DOWNLOAD_TIMEOUT = ClientTimeout(total=180)
MEDIA_EXTENSIONS = {
    "audio": "mp3",
    "video": "mp4",
    "image": "png",
    "document": "bin",
    "hls": "mp4",
}


def _extension(link_type: str, explicit: str | None) -> str:
    if explicit:
        return explicit.lstrip(".")
    return MEDIA_EXTENSIONS.get(link_type, "bin")


async def convert_url_to_io(
    url: str | io.BytesIO,
    ext: str,
    title: str | None = None,
) -> io.BytesIO:
    if isinstance(url, io.BytesIO):
        return url

    filename = title or datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()

    async with ClientSession(timeout=DOWNLOAD_TIMEOUT) as session:
        async with session.get(url, allow_redirects=True) as response:
            if response.status == 200:
                iofile = io.BytesIO(await response.read())
                iofile.name = f"{filename}.{ext}"
                return iofile

    raise ValueError(f"Unable to download media from {url}")


async def convert_to_io(obj: CommonLinks) -> CommonLinks:
    for link in obj.media:
        link.url = await convert_url_to_io(
            link.url,
            ext=_extension(link.type, link.extension),
            title=obj.title,
        )
    return obj
