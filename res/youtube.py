from hydrogram.enums import ChatAction
from data import dapi
from io import BytesIO
import logging, requests

def YTDL(url):
    data = requests.get(f"{dapi}/youtube", params={"url":url}, timeout=60).json()
    try:
        content = requests.get(data["url"]).content
        file = BytesIO(content)
        file.name = "video.mp4"
    except Exception as e:
        logging.critical(e)
        file = data["url"]
    print("Youtube")
    return file

def youtube(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(ChatAction.RECORD_VIDEO)
        file = YTDL(url)
        m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        m.reply_video(file, caption=caption, reply_markup=button)
        print("Completed")
    except Exception as e:
        logging.critical(e)