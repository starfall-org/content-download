#!/bin/bash

python main.py runserver &
gunicorn --log-level critical --bind 0.0.0.0:8080 webpage.flask:app &

sleep 10 

while true; do
  current_time=$(date -u +"%Y-%m-%d %H:%M:%S")
  gmt7_time=$(TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%d %H:%M:%S")
  
  echo "Content Download - UTC: $current_time, GMT+7: $gmt7_time"
  
  sleep 169200
done