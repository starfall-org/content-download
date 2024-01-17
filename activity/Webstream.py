from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from init import webstream
import logging
import time 
import os

typing = ChatAction.TYPING

@Client.on_message(filters.command("stream"))
def get_webstream(c, m):
    m.reply_chat_action(typing)
    try:
        if m.reply_to_message:
            box = m.reply_to_message.chat.id
            mid = m.reply_to_message.id
            if m.reply_to_message.video:
                file_id = m.reply_to_message.video.file_id
                file_type = "video"
            elif m.reply_to_message.audio:
                file_id = m.reply_to_message.audio.file_id
                file_type = "audio"
            elif m.reply_to_message.photo:
                file_id = m.reply_to_message.photo.file_id
                file_type = "photo"
            else:
                raise Exception("Không phát hiện đối tượng có thể stream, vui lòng cung cấp thêm")
        else:
            box = m.chat.id
            mid = m.id
            if m.video:
                file_id = m.video.file_id
                file_type = "video"
            elif m.audio:
                file_id = m.audio.file_id
                file_type = "audio"
            elif m.photo:
                file_id = m.photo.file_id
                file_type = "photo"
            else:
                raise Exception("Không phát hiện đối tượng có thể stream, vui lòng cung cấp thêm")
            main_stream = f"{webstream}/stream?box={box}&id={mid}"
            m.reply(f"Liên kết Stream:\n{main_stream}", quote=True)
    except Exception as e:
        m.reply(str(e), quote=True)
        logging.critical(e)
  
@Client.on_message(filters.command("setstream"))
def set_webstream(c,m):
    m.reply_chat_action(typing)
    url = m.command[1]
    os.environ["WEBSTREAM"] = url
    st = m.reply(f"Đã cập nhật webstream {url}", quote=True)
    time.sleep(30)
    st.delete()
    m.delete()