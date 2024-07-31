#!/usr/bin/bash

gunicorn --log-level critical -b 0.0.0.0:8080 helloworld:app &
cd src && python -u application.py