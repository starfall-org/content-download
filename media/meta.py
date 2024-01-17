from pyrogram.types import InputMediais_video
from api import FBDL, IGDL
from ext import Attrs, Actions,send_videos, send_photos

ris_video = Actions().record_video
upis_video = Actions().upload_video

def facebook(c, m):
    url = Attrs(m).url
    button = Attrs(m).button
    caption = Attrs(m).caption
    m.reply_chat_action(ris_video)
    files = FBDL(url)
    m.reply_chat_action(upis_video)
    if not isinstance(files, list):
        m.reply_is_video(files, caption=caption, reply_markup=button)
    else:
        for file in files:
            m.reply_is_video(file, caption=caption, reply_markup=button)

def instagram(c, m):
    url = Attrs(m).url
    button = Attrs(m).button
    caption = Attrs(m).caption
    m.reply_chat_action(ris_video)
    files, is_video = IGDL(url)
    if is_video == False:
        send_photos(m, files, button, caption)
    elif is_video == True:
        send_is_videos(m, files, button, caption)