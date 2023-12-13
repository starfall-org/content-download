import requests, random, re, logging
from utils.secret import api_url
from io import BytesIO

def YTM(url):
  data = requests.get(f"{api_url}/music", params={
    "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"audio{random.randint(1, 9999)}.mp3"
  return file
