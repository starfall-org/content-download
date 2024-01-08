import requests, random
from data.secret import webapi
from io import BytesIO
from ext.var import image_formats, video_formats, audio_formats


def YTDL(url):
  data = requests.get(f"{webapi}/youtube", params={
      "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"file{random.randint(1, 9999)}.mp4"
  return file


def YTM(url):
  data = requests.get(f"{webapi}/music", params={
      "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"audio{random.randint(1, 9999)}.mp3"
  return file


def ODL(url):
  data = requests.get(f"{webapi}/other", params={
      "url": url
  }, timeout=60).json()
  r = requests.get(data["url"])
  content = r.content
  try:
    header = r.headers['Content-Disposition']
    filename = re.findall("filename=(.+)", header)[0]
  except:
    filename = f"file{random.randint(1000,9000)}"
    if r.headers["Content-Type"] in audio_formats:
      filename = f"file{random.randint(1000,9000)}.mp3"
  file = BytesIO(content)
  file.name = filename
  if r.headers["Content-Type"] in image_formats:
    type = "image"
  elif r.headers["Content-Type"] in video_formats:
    type = "video"
  elif r.headers["Content-Type"] in audio_formats:
    type = "audio"
  else:
    return None, None
  return file, type
