#!/usr/bin/bash

wget -O lite.gz https://github.com/xxf098/LiteSpeedTest/releases/download/v0.15.0/lite-linux-amd64-v0.15.0.gz
gzip -d lite.gz
chmod +x ./main.py ./lite

gunicorn --log-level critical -b 0.0.0.0:8080 application:app &
./main.py

sleep 5
while true; do
  gmt7_time=$(TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%d %H:%M:%S")
  echo "$gmt7_time"
  sleep 86400
done