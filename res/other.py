from hydrogram.enums import ChatAction
from data import dapi
from io import BytesIO
from ext import Formats
import logging, requests, re

def ODL(url):
    data = requests.get(f"{dapi}/other", params={"url": url}, timeout=60).json()
    r = requests.get(data["url"])
    content = r.content
    try:
        header = r.headers['Content-Disposition']
        filename = re.findall("filename=(.+)", header)[0]
    except Exception:
        filename = "download"
        if r.headers["Content-Type"] in Formats().audio:
            filename = f"{filename}.mp3"
            types = "audio"
            file = BytesIO(content)
            file.name = filename
        if r.headers["Content-Type"] in Formats().image:
            types = "image"
        elif r.headers["Content-Type"] in Formats().video:
            types = "video"
        if r.headers["Content-Type"] in Formats().skip:
            return None, None
        else:
            types = "other"
    print("Other")
    return file, types

def other(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        file, types = ODL(url)
        if types == "image":
            m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            m.reply_photo(file, caption=caption, reply_markup=button)
        elif types == "video":
            m.reply_chat_action(ChatAction.UPLOA_VIDEO)
            m.reply_video(file, caption=caption, reply_markup=button)
        elif types == "audio":
            m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            m.reply_audio(file, caption=caption)
        else:
            m.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
            m.reply_document(file, reply_markup=button, caption=caption)
        print("Completed")
    except Exception as e:
        logging.critical(e)