#!/usr/bin/bash

curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/7616fc22-317d-43cf-bf87-4a51d4f339b6/cert'

chmod +x ./main.py ./lite

gunicorn --log-level critical -b 0.0.0.0:8080 application:app &
./main.py

sleep 5
while true; do
  gmt7_time=$(TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%d %H:%M:%S")
  echo "$gmt7_time"
  sleep 86400
done