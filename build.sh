#!/bin/bash

# Check if Docker daemon is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# Parameterize port and container name for flexibility
CONTAINER_NAME="chatbot-api-container"
IMAGE_NAME="chatbot-api"
PORT=4000

# Stop and remove the existing Docker container, if it exists
if docker container inspect $CONTAINER_NAME > /dev/null 2>&1; then
    echo "Removing existing Docker container..."
    docker container rm -f $CONTAINER_NAME || { echo "Failed to remove container"; exit 1; }
fi

# Remove the existing Docker image, if it exists
if docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
    echo "Removing existing Docker image..."
    docker image rm -f $IMAGE_NAME || { echo "Failed to remove image"; exit 1; }
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME . || { echo "Docker build failed"; exit 1; }

# Run the Docker container
echo "Running Docker container..."
docker run -d --name $CONTAINER_NAME -p $PORT:4000 --restart always $IMAGE_NAME || { echo "Failed to start container"; exit 1; }

echo "Docker container $CONTAINER_NAME running on port $PORT"
