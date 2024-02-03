import requests, random, os
from io import BytesIO
from data import dapi

def FBDL(url):
    data = requests.get(f"{dapi}/facebook", params={"url":url}, timeout=180).json()
    link = data["url"][0]
    req = requests.get(link)
    file = BytesIO(req.content)
    file.name = "video.mp4"
    print("Facebook")
    return file, link


def IGDL(url):
    data = requests.get(f"{dapi}/instagram", params={"url":url}, timeout=180).json()
    files = []
    links = data["url"]
    is_video = data["is_video"]
    if is_video:
        for link in data["url"]:
            content = requests.get(link).content
            file = BytesIO(content)
            file.name = "instagram.mp4"
            files.append(file)
    else:
        files = data["url"]
        print("Instagram")
    return [files, links], is_video
