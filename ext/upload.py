from datetime import datetime
from pytz import timezone
from threading import Thread
from init import collection, deta_web
from urllib.parse import quote
import requests
import logging
import os

def upload(file_data, file_link):
    current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    file_name = f"video {formatted_time}.mp4"
    Thread(target=upload_file, args=(file_data, file_name,)).start()
    Thread(target=upload_web, args=(file_data, file_name,)).start()
    Thread(target=youtube_upload, args=(file_link,)).start()

def upload_file(file_data, file_name):
    raw_bytes = file_data.getvalue()
    response = requests.post(f"{collection}/{file_name}",
                          data=raw_bytes)
    os.system(f'echo "{response.text}"')
    
def upload_web(file_data, file_name):
    base = deta_web.Base("files")
    drive = deta_web.Drive("files")
    file_data = file_data.getvalue()
    base.put({"key": file_name, "name": file_name})
    drive.put(name=file_name, data=file_data)
    return f"https://dash.serv00.net/play/{quote(file_name)}"

def youtube_upload(url, title="TikTok & Douyin", des="Welcome to my channel!"):
    current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    des = f"{title} - {formatted_time}\n\n{des}"
    r = requests.post("https://eohejw5exru9jhs.m.pipedream.net", json={"url":url, "title":title, "des": des})
    print(r.text)