import io
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from aiohttp import ClientSession
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from scipy.interpolate import PchipInterpolator

from db.models import GroupStats, MemberCount

from .models import APIResult, Atributes, LinkInfo, Links

API = os.environ["CONTENT_API"]


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
        link = LinkInfo(
            is_video=content.get("is_video", True),
            url=content["result"],
            title=content.get("title"),
        )
        result = Links(standalone=True, content=link)
    return APIResult(
        result=result,
        button=attrs.button,
        caption=attrs.caption,
    )


async def ionify(
    url: str, ext: str, title: str = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
) -> io.BytesIO:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                iofile = io.BytesIO(content)
                iofile.name = f"{title}.{ext}"
                return iofile


def plot_time_series(data: list[MemberCount], group_stats: GroupStats):
    title = f"{group_stats.title} - Members Count"
    save_path = f"tmp/{title}|{group_stats.id}.png"
    data.sort(key=lambda x: x.date)
    dates = [item.date for item in data]
    values = [item.count for item in data]
    dates = pd.to_datetime(dates)
    dates_num = mdates.date2num(dates)
    dates_smooth = np.linspace(dates_num.min(), dates_num.max(), 300)
    pchip = PchipInterpolator(dates_num, values)
    values_smooth = pchip(dates_smooth)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mdates.num2date(dates_smooth), values_smooth, linestyle="-", color="b")
    ax.scatter(dates, values, color="r", zorder=3)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=30, ha="right")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return save_path
