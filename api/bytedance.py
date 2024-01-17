import requests, logging
from io import BytesIO
from data.secret import dapi

class TDDL:
    def __init__(self, url):
        self.data = requests.get(f"{dapi}/tikdou", params={"url": url}, timeout=60).json()
    def get(self):
        music = None
        if self.data['is_video'] == True:
            content = requests.get(data["url"]).content
            file = BytesIO(content)
            file.name = "tiktokdouyin.mp4"
            is_video = True
        else:
            file = []
            for photo_url in self.data["url"]:
                photo_data = requests.get(photo_url).content
                photo_file = BytesIO(photo_data)
                photo_file.name = "photo.jpg"
                file.append(photo_file)
            is_video = False
        if self.data["music"]:
            music_data = requests.get(data["music"]).content
            music = BytesIO(music_data)
            music.name = "music.mp3"
        os.system("echo TikTok/Douyin")
        return file, self.data["url"], is_video, music, self.data["music"]
    def music(self):
        if self.data["music"]:
            music_data = requests.get(data["music"]).content
            music = BytesIO(music_data)
            music.name = "music.mp3"
            os.system("echo TikTok Music")
            return music, self.data["music"]