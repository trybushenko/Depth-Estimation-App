# Depth Estimation

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tools and Technologies](#tools-and-technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Optimizations](#optimizations)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Depth Estimation is a full-stack application designed to predict depth maps from input images using advanced machine learning models. It consists of a backend API built with FastAPI and a responsive frontend interface developed with modern web technologies. The project leverages Docker for containerization, ensuring consistent environments across development and production setups.

## Features
- Backend API: Provides endpoints for uploading images and retrieving depth maps
- Frontend Interface: User-friendly web application for interacting with the depth estimation service
- Dockerized Setup: Simplifies deployment and environment management
- Model Weights Management: Efficient handling and downloading of model weights during runtime
- Optimized Docker Images: Multi-stage builds and dependency pruning to minimize image sizes

## Project Structure
```
depth-estimation/
├── .dockerignore
├── build_and_run.sh
├── clean_up.sh
├── docker-compose.yml
├── entrypoint.sh
├── notebooks/
│   └── 2024-11-16-depth-anything-launch-and-benchmark.ipynb
├── poetry.lock
├── pyproject.toml
├── README.md
├── setup.py
└── src/
    ├── backend/
    │   ├── Dockerfile
    │   ├── __init__.py
    │   ├── main.py
    │   └── models/
    ├── depth_estimation/
    │   ├── depth_anything_v2/
    │   └── __init__.py
    └── frontend/
        ├── Dockerfile
        ├── nginx.conf
        ├── node_modules/
        ├── package.json
        ├── package-lock.json
        ├── public/
        ├── src/
        └── tsconfig.json
```

### Directory Overview
- `docker-compose.yml`: Defines multi-container Docker applications
- `build_and_run.sh`: Bash script to build and run Docker containers for backend and frontend
- `clean_up.sh`: Bash script to stop and remove Docker containers and network
- `src/backend/`: Contains the backend FastAPI application and its Dockerfile
- `src/frontend/`: Contains the frontend web application and its Dockerfile
- `notebooks/`: Jupyter notebooks for research and development
- `.dockerignore`: Specifies files and directories to exclude from Docker builds

## Tools and Technologies
- Docker: Containerization platform to ensure consistent environments
- FastAPI: High-performance Python web framework for building APIs
- React: JavaScript library for building user interfaces
- Poetry: Dependency management and packaging tool for Python
- PyTorch: Deep learning framework used for model development
- Nginx: Web server used in the frontend for serving the React application
- Uvicorn: ASGI server for running FastAPI applications
- Gdown: Tool for downloading files from Google Drive

## Prerequisites
Before running the project, ensure you have the following installed on your system:

- Docker: Version [27.3.1](https://docs.docker.com/engine/release-notes/27/#2731)
- Nvidia Container Toolkit: Version [1.17.2](https://github.com/NVIDIA/nvidia-container-toolkit/releases)
- Git: For cloning the repository
- Bash: For running the provided scripts

## Installation

### 1. Clone the Repository
Navigate to your desired directory and clone the project repository:
```bash
git clone https://github.com/alexrivera/depth_estimation.git
cd depth_estimation
```

### 2. Build and Run Docker Containers
Execute the build_and_run.sh script to build and run both backend and frontend Docker containers:
```bash
./build_and_run.sh
```

#### Script Breakdown:
1. **Build Backend Image**: Builds the backend Docker image using the Dockerfile located in src/backend/.
```bash
docker build -f src/backend/Dockerfile -t depth_estimation:v1.0 .
```

2. **Build Frontend Image**: Builds the frontend Docker image using the Dockerfile located in src/frontend/.
```bash
docker build -f src/frontend/Dockerfile -t depth_estimation_frontend:v1.0 src/frontend/
```

3. **Create Docker Network**: Creates a Docker network named app-network for inter-container communication.
```bash
docker network create app-network
```

4. **Run Backend Container**: Runs the backend container, connecting it to app-network and exposing port 8000.
```bash
docker run -d --name backend --network app-network -p 8000:8000 depth_estimation:v1.0
```

5. **Run Frontend Container**: Runs the frontend container, connecting it to app-network and exposing port 8080.
```bash
docker run -d --name frontend --network app-network -p 8080:80 depth_estimation_frontend:v1.0
```

**Note**: Ensure that the ports 8000 and 8080 are available on your host machine.

## Usage
Once the Docker containers are up and running, you can interact with the application as follows:

- Backend API: Accessible at http://localhost:8000/docs for interactive API documentation via Swagger UI
- Frontend Interface: Accessible at http://localhost:8080 to use the web application for depth estimation

### Example API Usage
1. **Access Swagger UI**:
   - Navigate to http://localhost:8000/docs to view and interact with the API endpoints

2. **Predict Depth Map**:
   - Use the `/predict` endpoint to upload an image and receive its depth map

## Scripts

### build_and_run.sh
A bash script to build and run Docker containers for both backend and frontend services.

Features:
- Docker Installation Check: Verifies if Docker is installed before proceeding
- Image Building: Builds Docker images for backend and frontend
- Network Management: Creates a Docker network if it doesn't already exist
- Container Management: Removes existing containers with the same name before running new ones to avoid conflicts
- Informative Output: Provides clear messages throughout the build and run process

Usage:
```bash
./build_and_run.sh
```

### clean_up.sh
A bash script to stop and remove Docker containers and the Docker network associated with the project.

Features:
- Docker Installation Check: Verifies if Docker is installed before proceeding
- Container Removal: Stops and removes backend and frontend containers if they exist
- Network Removal: Deletes the app-network Docker network if it exists
- Informative Output: Provides clear messages throughout the cleanup process

Usage:
```bash
./clean_up.sh
```

## Optimizations
To ensure efficient Docker image sizes and build times, the project incorporates several optimizations:

### Multi-Stage Builds
Separates the build environment from the runtime environment, ensuring only necessary artifacts are included in the final image.

### .dockerignore Configuration
Located at the root of the project to exclude unnecessary files and directories from the Docker build context, reducing image size and build time.

```
# Exclude frontend-related files
src/frontend/
src/**/node_modules/
src/**/__pycache__/

# Exclude development and version control files
.git
.gitignore
.env
*.pyc
notebooks/
tmp/
```

### Additional Optimizations
- **Selective File Copying**: Dockerfiles are configured to copy only the necessary backend or frontend source code, avoiding the inclusion of irrelevant files
- **Dependency Pruning**: The pyproject.toml is curated to include only essential dependencies for the backend API, excluding development and R&D packages
- **Layer Consolidation**: Dockerfile RUN commands are consolidated to minimize the number of layers, further reducing image size
- **Runtime Model Weight Handling**: Model weights are downloaded during the Docker run phase rather than being included in the image, saving space. Additionally, consider mounting a persistent volume for model weights to avoid repeated downloads

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the Repository

2. Create a Feature Branch
```bash
git checkout -b feature/YourFeature
```

3. Commit Your Changes
```bash
git commit -m "Add some feature"
```

4. Push to the Branch
```bash
git push origin feature/YourFeature
```

5. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate documentation.

## License
This project is licensed under the MIT License.