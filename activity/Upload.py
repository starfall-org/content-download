from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from pytz import timezone
from datetime import datetime
from urllib.parse import quote
from ext import Attrs
from ext import upload_web
from init import collection
import requests
import re

typing = ChatAction.TYPING

@Client.on_message(filters.command("album"))
def cloud_list(c, m):
    m.reply_chat_action(typing)
    m.reply(f"__--**[COLLECTION]({collection})\n\n[WEB COLLECTION](https://dash.serv00.net/)**--__",
        disable_web_page_preview=True)


@Client.on_message(filters.command("upload"))
def upload_to_cloud(c, m):
    m.reply_chat_action(typing)
    current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    formatted = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    if not m.reply_to_message:
        raise Exception("Please reply to a message containing a file to upload.")
    words = f"date: {formatted}"
    file_id = None
    file_name = words
    headers = {"Content-type": "application/octet-stream"}
    if m.reply_to_message.document:
        file_id = m.reply_to_message.document.file_id
    elif m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        file_name = f"image {words}.jpg"
        headers = {"Content-type": "image/jpeg"}
    elif m.reply_to_message.video:
        file_id = m.reply_to_message.video.file_id
        file_name = f"video {words}.mp4"
        headers = {"Content-type": "video/mp4"}
    elif m.reply_to_message.voice:
        file_id = m.reply_to_message.voice.file_id
        file_name = f"audio {words}.ogg"
        headers = {"Content-type": "audio/ogg"}
    elif m.reply_to_message.audio:
        file_id = m.reply_to_message.audio.file_id
        file_name = f"music {words}.mp3"
        headers = {"Content-type": "audio/mpeg"}
    if not file_id:
        raise Exception("Vui lòng phản hồi lại tin nhắn chứa tệp")
    set_filename = re.search(r"\?(.*)", m.text)
    if set_filename:
        file_name = set_filename.group(1)
    file_data = c.download_media(file_id, in_memory=True)
    m.reply_chat_action(typing)
    file_url = upload_web(file_data, file_name)
    m.reply(f"`Result:` \n{quote(file_url, safe=":/")}")
  
@Client.on_message(filters.command("delete"))
def request_delete_file(c, m):
    m.reply_chat_action(typing)
    if m.reply_to_message:
        url = Attrs(m.reply_to_message).url
    else:
        url = Attrs(m).url
    res = requests.delete(url).text
    m.reply(res)
  