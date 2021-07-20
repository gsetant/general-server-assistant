# Self host general-server-assistant with Docker

## install
- install Docker and Docker compose on your server
- Download the docker-compose.yml file (This version only contains Gsetant, you need to install plugins manually)
`
wget https://raw.githubusercontent.com/gsetant/general-server-assistant/master/docker/docker-compose.yml
`

- If you wish to install Gsetant with all official plugins please download this docker-compose.yml file 
`
wget https://raw.githubusercontent.com/gsetant/general-server-assistant/master/docker/aio/docker-compose.yml
`
- run docker with docker-comppse

`
docker-compose up -d
`

access through ip:9999 default username:admin password:admin

## update
`docker-compose pull`

`docker-compose up -d`
