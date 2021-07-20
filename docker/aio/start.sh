#!/bin/bash
if [ -f "/home/gstant/general-server-assistant/config/appConfig.json" ];then
  echo "using user appConfig"
else
  echo "copy default appConfig"
  cp /home/gstant/general-server-assistant/docker/appConfig.json /home/gstant/general-server-assistant/config/appConfig.json
fi

if [ -f "/home/gstant/general-server-assistant/config/requirements.json" ];then
  echo "using user requirements"
else
  echo "copy default requirements"
  cp /home/gstant/general-server-assistant/docker/requirements.json /home/gstant/general-server-assistant/config/requirements.json
fi


if [ -f "/home/gstant/general-server-assistant/app/plugins/__init__.py" ];then
  echo "have __init__.py"
else
  echo "generate __init__.py"
  touch /home/gstant/general-server-assistant/app/plugins/__init__.py
fi
nohup node NeteaseCloudMusicApi/app.js &
python3 main.py
