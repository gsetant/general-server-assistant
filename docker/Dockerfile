FROM nikolaik/python-nodejs

RUN apt update \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install ./google-chrome-stable_current_amd64.deb

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
