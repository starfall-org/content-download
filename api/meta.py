import requests, random, os
from io import BytesIO
from init import dapi, proxy

def FBDL(url):
    data = requests.get(f"{dapi}/facebook", params={"url":url}, timeout=180).json()
    files = []
    links = data["url"]
    for link in data["url"]:
        content = requests.get(link).content
        file = BytesIO(content)
        file.name = "video.mp4"
        files.append(file)
    os.system("echo Facebook")
    return files, links


def IGDL(url):
    data = requests.get(f"{dapi}/instagram", params={"url":url}, timeout=180).json()
    files = []
    links = data["url"]
    if data.get("is_video", True):
        is_video = True
        for link in data["url"]:
            content = requests.get(link, proxies=proxy).content
            file = BytesIO(content)
            file.name = "instagram.mp4"
            files.append(file)
    else:
        files = data["url"]
        is_video = False
        os.system("echo Instagram")
    return (files, links), is_video
