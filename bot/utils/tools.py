import re
from urllib.parse import urljoin
from typing import List

import requests
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatAction
from pyrogram.types import InputMediaPhoto, InputMediaVideo


def get_attrs(m):
    try:
        url = re.search(r"(?P<url>https?://[^\s]+)", m.text).group("url")
    except Exception:
        url = re.search(r"(?P<url>https?://[^\s]+)", m.reply_to_message.text).group(
            "url"
        )
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
    try:
        user_name = m.sender_chat.title
        user_id = m.sender_chat.id
    except Exception:
        user_name = m.from_user.first_name
        user_id = m.from_user.id
    caption = f"**Sent by --__[{user_name}](tg://user?id={user_id})__--**"
    return (url, button, caption)


def tiktok_user_videos(url):
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    html = requests.get(url, headers={"User-Agent": user_agent}, timeout=120).text
    soup = BeautifulSoup(html, "html.parser")
    return [
        urljoin(url, a["href"]) for a in soup.select("li.tiktok-18tsjrs-LiVideoItem a")
    ]


def send_photos(m, photo_links: List[str], button, caption):
    m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    if len(photo_links) == 1:
        m.reply_photo(photo_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(photo_links) - 1, 10):
            media_group = [
                InputMediaPhoto(link)
                for link in photo_links[i : min(i + 10, len(photo_links) - 1)]
            ]
            m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            m.reply_media_group(media_group)
        m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        m.reply_photo(photo_links[-1], caption=caption, reply_markup=button)


def send_videos(m, video_links: List[str], button, caption):
    m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
    if len(video_links) == 1:
        m.reply_video(video_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(video_links) - 1, 10):
            media_group = [
                InputMediaVideo(link)
                for link in video_links[i : min(i + 10, len(video_links) - 1)]
            ]
            m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            m.reply_media_group(media_group)
        m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        m.reply_video(video_links[-1], caption=caption, reply_markup=button)
