FROM gstant/base

RUN useradd -ms /bin/bash gstant
WORKDIR  /home/gstant
RUN git clone --depth=1 https://github.com/gsetant/general-server-assistant/
WORKDIR  /home/gstant/general-server-assistant/front-end
RUN npm install 
RUN npm run build:prod
WORKDIR /home/gstant/general-server-assistant
CMD sh docker/start.sh
