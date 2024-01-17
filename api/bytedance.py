from io import BytesIO
from init import dapi
import requests
import os

def TDDL(url):
    data = requests.get(f"{dapi}/tikdou", params={"url": url}, timeout=60).json()
    music = None
    if data['is_video'] == True:
        content = requests.get(data["url"]).content
        file = BytesIO(content)
        file.name = "tiktokdouyin.mp4"
        is_video = True
    else:
        file = []
        for photo_url in data["url"]:
            photo_data = requests.get(photo_url).content
            photo_file = BytesIO(photo_data)
            photo_file.name = "photo.jpg"
            file.append(photo_file)
        is_video = False
    if data["music"]:
        music_data = requests.get(data["music"]).content
        music = BytesIO(music_data)
        music.name = "music.mp3"
    os.system("echo TikTok/Douyin")
    return file, music, is_video