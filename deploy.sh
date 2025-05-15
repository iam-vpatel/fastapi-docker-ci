#!/bin/bash

set -e

APP_NAME="fastapi_app"
PORT=8000
TEST_ENDPOINT="/docs"
URL="http://localhost:$PORT$TEST_ENDPOINT"

echo "🔍 Checking if Docker is installed and running..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker."
    exit 1
fi

echo "🚀 Building Docker image..."
docker-compose build

echo "📦 Starting containers..."
docker-compose up -d

echo "⏳ Waiting for FastAPI to become available on $URL..."

USE_HEALTHCHECK=false

# Check if healthcheck exists
if docker inspect --format '{{json .State.Health}}' "$APP_NAME" &>/dev/null; then
    USE_HEALTHCHECK=true
fi

if [ "$USE_HEALTHCHECK" = true ]; then
    for i in {1..30}; do
        STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$APP_NAME")
        echo "⏳ Container health status: $STATUS ($i/30)"
        if [ "$STATUS" == "healthy" ]; then
            echo "✅ FastAPI container is healthy."
            break
        fi
        sleep 2
    done

    if [ "$STATUS" != "healthy" ]; then
        echo "❌ FastAPI container did not become healthy in time."
        docker-compose logs "$APP_NAME"
        exit 1
    fi
else
    for i in {1..30}; do
        HTTP_STATUS=$(curl --max-time 2 -s -o /dev/null -w "%{http_code}" "$URL")
        if [ "$HTTP_STATUS" -eq 200 ]; then
            echo "✅ FastAPI is up and running!"
            break
        else
            echo "🔁 Waiting... HTTP status: $HTTP_STATUS ($i/30)"
            sleep 2
        fi
    done

    if [ "$HTTP_STATUS" -ne 200 ]; then
        echo "❌ API did not start properly within 30 seconds."
        docker-compose logs "$APP_NAME"
        exit 1
    fi
fi

# Optional: Perform a test API call
echo "🧪 Sending test GET request to / ..."
curl -s "http://localhost:$PORT/"

echo -e "\n🎉 Deployment script completed successfully!"
