from threading import Thread
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from hydrogram.enums import ChatAction
from hydrogram.types import InputMediaPhoto, InputMediaVideo

from data import Save

from .var import proxies

sp = ChatAction.UPLOAD_PHOTO
sv = ChatAction.UPLOAD_VIDEO


def get_media_links(url):
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    html = requests.get(url, headers={"User-Agent": user_agent}).text
    soup = BeautifulSoup(html, "html.parser")
    list_links = [
        urljoin(url, a["href"]) for a in soup.select("li.tiktok-18tsjrs-LiVideoItem a")
    ]
    return list_links


def save(m):
    if str(m.chat.id).startswith("-100"):
        Thread(target=Save.chat, args=(m,)).start()
    if m.from_user:
        Thread(target=Save.user, args=(m,)).start()
        print(f"{m.from_user.first_name} ID:{m.from_user.id}")
    else:
        print(f"{m.sender_chat.title} ID:{m.sender_chat.id}")


def send_photos(m, photo_links: List[str], button, caption):
    m.reply_chat_action(sp)
    if len(photo_links) == 1:
        m.reply_photo(photo_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(photo_links) - 1, 10):
            media_group = [
                InputMediaPhoto(link)
                for link in photo_links[i : min(i + 10, len(photo_links) - 1)]
            ]
            m.reply_chat_action(sp)
            m.reply_media_group(media_group)
        m.reply_chat_action(sp)
        m.reply_photo(photo_links[-1], caption=caption, reply_markup=button)


#
def send_videos(m, video_links: List[str], button, caption):
    m.reply_chat_action(sv)
    if len(video_links) == 1:
        m.reply_video(video_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(video_links) - 1, 10):
            media_group = [
                InputMediaVideo(link)
                for link in video_links[i : min(i + 10, len(video_links) - 1)]
            ]
            m.reply_chat_action(sv)
            m.reply_media_group(media_group)
        m.reply_chat_action(sv)
        m.reply_video(video_links[-1], caption=caption, reply_markup=button)


def server_info():
    try:
        response = requests.get("https://ipinfo.io", proxies=proxies)
        data = response.json()
        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        provider = data.get("org", "N/A")

        server_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nProvider: {provider}"

    except Exception as e:
        server_info = f"Error: {e}"
    return server_info
