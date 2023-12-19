import requests
import logging
from datetime import datetime
from pytz import timezone
from secret import upload_app


def upload_file(file_data):
  raw_bytes = file_data.getvalue()
  current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
  formatted_time = current_time.strftime("%H:%M:%S(%d-%B-%Y)")

  file_name = f"video {formatted_time}.mp4"
  headers = {'Content-type': 'video/mp4'}

  response = requests.put(f"{upload_app}/{file_name}",
                          data=raw_bytes,
                          headers=headers)
  logging.critical(response.text)
