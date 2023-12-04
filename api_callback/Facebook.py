import requests, random, logging
from utils.variables import api_url
from io import BytesIO

def FBDL(url):
  data = requests.get(f"{api_url}/facebook", params={
    "url": url
  }, timeout=60).json()
  files = []
  for link in data["url"]:
    content = requests.get(link).content
    file = BytesIO(content)
    file.name = f"file{random.randint(1, 9999)}.mp4"
    files.append(file)
  logging.critical("Facebook")
  return files
