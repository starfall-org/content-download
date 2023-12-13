import requests, random, logging
from utils.secret import api_url
from io import BytesIO


def IGDL(url):
  data = requests.get(f"{api_url}/instagram", params={
      "url": url
  }, timeout=60).json()
  files = []
  if data.get("video", True):
    is_video = True
    for link in data["url"]:
      content = requests.get(link).content
      file = BytesIO(content)
      file.name = f"file{random.randint(1, 9999)}.mp4"
      files.append(file)
  else:
    files = data["url"]
    is_video = False
  logging.critical("Instagram")
  return files, is_video
