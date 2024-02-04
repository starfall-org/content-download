from api import FBDL, IGDL
from ext import send_videos, send_photos
from hydrogram.enums import ChatAction
import logging
import os

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sp = ChatAction.UPLOAD_PHOTO

def facebook(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(rv)
        files, links = FBDL(url)
        m.reply_chat_action(sv)
        try:
            m.reply_video(links, caption=caption, reply_markup=button)
        except Exception:
            m.reply_video(files, caption=caption, reply_markup=button)
        os.system("echo Completed")
    except Exception as e:
        logging.error(e)
        raise Exception(e)

def instagram(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(rv)
        links, files, is_video = IGDL(url)
        if not is_video:
            send_photos(m, links, button, caption)
        elif is_video:
            try:
                send_videos(m, links, button, caption)
            except Exception:
                send_videos(m, files, button, caption)
        print("Completed")
    except Exception as e:
        logging.error(e)
        raise Exception(e)