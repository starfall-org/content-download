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
        music(m, Attrs(m))
        try:
            m.delete()
        except Exception as e:
            raise Exception(e)
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)

@Client.on_message((((filters.regex("http|https") & filters.regex("youtube.|youtu.be")) & filter_on) | filters.command('youtube')) & filters.incoming & channel_post)
def youtube_download(c, m):
    save(m)
    try:
        youtube(m, Attrs(m))
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)
    try:
        m.delete()
    except Exception as e:
        logging.critical(e)
    
@Client.on_message((((filters.regex("http|https") & filters.regex("facebook.|fb.")) & filter_on) | filters.command('facebook')) & filters.incoming & channel_post)
def facebook_download(c, m):
    save(m)
    try:
        facebook(m, Attrs(m))
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)
    try:
        m.delete()
    except Exception as e:
        logging.critical(e)
    
@Client.on_message((((filters.regex("http|https") & filters.regex("instagram.")) & filter_on) | filters.command('instagram')) & filters.incoming & channel_post)
def instagram_download(c, m):
    save(m)
    try:
        instagram(m, Attrs(m))
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)
    try:
        m.delete()
    except Exception as e:
        logging.critical(e)
    
@Client.on_message((((filters.regex("http|https") & filters.regex("tiktok.|douyin.")) & filter_on) | filters.command('facebook')) & filters.incoming & channel_post)
def tiktokdouyin_download(c, m):
    save(m)
    try:
        tiktokdouyin(m, Attrs(m))
    except Exception as e:
        m.reply_chat_action(typing)
        m.reply("__--**resource unavailable**--__", quote=True)
        logging.critical(e)
    try:
        m.delete()
    except Exception as e:
        logging.critical(e)
   
@Client.on_message(((filters.regex("http://|https://") & filter_on) | filters.command('download')) & filters.incoming & channel_post)
def other_download(c, m):
    try:
        other(m, Attrs(m))
        save(m)
    except Exception:
        pass
        