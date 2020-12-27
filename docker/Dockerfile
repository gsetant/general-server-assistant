FROM nikolaik/python-nodejs

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable git \
    &&  apt-get install -yqq unzip \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \

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
