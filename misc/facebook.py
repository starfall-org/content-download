import logging
from io import BytesIO
import requests
from hydrogram.enums import ChatAction
from data import DAPI


def FBDL(url):
    data = requests.get(f"{DAPI}/facebook", params={"url": url}, timeout=180).json()
    link = data["url"][0]
    req = requests.get(link)
    file = BytesIO(req.content)
    file.name = "video.mp4"
    print("Facebook")
    return file, link


def facebook(m, attrs):
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_VIDEO)
    files, links = FBDL(url)
    m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
    try:
        m.reply_video(links, caption=caption, reply_markup=button)
    except Exception as e:
        logging.critical(e)
        m.reply_video(files, caption=caption, reply_markup=button)
    print("Completed")
