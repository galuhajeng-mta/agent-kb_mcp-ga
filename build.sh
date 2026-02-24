#!/bin/bash

# Configuration for Docker image
# GitHub Container Registry path
docker_registry='asia-southeast2-docker.pkg.dev/arched-jetty-392811/mta-docker/mcp'
# Name of the artifact/image
artifact_id=$(grep '^name =' pyproject.toml | cut -d '"' -f 2)
# Version from VERSION file
full_version=$(grep '^version =' pyproject.toml | cut -d '"' -f 2)


docker build --platform=linux/amd64 --no-cache -f Dockerfile \
  -t $docker_registry/$artifact_id:$full_version \
  -t $docker_registry/$artifact_id:latest .

# Push the image to Docker Registry
docker push $docker_registry/$artifact_id:$full_version
docker push $docker_registry/$artifact_id:latest

