import logging
from io import BytesIO
import requests
from hydrogram.enums import ChatAction
from hydrogram import Client, filters
from misc import Attrs, save
from hydrogram.enums import ChatAction
from data import DAPI


def get(url):
    data = requests.get(f"{DAPI}/youtube", params={"url": url}, timeout=60).json()
    try:
        content = requests.get(data["url"], timeout=120).content
        file = BytesIO(content)
        file.name = "video.mp4"
    except Exception as e:
        logging.critical(e)
        file = data["url"]
    print("Youtube")
    return file


def music(url):
    data = requests.get(f"{DAPI}/music", params={"url": url}, timeout=60).json()
    content = requests.get(data["url"], timeout=120).content
    file = BytesIO(content)
    file.name = f"{data['title']}.mp3"
    print("Music")
    return file


def _channel(_, __, m):
    return (
        not m.sender_chat.username == "contentdownload"
        if m.sender_chat
        and m.forward_from_chat
        and m.chat.username == "contentdownload_group"
        else True
    )


@Client.on_message(filters.command("music"), group=3)
def music_download(c, m):
    save(m)
    attrs = Attrs(m)
    url = attrs.url
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_AUDIO)
    audio = music(url)
    m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    m.reply_audio(audio, caption=caption)
    print("Music Done")


@Client.on_message(
    (filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
    & filters.incoming
    & filters.create(_channel)
)
def youtube_download(c, m):
    save(m)
    attrs = Attrs(m)
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_VIDEO)
    file = get(url)
    m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
    m.reply_video(file, caption=caption, reply_markup=button)
    print("Youtube Done")
