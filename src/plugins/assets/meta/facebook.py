import logging
from io import BytesIO
import requests
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from assets.var import Attrs
from assets.util import save
from environment import DAPI_FB


def FBDL(url):
    data = requests.get(DAPI_FB, params={"url": url}, timeout=180).json()
    link = data["url"][0]
    req = requests.get(link, timeout=120)
    file = BytesIO(req.content)
    file.name = "video.mp4"
    print("Facebook")
    return file, link


@Client.on_message(
    filters.regex("http|https") & filters.regex("facebook.|fb.") & filters.incoming
)
def facebook_dl(c, m):
    save(m)
    attrs = Attrs(m)
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
