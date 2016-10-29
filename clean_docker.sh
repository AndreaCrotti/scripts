#!/usr/bin/env bash

# clean exited containers, dangling images and unwanted volumes

docker rm -v $(docker ps -a -q -f status=exited)
docker rm -v $(docker ps -a -q -f status=dead)

docker rmi $(docker images -f "dangling=true" -q)

# TODO: this might be a bit more dangerous maybe?
# docker volume rm $(docker volume ls -qf dangling=true)
