import requests, random, os
from data.secret import dapi
from io import BytesIO

class FBDL:
    def __init__(self, url):
        self.url = url
        self.fb = requests.get(f"{dapi}/facebook", params={"url": self.url}, timeout=60).json()
    def get(self):
        files = []
        for link in self.fb["url"]:
            content = requests.get(link).content
            file = BytesIO(content)
            file.name = f"file{random.randint(1, 9999)}.mp4"
            files.append(file)
        os.system("echo Facebook")
        return files


class IGDL:
    def __init__(self, url):
        self.url = url
        self.ig = requests.get(f"{dapi}/instagram", params={"url":url}, timeout=60).json()
    def get(self):
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
  