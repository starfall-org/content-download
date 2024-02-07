from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction
from hydrogram import Client, filters
from res import tiktokdouyin, facebook, instagram, youtube, music, other
from ext import Attrs, save, channel_post, filter_on
import logging
import os

typing = ChatAction.TYPING

@Client.on_message(filters.command("music"))
def music_download(c, m):
    save(m)
    try:
        attrs = Attrs(m)
        music(m, attrs)
        try:
            m.delete()
        except Exception as e:
            raise Exception(e)
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)

@Client.on_message(((filters.regex("http://|https://") & filter_on) | filters.command('download')) & filters.incoming & channel_post)
def all_media_download(c, m):
    attrs = Attrs(m)
    if attrs.url:
        media_group = ["youtube", "youtu.be", "tiktok", "douyin", "iesdouyin", "facebook", "fb.com", "instagram"]
        url = attrs.url
        if any(media in url for media in media_group):
            save(m)
            try:
                if any(reg in url for reg in ["youtube", "youtu.be"]):
                    youtube(m, attrs)
                elif any(reg in url for reg in ["facebook", "fb"]):
                    facebook(m, attrs)
                elif "instagram" in url:
                    instagram(m, attrs)
                else:
                    tikdou(m, attrs)
                m.delete()
            except Exception as e:
                m.reply_chat_action(typing)
                m.reply("__--**resource unavailable**--__", quote=True)
                logging.critical(e)
        else:
            try:
                file, types = ODL(url)
                if file:
                    save(m)
                    other(m, file, types,  attrs)
            except Exception as e:
                logging.critical(e)