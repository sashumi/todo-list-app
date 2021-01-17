#!/bin/bash

# Deploy with Docker Compose
docker rm -f $(docker ps -qa)
docker-compose up -d
docker exec todo-app python create.py