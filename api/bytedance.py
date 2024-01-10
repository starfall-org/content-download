import requests, logging
from data.secret import dapi
from io import BytesIO


def TDDL(url):
  data = requests.get(f"{dapi}/tikdou",
                      params={
                          "url": url
                      },
                      timeout=60).json()
  music = None
  if data['is_video'] == True:
    content = requests.get(data["url"]).content
    file = BytesIO(content)
    file.name = "video.mp4"
    is_video = True
  else:
    file = data["url"]
    music_url = data["music"]
    is_video = False
    if music_url:
        music_data = requests.get(music_url).content
        music = BytesIO(content)
        music.name = "music.mp3"
  logging.critical("TikTok/Douyin")
  return file, data["url"], is_video, music
