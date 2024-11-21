#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
NETWORK_NAME="app-network"
BACKEND_CONTAINER="backend"
FRONTEND_CONTAINER="frontend"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null
    then
        echo "Docker is not installed. Please install Docker and try again."
        exit 1
    fi
}

# Function to stop and remove a container if it exists
remove_container() {
    local container_name=$1
    if [ "$(docker ps -a -f name=$container_name --format '{{.Names}}')" == "$container_name" ]; then
        echo "Stopping and removing container '$container_name'..."
        docker rm -f "$container_name"
        echo "Container '$container_name' removed successfully."
    else
        echo "Container '$container_name' does not exist. Skipping..."
    fi
}

# Function to remove Docker network if it exists
remove_network() {
    if docker network ls --format '{{.Name}}' | grep -w "$NETWORK_NAME" > /dev/null; then
        echo "Removing Docker network '$NETWORK_NAME'..."
        docker network rm "$NETWORK_NAME"
        echo "Docker network '$NETWORK_NAME' removed successfully."
    else
        echo "Docker network '$NETWORK_NAME' does not exist. Skipping..."
    fi
}

# Main Execution Flow
echo "Starting the cleanup process..."

check_docker
remove_container "$BACKEND_CONTAINER"
remove_container "$FRONTEND_CONTAINER"
remove_network

echo "Cleanup completed successfully."