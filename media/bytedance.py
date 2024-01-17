from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from api import TDDL
from ext import Attrs, Actions, send_videos, send_photos, get_media_dllinks
from ext.upload import upload
import logging

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sa = ChatAction.UPLOAD_AUDIO

class TikTokUser:
    def __init__(self, c, m, url, caption):
        original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        media_dllinks = get_media_dllinks(url)
        list_video = []
        list_vdllink = []
        list_photo = []
        list_music = []
        for media_dllink in media_dllinks:
            dlfile, dldllink, is_video, mfile = TDDL(media_dllink)
            if is_video == True:
                m.reply_chat_action(rv)
                list_video.append(dldllink)
                list_vdllink.append(dlfile)
            else:
                list_photo.extend(dldllink)
            if mfile:
                m.reply_chat_action(ra)
                list_music.append(mfile)
        if list_photo:
            try:
                send_photos(m, list_photo, original, caption)
            except Exception as e:
                logging.error(e)
        if list_video:
            try:
                send_videos(m, list_vdllink, original, caption)
            except:
                send_videos(m, list_video, original, caption)
        if list_music:
            for music in list_music:
                m.reply_chat_action(sa)
                m.reply_audio(music, caption=caption)
  
def tikdou(c, m):
    url = Attrs(m).url
    button = Attrs(m).button
    caption = Attrs(m).caption
    m.reply_chat_action(rv)
    try:
        file, dllink, is_video, music = TDDL(url)
    except:
        TikTokUser(c, m, url, caption)
        return
    if is_video == False:
        try:
            send_photos(m, dllink, original, caption)
        except:
            send_photos(m, file, original, caption)
    if music:
        m.reply_chat_action(sa)
        m.reply_audio(music, caption=caption)
    elif is_video == True:
        m.reply_chat_action(sv)
        try:
            m.reply_video(dllink, caption=caption, reply_markup=original)
        except:
            m.reply_video(file, caption=caption, reply_markup=original)
    if m.chat.username == "contentdownload":
        upload(file)
      
def tdmusic(c, m, getattrs):
    url = Attrs(m).url
    caption = Attrs(m).caption
    m.reply_chat_action(ra)
    _, __, ____, music = TDDL(url)
    m.reply_chat_action(sa)
    if not audio_url:
        m.reply("API không hoạt động, không thể tải âm thanh", quote=True)
        raise
    m.reply_audio(audio, caption=caption)