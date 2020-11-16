#!/bin/bash
app="deplacement-bot-lu"
sudo docker stop ${app}
sudo docker rm ${app}
docker build -f Dockerfile_lu -t ${app} .
docker run --name=${app} \
  -v $PWD:/bot --restart=unless-stopped -d ${app}
sudo docker network connect pi ${app}
docker restart ${app}
