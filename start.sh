#!/bin/bash
app="deplacement-bot"
sudo docker stop ${app}
sudo docker rm ${app}
docker build -f Dockerfile -t ${app} .
docker run --name=${app} \
  -v $PWD:/bot --restart=unless-stopped -d ${app}
sudo docker network connect pi ${app}
docker restart ${app}
