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

python3 main.py
