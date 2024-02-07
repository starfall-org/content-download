from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction
from api import TDDL
from ext import send_videos, send_photos, get_media_links
from ext import upload
from .tiktokuser import TikTokUser
import logging
import os

def tikdou(m, attrs):
    try:
        url = attrs.url
        button = attrs.button
        caption = attrs.caption
        m.reply_chat_action(ChatAction.RECORD_VIDEO)
        try:
            media, music, is_video = TDDL(url)
        except Exception as e:
            logging.critical(e)
            TikTokUser(m, url, caption, TDDL)
            return
        if not is_video:
            try:
                send_photos(m, media[0], button, caption)
            except Exception as e:
                logging.critical(e)
                send_photos(m, media[1], button, caption)
            if music[0]:
                m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
                try:
                    m.reply_audio(music[0], caption=caption)
                except Exception as e:
                    logging.critical(e)
                    m.reply_audio(music[1], caption=caption)
        else:
            m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                m.reply_video(media[0], caption=caption, reply_markup=button)
            except Exception as e:
                logging.critical(e)
                m.reply_video(media[1], caption=caption, reply_markup=button)
        if m.chat.username == "contentdownload":
            try:
                upload(media[1], media[0])
            except Exception as e:
                logging.critical(e)
        return
    except Exception as e:
        raise Exception(e)
      
def tdmusic(m, attrs):
    try:
        url = attrs.url
        caption = attrs.caption
        m.reply_chat_action(ChatAction.RECORD_AUDIO)
        _, audio, __ = TDDL(url)
        m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
        if not audio:
            raise Exception("API error")
        try:
            m.reply_audio(audio[0], caption=caption)
        except Exception:
            m.reply_audio(audio[1], caption=caption)
        print("Completed")
        return
    except Exception as e:
        raise Exception(e)