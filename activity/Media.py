from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction
from hydrogram import Client, filters
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
            raise Exception(e)
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("**Error:** __resource not found__", quote=True)
        logging.critical(e)

@Client.on_message((filters.regex("http://|https://") | filters.command('download')) & filters.incoming & channel_post)
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
                m.reply("**Error:** __resource not found__", quote=True)
                logging.critical(e)
        else:
            try:
                file, types = ODL(url)
                if file:
                    save(m)
                    other(m, file, types,  attrs)
            except Exception as e:
                logging.critical(e)