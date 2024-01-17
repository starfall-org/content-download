import requests, random, os
from io import BytesIO
from init import dapi

class FBDL:
    def __init__(self, url):
        data = requests.get(f"{dapi}/facebook", params={"url":url}, timeout=60).json()
        files = []
        for link in data["url"]:
            content = requests.get(link).content
            file = BytesIO(content)
            file.name = f"file{random.randint(1, 9999)}.mp4"
            files.append(file)
        os.system("echo Facebook")
        return files


class IGDL:
    def __init__(self, url):
        data = requests.get(f"{dapi}/instagram", params={"url":url}, timeout=60).json()
        files = []
        if data.get("is_video", True):
            is_video = True
            for link in data["url"]:
                content = requests.get(link).content
                file = BytesIO(content)
                file.name = f"instagram.mp4"
                files.append(file)
        else:
            files = data["url"]
            is_video = False
            os.system("echo Instagram")
        return files, is_video
  