import requests, random, os
from secret import api_url
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
  os.system("echo Facebook")
  return files


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
  os.system("echo Instagram")
  return files, is_video
  