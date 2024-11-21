#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
NETWORK_NAME="app-network"
BACKEND_CONTAINER="backend"
FRONTEND_CONTAINER="frontend"

# Function to check if Docker is installed
check_docker() {
    echo "Checking Docker installation..."

    echo "Current PATH: $PATH"
    echo "Locating Docker command..."
    if command -v docker &> /dev/null; then
        echo "Docker command found at $(which docker)."
        docker --version
        return 0
    fi

    echo "Docker command not found. Checking for docker.io..."
    if command -v docker.io &> /dev/null; then
        echo "docker.io command found at $(which docker.io)."
        docker.io --version
        return 0
    fi

    echo "Checking if Docker service is active..."
    if systemctl is-active --quiet docker; then
        echo "Docker service is active."
        return 0
    fi

    echo "Checking common Docker paths..."
    if [ -x "/usr/bin/docker" ] || [ -x "/usr/local/bin/docker" ]; then
        echo "Docker executable found in /usr/bin/docker or /usr/local/bin/docker."
        return 0
    fi

    echo "Docker is not installed or not properly configured."
    echo "Please ensure Docker is installed and the service is running:"
    echo "1. Install Docker: sudo apt install docker.io"
    echo "2. Start Docker: sudo systemctl start docker"
    echo "3. Enable Docker service: sudo systemctl enable docker"
    echo "4. Add your user to docker group: sudo usermod -aG docker \$USER"
    echo "5. Log out and log back in for the group changes to take effect"
    exit 1
}

# Function to stop and remove a container if it exists
remove_container() {
    local container_name=$1
    local container_status
    container_status=$(docker ps -a --filter "name=^/${container_name}$" --format '{{.Names}}')

    if [ "$container_status" = "$container_name" ]; then
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

# Attempt to remove the network
# If it fails due to active endpoints, list and remove those containers first
if docker network ls --format '{{.Name}}' | grep -w "$NETWORK_NAME" > /dev/null; then
    echo "Attempting to remove Docker network '$NETWORK_NAME'..."
    if ! docker network rm "$NETWORK_NAME"; then
        echo "Failed to remove network '$NETWORK_NAME' because it has active endpoints."
        echo "Listing containers connected to '$NETWORK_NAME':"
        docker network inspect "$NETWORK_NAME" -f '{{range .Containers}}{{.Name}} {{end}}' | tr ' ' '\n'

        # Remove all containers connected to the network
        connected_containers=$(docker network inspect "$NETWORK_NAME" -f '{{range .Containers}}{{.Name}} {{end}}')
        for container in $connected_containers; do
            echo "Stopping and removing connected container '$container'..."
            docker rm -f "$container"
            echo "Container '$container' removed."
        done

        # Retry removing the network
        echo "Retrying to remove Docker network '$NETWORK_NAME'..."
        docker network rm "$NETWORK_NAME"
        echo "Docker network '$NETWORK_NAME' removed successfully."
    fi
else
    echo "Docker network '$NETWORK_NAME' does not exist. Skipping..."
fi

echo "Cleanup completed successfully."
