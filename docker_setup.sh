#!/bin/bash
source .env
docker stop group6_cloud
docker kill group6_cloud
docker rm group6_cloud
docker rmi rvwani
echo "Removing dangling images..."
docker images -qf dangling=true | xargs docker rmi
docker build --rm -f Dockerfile -t ronakwani/rvwani:latest . 2>&1 | tee build1.txt
docker login
docker push ronakwani/rvwani:latest
docker run --name group6_cloud -d -p 127.0.0.1:8010:8010 --env GEMINI_API_KEY=$GEMINI_API_KEY ronakwani/rvwani:latest
