import requests
from datetime import datetime
from threading import Thread
from pytz import timezone


def upload(file_data, file_link):
    current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    des = f"Uploaded at {formatted_time}"
    Thread(target=youtube_upload, args=(file_link,)).start()
    return {"status": "success", "description": des}


def youtube_upload(url, title="TikTok & Douyin", des="Welcome to my channel!"):
    current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    des = f"{title} - {formatted_time}\n\n{des}"
    r = requests.post(
        "https://eohejw5exru9jhs.m.pipedream.net",
        json={"url": url, "title": title, "des": des},
        timeout=999,
    )
    print(r.text)
