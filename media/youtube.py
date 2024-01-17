from api import YTDL,YTM, ODL
from pyrogram.enums import ChatAction
import os

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sp = ChatAction.UPLOAD_PHOTO
sa = ChatAction.UPLOAD_AUDIO
sd = ChatAction.UPLOAD_DOCUMENT

def youtube(m, attrs):
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(rv)
    file = YTDL(url)
    m.reply_chat_action(sv)
    m.reply_video(file, caption=caption, reply_markup=button)
    
def other(m, file, types, attrs):
    button = attrs.button
    caption = attrs.caption
    if types == "image":
        m.reply_chat_action(sp)
        m.reply_photo(file, caption=caption, reply_markup=button)
    elif types == "video":
        m.reply_chat_action(sv)
        m.reply_video(file, caption=caption, reply_markup=button)
    elif types == "audio":
        m.reply_chat_action(sa)
        m.reply_audio(file, caption=caption)
    else:
        m.reply_chat_action(sd)
        m.reply_document(file, reply_markup=button, caption=caption)

def music(m, attrs):
    url = attrs.url
    caption = attrs.caption
    m.reply_chat_action(ra)
    audio = YTM(url)
    m.reply_chat_action(sa)
    m.reply_audio(audio, caption=caption)