#!/bin/env bash

chmod +x ./main.py
./main.py &
gunicorn --log-level critical -b 0.0.0.0:8080 application.flask:app &

sleep 5
while true; do
  gmt7_time=$(TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%d %H:%M:%S")
  echo "$gmt7_time"
  sleep 86400
done