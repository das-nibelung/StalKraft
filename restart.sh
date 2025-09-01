#!/bin/bash
export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true
docker compose -f ~/StalKraftProject/docker-compose.dev.yml down 
docker volume rm stalkraftproject_static_files
docker compose -f ~/StalKraftProject/docker-compose.dev.yml build
docker compose -f ~/StalKraftProject/docker-compose.dev.yml up -d
