import requests, random, logging
from data.secret import dapi
from io import BytesIO


def TDDL(url):
  data = requests.get(f"{dapi}/tiktokdouyin",
                      params={
                          "url": url
                      },
                      timeout=60).json()
  if data['video'] == True:
    content = requests.get(data["url"]).content
    file = BytesIO(content)
    file.name = f"file{random.randint(1, 9999)}.mp4"
  else:
    file = data["url"]
  logging.critical("TikTok/Douyin")
  return file, data["url"], data["video"]
