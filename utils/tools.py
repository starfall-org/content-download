import re
import io
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from aiohttp import ClientSession
from hydrogram import API
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from .models import Atributes, APIResult, Links, LinkInfo


def __attrs__(m: Message) -> Atributes:
    text = m.reply_to_message.text if m.reply_to_message else m.text
    user_name = m.sender_chat.title if m.sender_chat else m.from_user.first_name
    user_id = m.sender_chat.id if m.sender_chat else m.from_user.id
    url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Original", url=url),
                InlineKeyboardButton(
                    "Youtube", url="https://youtube.com/@tiktokdouyin-share"
                ),
                InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
            ]
        ]
    )
    caption = f"**Sent by --__[{user_name}](tg://user?id={user_id})__--**"

    return Atributes(url=url, button=button, caption=caption)


async def api_handler(endpoint: str, m: Message) -> APIResult:
    api_url = f"{API}/{endpoint}"
    attrs: Atributes = __attrs__(m)
    url: str = attrs.url
    async with ClientSession() as session:
        async with session.get(api_url, params={"url": url}) as response:
            if response.status == 200:
                content = await response.json()
                await session.close()

    if isinstance(content["result"], list):
        result: list[LinkInfo] = []
        for link in content["result"]:
            match endpoint:
                case "instagram":
                    result.append(LinkInfo(is_video=link["is_video"], url=link["url"]))
                case _:
                    result.append(LinkInfo(is_video=False, url=link))
        result = Links(standalone=False, content=result)
    else:
        link = LinkInfo(is_video=content.get("is_video", True), url=content["result"])
        result = Links(standalone=True, content=link)
    return APIResult(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )


async def ionify(url: str, ext: str) -> io.BytesIO:
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    date = datetime.now(tz)
    content = b""
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{date}.{ext}"
                return iofile
