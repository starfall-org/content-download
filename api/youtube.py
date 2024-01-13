import requests, random
from data.secret import dapi
from io import BytesIO
from ext.var import image_formats, video_formats, audio_formats


def YTDL(url):
  data = requests.get(f"{dapi}/youtube", params={
      "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"file{random.randint(1, 9999)}.mp4"
  return file


def YTM(url):
  data = requests.get(f"{dapi}/music", params={
      "url": url
  }, timeout=60).json()
  content = requests.get(data["url"]).content
  file = BytesIO(content)
  file.name = f"audio{random.randint(1, 9999)}.mp3"
  return file


def ODL(url):
  data = requests.get(f"{dapi}/other", params={
      "url": url
  }, timeout=60).json()
  r = requests.get(data["url"])
  content = r.content
  try:
    header = r.headers['Content-Disposition']
    filename = re.findall("filename=(.+)", header)[0]
  except:
    filename = f"{random.randint(1000,9000)}"
    if r.headers["Content-Type"] in audio_formats:
      filename = f"{filename}.mp3"
      type = "audio"
  file = BytesIO(content)
  file.name = filename
  if r.headers["Content-Type"] in image_formats:
    type = "image"
  elif r.headers["Content-Type"] in video_formats:
    type = "video"
  else:
    type = "other"
  return file, type
