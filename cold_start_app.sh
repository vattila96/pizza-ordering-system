#!/bin/sh

cp ./payment-server/.env.example ./payment-server/.env
docker-compose -f container/docker-compose.yml up --build
