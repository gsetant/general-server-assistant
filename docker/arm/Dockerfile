FROM arm64v8/debian
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get -y update \
    && apt-get install -y chromium git chromium-driver python3 python3-pip nodejs npm python

# set display port to avoid crash
ENV DISPLAY=:99


RUN useradd -ms /bin/bash gstant
WORKDIR  /home/gstant
RUN git clone --depth=1 https://github.com/gsetant/general-server-assistant/
WORKDIR  /home/gstant/general-server-assistant/front-end
RUN npm install npm -g
RUN npm install 
RUN npm run build:prod
WORKDIR /home/gstant/general-server-assistant
RUN apt-get install  -y python-dev python3-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev
CMD sh docker/start.sh
