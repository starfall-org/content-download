import re
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from aiohttp import ClientSession
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


def get_attrs(m: Message):
    text = m.reply_to_message.text if m.reply_to_message else m.text
    user_name = m.sender_chat.title if m.sender_chat else m.from_user.first_name
    user_id = m.sender_chat.id if m.sender_chat else m.from_user.id

    class Attrs:
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

    return Attrs


async def api_handler(api_url: str, m: Message):
    atr = get_attrs(m)
    url = atr.url
    async with ClientSession() as session:
        async with session.get(api_url, params={"url": url}) as response:
            if response.status == 200:
                content = await response.json()
                await session.close()

    class Result:
        is_video: bool = content.get("is_video", True)
        result: list | str = content["url"]
        button: InlineKeyboardMarkup = atr.button
        caption: str = atr.caption

    return Result


async def ionify(url: str):
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    date = datetime.now(tz)
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{date}.mp4"
                return iofile
