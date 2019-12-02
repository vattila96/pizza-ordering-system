#!/bin/sh

cp ./payment-server/.env.example ./payment-server/.env
docker pull postgres:latest
docker pull node:13.1.0-alpine3.10
docker-compose -f ./container/docker-compose.yml build payment-server
cd container
docker build . -t pizza-django
