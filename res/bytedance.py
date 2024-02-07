from hydrogram.enums import ChatAction
from ext import send_photos, upload
from io import BytesIO
from data import dapi
from .tiktokuser import TikTokUser
import requests, logging, os

def TDDL(url):
    data = requests.get(f"{dapi}/tikdou", params={"url": url}, timeout=180).json()
    link = data["url"]
    if data['is_video']:
        try:
            content = requests.get(link).content
            file = BytesIO(content)
            file.name = "tiktokdouyin.mp4"
        except Exception as e:
            file = None
            logging.critical(e)
        is_video = True
    else:
        file = []
        for photo_link in link:
            try:
                photo_data = requests.get(photo_link).content
                photo_file = BytesIO(photo_data)
                photo_file.name = "photo.jpg"
            except Exception as e:
                logging.critical(e)
                continue
            file.append(photo_file)
        is_video = False
    if data["music"]:
        musiclink = data["music"]
        try:
            music_data = requests.get(musiclink).content
            musicfile = BytesIO(music_data)
            musicfile.name = "music.mp3"
        except Exception as e:
            logging.critical(e)
            musiclink = None
            musicfile = None
    else:
        musiclink = None
        musicfile = None
    os.system("echo TikTok/Douyin")
    return (link, file), (musiclink, musicfile), is_video

def tiktokdouyin(m, attrs):
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
        logging.critical(e)