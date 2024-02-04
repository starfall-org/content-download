import requests, random
from data import dapi
from io import BytesIO
from ext import Formats
import re, logging


def YTDL(url):
    data = requests.get(f"{dapi}/youtube", params={"url":url}, timeout=60).json()
    try:
        content = requests.get(data["url"]).content
        file = BytesIO(content)
        file.name = "video.mp4"
    except Exception as e:
        logging.critical(e)
        file = data["url"]
    return file
    
def YTM(url):
    data = requests.get(f"{dapi}/music", params={"url":url}, timeout=60).json()
    content = requests.get(data["url"]).content
    file = BytesIO(content)
    file.name = "music.mp3"
    return file

def ODL(url):
    data = requests.get(f"{dapi}/other", params={"url": url}, timeout=60).json()
    r = requests.get(data["url"])
    content = r.content
    try:
        header = r.headers['Content-Disposition']
        filename = re.findall("filename=(.+)", header)[0]
    except Exception:
        filename = f"{random.randint(1000,9000)}"
        if r.headers["Content-Type"] in Formats().audio:
            filename = f"{filename}.mp3"
            type = "audio"
            file = BytesIO(content)
            file.name = filename
        if r.headers["Content-Type"] in Formats().image:
            type = "image"
        elif r.headers["Content-Type"] in Formats().video:
            type = "video"
        if r.headers["Content-Type"] in Formats().skip:
            return None, None
        else:
            type = "other"
    return file, type
