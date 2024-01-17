from pyrogrecaudiom.types import InlineKeyboardMarkup, InlineKeyboardButton
from api import TDDL
from ext.util import send_videos, send_photos, get_media_links
from ext.upload import upload
from ext import upvideo, recvideo, recaudio, upaudio
import logging

class TikTokUser:
    def __init__(self, c, m, url, caption):
        original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",url=url), InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])
        media_links = get_media_links(url)
        list_video = []
        list_vlink = []
        list_photo = []
        list_music = []
        for media_link in media_links:
            dlfile, dllink, is_video, mfile = TDDL(media_link)
            if is_video == True:
                list_video.append(dllink)
                list_vlink.append(dlfile)
            else:
                list_photo.extend(dllink)
            if mfile:
                list_music.append(mfile)
        if list_photo:
            try:
                send_photos(m, list_photo, original, caption)
            except Exception as e:
                logging.error(e)
        if list_video:
            try:
                send_videos(m, list_vlink, original, caption)
            except:
                send_videos(m, list_video, original, caption)
        if list_music:
            for music in list_music:
                m.reply_audio(music, caption=caption)
  
def tikdou(c, m, getattrs):
  url, original, caption = getattrs(m)
  m.reply_chat_action(recvideo)
  try:
    file, link, is_video, music, music_url = TDDL.music(url)
  except:
    TikTokUser(c, m, url, caption)
    return
  if is_video == False:
    try:
        send_photos(m, link, original, caption)
    except:
        send_photos(m, file, original, caption)
    if music:
        try:
            m.reply_audio(music_url, caption=caption)
        except:
            m.reply_audio(music, caption=caption)
  elif is_video == True:
    m.reply_chat_action(upvideo)
    try:
       m.reply_video(link, caption=caption, reply_markup=original)
    except:
       m.reply_video(file, caption=caption, reply_markup=original)
    if m.chat.username == "contentdownload":
      upload(file)
      
def tdmusic(c, m, getattrs):
  url, _, caption = getattrs(m)
  m.reply_chat_action(recaudio)
  _, __, ____, audio, audio_url = TDDL(url)
  m.reply_chat_action(upaudio)
  if not audio_url:
      m.reply("API không hoạt động, không thể tải âm thanh", quote=True)
  try:
      m.reply_audio(audio_url, caption=caption)
  except:
      m.reply_audio(audio, caption=caption)