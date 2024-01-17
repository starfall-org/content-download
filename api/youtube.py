import requests, random
from data.secret import dapi
from io import BytesIO
from ext.var import image_formats, video_formats, audio_formats, skip_formats


class YTDL:
    def __init__(self, url):
        self.url
    def get(self):
        data = requests.get(f"{dapi}/youtube", params={"url":self.url}, timeout=60).json()
        content = requests.get(data["url"]).content
        file = BytesIO(content)
        file.name = f"video.mp4"
        return file
    def music(self):
        data = requests.get(f"{dapi}/music", params={"url":self.url}, timeout=60).json()
        content = requests.get(data["url"]).content
        file = BytesIO(content)
        file.name = f"music.mp3"
        return file
    
    
    def other(self):
        data = requests.get(f"{dapi}/other", params={"url": self.url}, timeout=60).json()
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
            if r.headers["Content-Type"] in skip_formats:
                return None, None
            else:
                type = "other"
        return file, type
