FROM nikolaik/python-nodejs

RUN apt -y update \ 
    && apt install snapd -y \
    && snap install core \
    && snap install chromium
# set display port to avoid crash
ENV DISPLAY=:99

RUN useradd -ms /bin/bash gstant
WORKDIR  /home/gstant
RUN git clone --depth=1 https://github.com/gsetant/general-server-assistant/
WORKDIR  /home/gstant/general-server-assistant/front-end
RUN npm install 
RUN npm run build:prod
WORKDIR /home/gstant/general-server-assistant
CMD sh docker/start.sh
