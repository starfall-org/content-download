import io
from datetime import datetime
from zoneinfo import ZoneInfo

from aiohttp import ClientSession


async def url_to_io(
    url: str, ext: str, title: str = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
) -> io.BytesIO:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{title}.{ext}"
                return iofile
