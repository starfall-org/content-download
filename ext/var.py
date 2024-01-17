#
#
class Formats:
    def __init__(self):
        self.image = [
            "image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp",
            "image/svg+xml", "image/bmp"]

        self.video = [
            "video/mp4", "video/webm", "video/ogg", "video/avi", "video/mov",
            "video/mpeg", "video/x-flv", "video/3gpp", "video/h261", "video/h263"]

        self.audio = [
            "audio/mpeg", "audio/ogg", "audio/aac", "audio/midi", "audio/wav",
            "audio/webm", "audio/mp3"]

        self.skip = [
           "application/json", "text/plain", "text/plain; charset=utf-8",
           "text/html; charset=UTF-8"]
