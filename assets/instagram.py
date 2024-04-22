import logging
from io import BytesIO

import requests
from hydrogram.enums import ChatAction

from data import dapi
from misc import send_photos, send_videos


def IGDL(url):
    data = requests.get(f"{dapi}/instagram", params={"url": url}, timeout=180).json()
    files = []
    links = data["url"]
    is_video = data["is_video"]
    if is_video:
        for link in links:
            try:
                req = requests.get(link)
                file = BytesIO(req.content)
                file.name = "instagram.mp4"
            except Exception as e:
                logging.critical(e)
                continue
            files.append(file)

    print("Instagram")
    return links, files, is_video


def instagram(m, attrs):
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_VIDEO)
    links, files, is_video = IGDL(url)
    if not is_video:
        send_photos(m, links, button, caption)
    else:
        try:
            send_videos(m, links, button, caption)
        except Exception:
            send_videos(m, files, button, caption)
    print("Completed")
