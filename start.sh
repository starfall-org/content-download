#!/bin/bash

python main.py runserver &
gunicorn --log-level critical --bind 0.0.0.0:8080 webpage.flask:app &

sleep 10 

while true; do
  echo "Content Download"
  sleep 169200
done