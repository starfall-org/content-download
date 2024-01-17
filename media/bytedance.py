from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from api import TDDL
from ext import Attrs, Actions, send_videos, send_photos, get_media_links
from ext.upload import upload
import logging

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sa = ChatAction.UPLOAD_AUDIO

class TikTokUser:
    def __init__(self, c, m, url, caption):
        original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        media_links = get_media_links(url)
        list_video = []
        list_photo = []
        list_music = []
        for media_link in media_links:
            file, music, is_video = TDDL(media_link)
            if is_video == True:
                m.reply_chat_action(rv)
                list_video.append(file)
            else:
                list_photo.extend(file)
            if music:
                m.reply_chat_action(ra)
                list_music.append(music)
        if list_photo:
            try:
                send_photos(m, list_photo, original, caption)
            except Exception as e:
                logging.error(e)
        if list_video:
            send_videos(m, list_video, original, caption)
        if list_music:
            for music in list_music:
                m.reply_chat_action(sa)
                m.reply_audio(music, caption=caption)
  
def tikdou(m, attrs):
    url = attrs.url
    button = attrs.button
    caption = attrs.caption
    m.reply_chat_action(rv)
    try:
        file, music, is_video = TDDL(url)
    except:
        TikTokUser(c, m, url, caption)
        return
    if is_video == False:
        send_photos(m, file, original, caption)
        if music:
            m.reply_chat_action(sa)
            m.reply_audio(music, caption=caption)
    elif is_video == True:
        m.reply_chat_action(sv)
        m.reply_video(file, caption=caption, reply_markup=original)
    if m.chat.username == "contentdownload":
        upload(file)
      
def tdmusic(m, attrs):
    url = attrs.url
    caption = attrs.caption
    m.reply_chat_action(ra)
    _, music, __ = TDDL(url)
    m.reply_chat_action(sa)
    if not audio_url:
        m.reply("API không hoạt động, không thể tải âm thanh", quote=True)
        raise
    m.reply_audio(audio, caption=caption)