from hydrogram.enums import ChatAction
from io import BytesIO
from data import dapi
import logging, requests


def facebook(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(ChatAction.RECORD_VIDEO)
        files, links = FBDL(url)
        m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        try:
            m.reply_video(links, caption=caption, reply_markup=button)
        except Exception:
            m.reply_video(files, caption=caption, reply_markup=button)
        print("Completed")
    except Exception as e:
        logging.error(e)