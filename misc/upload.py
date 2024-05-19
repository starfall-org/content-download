import requests
from datetime import datetime
from threading import Thread
from urllib.parse import quote
from pytz import timezone
from deta import Deta
from data import COLLECTON, WEB_COLLECTION

deta = Deta(WEB_COLLECTION)


def upload(file_data, file_link):
    current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    file_name = f"video {formatted_time}.mp4"
    Thread(
        target=upload_file,
        args=(
            file_data,
            file_name,
        ),
    ).start()
    Thread(
        target=upload_web,
        args=(
            file_data,
            file_name,
        ),
    ).start()
    Thread(target=youtube_upload, args=(file_link,)).start()


def upload_file(file_data, file_name):
    raw_bytes = file_data.getvalue()
    response = requests.post(f"{COLLECTON}/s3/upload/{file_name}", data=raw_bytes)
    print(response.text)


def upload_web(file_data, file_name):
    base = deta.Base("files")
    drive = deta.Drive("files")
    file_data = file_data.getvalue()
    base.put({"key": file_name, "name": file_name})
    drive.put(name=file_name, data=file_data)
    return f"{COLLECTON}/play/{quote(file_name)}"


def youtube_upload(url, title="TikTok & Douyin", des="Welcome to my channel!"):
    current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    des = f"{title} - {formatted_time}\n\n{des}"
    r = requests.post(
        "https://eohejw5exru9jhs.m.pipedream.net",
        json={"url": url, "title": title, "des": des},
    )
    print(r.text)
