from pyrogram import Client, filters, enums
import requests
import re
from pytz import timezone
from datetime import datetime
from urllib.parse import quote
from data.secret import collection

t = enums.ChatAction.TYPING


@Client.on_message(filters.command("album"))
def cloud_list(c, m):
  m.reply(f"<a href='{collection}'><b>COLLECTION</b></a>",
          parse_mode=enums.ParseMode.HTML,
          disable_web_page_preview=True)


@Client.on_message(filters.command("upload"))
def upload_file(c, m):
  current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
  formatted = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
  if not m.reply_to_message:
    m.reply('Please reply to a message containing a file to upload.')
    return
  words = f"date: {formatted}"
  file_id = None
  file_name = words
  headers = {'Content-type': 'application/octet-stream'}

  if m.reply_to_message.document:
    file_id = m.reply_to_message.document.file_id
  elif m.reply_to_message.photo:
    file_id = m.reply_to_message.photo.file_id
    file_name = f"image {words}.jpg"
    headers = {'Content-type': 'image/jpeg'}
  elif m.reply_to_message.video:
    file_id = m.reply_to_message.video.file_id
    file_name = f"video {words}.mp4"
    headers = {'Content-type': 'video/mp4'}
  elif m.reply_to_message.voice:
    file_id = m.reply_to_message.voice.file_id
    file_name = f"audio {words}.ogg"
    headers = {'Content-type': 'audio/ogg'}
  elif m.reply_to_message.audio:
    file_id = m.reply_to_message.audio.file_id
    file_name = f"music {words}.mp3"
    headers = {'Content-type': 'audio/mpeg'}
  if not file_id:
    m.reply('Vui lòng phản hồi lại tin nhắn chứa tệp.')
    return
  set_filename = re.search(r'\?(.*)', m.text)
  if set_filename:
    file_name = set_filename.group(1)
  file_data = c.stream_media(file_id)
  m.reply_chat_action(t)
  response = requests.put(f"{collection}/{quote(file_name)}",
                          data=file_data,
                          headers=headers)
  print(response.text)
  file_url = f"{collection}/{file_name}"
  m.reply(f"`Result:` \n{quote(file_url, safe=':/')}")
  