from datetime import datetime
from pytz import timezone
from threading import Thread
import collection
import requests
import logging
import os

def upload(file_data):
    current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
    formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")
    file_name = f"video {formatted_time}.mp4"
    Thread(target=upload_file, args=(file_data, file_name,)).start()

def upload_file(file_data, file_name):
    raw_bytes = file_data.getvalue()
    response = requests.post(f"{collection}/{file_name}",
                          data=raw_bytes)
    os.system(f"echo {response.text}")
