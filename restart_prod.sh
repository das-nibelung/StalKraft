#!/bin/bash
export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true
docker compose -f ~/StalKraftProject/docker-compose.yml down 
docker compose -f ~/StalKraftProject/docker-compose.yml build
docker compose -f ~/StalKraftProject/docker-compose.yml up -d
