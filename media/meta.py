from pyrogram.types import InputMediaVideo
from api import FBDL, IGDL
from ext import Attrs, Actions,send_videos, send_photos

rvideo = Actions().record_video
upvideo = Actions().upload_video

def facebook(c, m, getattrs):
    url, original, caption = getattrs(m)
    m.reply_chat_action(rvideo)
    files = FBDL(url)
    m.reply_chat_action(upvideo)
    if not isinstance(files, list):
         m.reply_video(files, caption=caption, reply_markup=original)
    else:
        for file in files:
             m.reply_video(file, caption=caption, reply_markup=original)

def instagram(c, m, getattrs):
    url, original, caption = getattrs(m)
    m.reply_chat_action(rvideo)
    files, video = IGDL(url)
    if video == False:
        send_photos(m, files, original, caption)
    elif video == True:
        send_videos(m, files, original, caption)