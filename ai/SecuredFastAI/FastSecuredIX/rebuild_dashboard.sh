#!/usr/bin/env bash
set -e

echo "Stopping and removing dashboard container/image..."
docker compose down

# Delete just the dashboard image so it cannot be reused
docker images | grep fastsecuredix-dashboard | awk '{print $3}' | xargs -r docker rmi -f

echo "Rebuilding dashboard container with --no-cache..."
docker compose build dashboard --no-cache

echo "Starting stack..."
docker compose up
