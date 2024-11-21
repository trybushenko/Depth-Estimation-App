#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
BACKEND_DIR="src/backend"
FRONTEND_DIR="src/frontend"
BACKEND_IMAGE="depth_estimation:v1.0"
FRONTEND_IMAGE="depth_estimation_frontend:v1.0"
NETWORK_NAME="app-network"
BACKEND_CONTAINER="backend"
FRONTEND_CONTAINER="frontend"
BACKEND_PORT=8000
FRONTEND_PORT=8080

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

# Function to build the backend Docker image
build_backend() {
    echo "Building backend Docker image..."
    docker build -f "$BACKEND_DIR/Dockerfile" -t "$BACKEND_IMAGE" .
    echo "Backend image built successfully: $BACKEND_IMAGE"
}

# Function to build the frontend Docker image
build_frontend() {
    echo "Building frontend Docker image..."
    docker build -f "$FRONTEND_DIR/Dockerfile" -t "$FRONTEND_IMAGE" "$FRONTEND_DIR"
    echo "Frontend image built successfully: $FRONTEND_IMAGE"
}

# Function to create Docker network
create_network() {
    if docker network ls --format '{{.Name}}' | grep -w "$NETWORK_NAME" > /dev/null; then
        echo "Docker network '$NETWORK_NAME' already exists."
    else
        echo "Creating Docker network '$NETWORK_NAME'..."
        docker network create "$NETWORK_NAME"
        echo "Docker network '$NETWORK_NAME' created successfully."
    fi
}

# Function to run backend container
run_backend() {
    if [ "$(docker ps -a -f name=$BACKEND_CONTAINER --format '{{.Names}}')" == "$BACKEND_CONTAINER" ]; then
        echo "Backend container '$BACKEND_CONTAINER' already exists. Restarting container..."
        docker rm -f "$BACKEND_CONTAINER"
    fi

    echo "Running backend container..."
    docker run -d \
        --name "$BACKEND_CONTAINER" \
        --network "$NETWORK_NAME" \
        -p "$BACKEND_PORT":8000 \
        "$BACKEND_IMAGE"
    echo "Backend container '$BACKEND_CONTAINER' is up and running on port $BACKEND_PORT."
}

# Function to run frontend container
run_frontend() {
    if [ "$(docker ps -a -f name=$FRONTEND_CONTAINER --format '{{.Names}}')" == "$FRONTEND_CONTAINER" ]; then
        echo "Frontend container '$FRONTEND_CONTAINER' already exists. Restarting container..."
        docker rm -f "$FRONTEND_CONTAINER"
    fi

    echo "Running frontend container..."
    docker run -d \
        --name "$FRONTEND_CONTAINER" \
        --network "$NETWORK_NAME" \
        -p "$FRONTEND_PORT":80 \
        "$FRONTEND_IMAGE"
    echo "Frontend container '$FRONTEND_CONTAINER' is up and running on port $FRONTEND_PORT."
}

# Main Execution Flow
echo "Starting the build and run process..."

check_docker
build_backend
build_frontend
create_network
run_backend
run_frontend

echo "All containers are built and running successfully."

