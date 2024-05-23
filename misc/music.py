from io import BytesIO
import requests
from hydrogram.enums import ChatAction
from data import DAPI


def YTM(url):
    data = requests.get(f"{DAPI}/music", params={"url": url}, timeout=60).json()
    content = requests.get(data["url"]).content
    file = BytesIO(content)
    file.name = "music.mp3"
    print("Music")
    return file


def music(m, attrs):
    url = attrs.url
    caption = attrs.caption
    m.reply_chat_action(ChatAction.RECORD_AUDIO)
    audio = YTM(url)
    m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    m.reply_audio(audio, caption=caption)
    print("Completed")
