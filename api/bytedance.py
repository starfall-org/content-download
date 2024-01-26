from io import BytesIO
from init import dapi
from ext import request_get
import requests
import os

def TDDL(url):
    data = requests.get(f"{dapi}/tikdou", params={"url": url}, timeout=180).json()
    music = None
    link = data["url"]
    if data['is_video']:
        content = request_get(link)
        file = BytesIO(content)
        file.name = "tiktokdouyin.mp4"
        is_video = True
    else:
        file = []
        for photo_link in link:
            photo_data = request_get(photo_link)
            photo_file = BytesIO(photo_data)
            photo_file.name = "photo.jpg"
            file.append(photo_file)
        is_video = False
    if data["music"]:
        musiclink = data["music"]
        try:
            music_data = request_get(musiclink)
            if music_data:
                musicfile = BytesIO(music_data)
                musicfile.name = "music.mp3"
            else:
                musiclink = None
                musicfile = None
    os.system("echo TikTok/Douyin")
    return (link, file), (musiclink, musicfile), is_video