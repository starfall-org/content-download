import requests, random, re, logging
from utils.secret import api_url
from utils.var import image_formats, video_formats, audio_formats
from io import BytesIO

def DL(url):
  data = requests.get(f"{api_url}/other", params={
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
    return None, "other"
  return file, type
