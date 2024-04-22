#!/bin/bash

# For using with pm2
source ~/.bashrc
SERVICE_NAME=fact-extractor-backend
pm2 stop $SERVICE_NAME 2> /dev/null || :
pm2 delete $SERVICE_NAME  2> /dev/null || :
pm2 start "gunicorn --bind 0.0.0.0:8000 -w 1 -k uvicorn.workers.UvicornWorker --chdir src main:app" --name $SERVICE_NAME
