from hydrogram.enums import ChatAction
from data import dapi
from io import BytesIO
import logging, requests

def YTM(url):
    data = requests.get(f"{dapi}/music", params={"url":url}, timeout=60).json()
    content = requests.get(data["url"]).content
    file = BytesIO(content)
    file.name = "music.mp3"
    return file

def music(m, attrs):
    try:
        url = attrs.url
        caption = attrs.caption
        m.reply_chat_action(ChatAction.RECORD_AUDIO)
        audio = YTM(url)
        m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
        m.reply_audio(audio, caption=caption)
        print("Completed")
    except Exception as e:
        logging.critical(e)