#!/bin/bash

# Load variables from .env
export $(grep -v '^#' .env | xargs)

# Build and start containers
docker-compose up --build
