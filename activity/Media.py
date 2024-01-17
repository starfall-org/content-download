from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from pyrogram import Client, filters
from media import tikdou, tdmusic, facebook, instagram, youtube, music, other
from api import ODL
from ext import Attrs, save, channel_post
import logging
import os

typing = ChatAction.TYPING

@Client.on_message(filters.command("music") & channel_post)
def music_download(c, m):
    save(m)
    try:
        attrs = Attrs(m)
        if any(match in m.text for match in ["tiktok", "douyin"]):
            tdmusic(m, attrs)
        else:
            music(m, attrs)
        try:
            m.delete()
        except Exception as e:
            logging.error(e)
    except Exception as e:
        logging.error(e)

@Client.on_message((filters.regex("https://|http://")|filters.command('download')) & filters.incoming & channel_post)
def all_media_download(c, m):
    attrs = Attrs(m)
    if attrs.url:
        media_group = ["youtube", "youtu.be", "tiktok", "douyin", "iesdouyin", "facebook", "fb", "instagram"]
        url = attrs.url
        if any(media in url for media in media_group):
            m.reply_chat_action(t)
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
                save(m)
            except Exception as e:
                logging.error(e)
        else:
            try:
                file, types = ODL(url)
                if file:
                    save(m)
                    m.reply_chat_action(typing)
                    other(m, file, types,  attrs)
            except Exception as e:
                logging.error(e)