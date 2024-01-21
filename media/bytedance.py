from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction
from api import TDDL
from ext import send_videos, send_photos, get_media_links
from ext import upload
import logging
import os

rv = ChatAction.RECORD_VIDEO
ra = ChatAction.RECORD_AUDIO
sv = ChatAction.UPLOAD_VIDEO
sa = ChatAction.UPLOAD_AUDIO

class TikTokUser:
    def __init__(self, m, url, caption):
        button = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        media_links = get_media_links(url)
        list_video = []
        list_photo = []
        list_music = []
        for media_link in media_links:
            media, music, is_video = TDDL(media_link)
            if is_video == True:
                m.reply_chat_action(rv)
                list_video.append(media[1])
            else:
                list_photo.extend(media[0])
            if music:
                m.reply_chat_action(ra)
                list_music.append(music[0])
        if list_photo:
            try:
                send_photos(m, list_photo, button, caption)
            except Exception as e:
                logging.critical(e)
        if list_video:
            try:
                send_videos(m, list_video, button, caption)
            except Exception as e:
                logging.critical(e)
        if list_music:
            for music in list_music:
                m.reply_chat_action(sa)
                try:
                    m.reply_audio(music, caption=caption)
                except Exception as e:
                    logging.critical(e)
        os.system("echo Completed")
  
def tikdou(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(rv)
        try:
            media, music, is_video = TDDL(url)
        except:
            TikTokUser(m, url, caption)
            return
        if is_video == False:
            try:
                send_photos(m, media[0], button, caption)
            except:
                send_photos(m, media[1], button, caption)
            if music[0]:
                m.reply_chat_action(sa)
                try:
                    m.reply_audio(music[0], caption=caption)
                except:
                    m.reply_audio(music[1], caption=caption)
        elif is_video == True:
            m.reply_chat_action(sv)
            try:
                m.reply_video(media[0], caption=caption, reply_markup=button)
            except:
                m.reply_video(media[1], caption=caption, reply_markup=button)
        if m.chat.username == "contentdownload":
            try:
                upload(media[1], media[0])
            except Exception as e:
                logging.critical(e)
        os.system("echo Completed")
        return
    except Exception as e:
        raise Exception(e)
      
def tdmusic(m, attrs):
    try:
        url = attrs.url
        caption = attrs.caption
        m.reply_chat_action(ra)
        _, music, __ = TDDL(url)
        m.reply_chat_action(sa)
        if not audio_url:
            m.reply("API không hoạt động, không thể tải âm thanh", quote=True)
            raise
        try:
            m.reply_audio(audio[0], caption=caption)
        except:
            m.reply_audio(audio[1], caption=caption)
        os.system("echo Completed")
        return
    except Exception as e:
        raise Exception(e)