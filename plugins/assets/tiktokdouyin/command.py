import logging
from io import BytesIO
import requests
from pyrogram.enums import ChatAction
from data import DAPI
from plugins.util import send_photos, save
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from plugins.var import Attrs
from plugins.upload import upload
from .tiktokuser import TikTokUser


def get(url):
    data = requests.get(f"{DAPI}/tikdou", params={"url": url}, timeout=180).json()
    link = data["url"]
    if data["is_video"]:
        content = requests.get(link, timeout=120).content
        file_obj = BytesIO(content)
        file_obj.name = "tiktokdouyin.mp4"
        is_video = True
    else:
        file_obj = []
        for photo_link in link:
            try:
                photo_data = requests.get(photo_link, timeout=120).content
                photo_file = BytesIO(photo_data)
                photo_file.name = "photo.jpg"
            except Exception as e:
                logging.critical(e)
                continue
            file_obj.append(photo_file)
        is_video = False

    return (link, file_obj), is_video


def _channel(_, __, m):
    return (
        not m.sender_chat.username == "contentdownload"
        if m.sender_chat
        and m.forward_from_chat
        and m.chat.username == "contentdownload_group"
        else True
    )


@Client.on_message(
    ((filters.regex("http|https") & filters.regex("tiktok.|douyin.")))
    & filters.incoming
    & filters.create(_channel)
)
def tikdou_download(c, m):
    save(m)
    attrs = Attrs(m)
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_VIDEO)
    try:
        media, is_video = get(url)
    except Exception:
        TikTokUser(m, url, caption, get)
        return
    if not is_video:
        send_photos(m, media[0], button, caption)
    else:
        m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        try:
            m.reply_video(media[0], caption=caption, reply_markup=button)
        except Exception:
            m.reply_video(media[1], caption=caption, reply_markup=button)
    print("TikTok and Douyin Done")
    m.delete()
    if m.chat.username == "contentdownload":
        upload(media[1], media[0])
