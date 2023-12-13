import requests, random, logging
from utils.secret import api_url
from io import BytesIO

def YTDL(url):
  data = requests.get(f"{api_url}/youtube", params={
    "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"file{random.randint(1, 9999)}.mp4"
  return file
