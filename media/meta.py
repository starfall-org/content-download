from api import FBDL, IGDL
from ext import Attrs, Actions,send_videos, send_photos
from pyrogram.enums import ChatAction

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sp = ChatAction.UPLOAD_PHOTO

def facebook(m):
    url = Attrs(m).url
    button = Attrs(m).button
    caption = Attrs(m).caption
    m.reply_chat_action(rv)
    files = FBDL(url)
    m.reply_chat_action(sv)
    if not isinstance(files, list):
        m.reply_video(files, caption=caption, reply_markup=button)
    else:
        for file in files:
            m.reply_chat_action(sv)
            m.reply_video(file, caption=caption, reply_markup=button)

def instagram(m):
    url = Attrs(m).url
    button = Attrs(m).button
    caption = Attrs(m).caption
    m.reply_chat_action(rv)
    files, is_video = IGDL(url)
    if is_video == False:
        send_photos(m, files, button, caption)
    elif is_video == True:
        send_videos(m, files, button, caption)