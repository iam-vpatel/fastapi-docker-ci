#!/bin/bash

APP_NAME="fastapi_app"
PORT=8000
TEST_ENDPOINT="/docs"

echo "🚀 Building Docker image..."
docker-compose build

echo "📦 Starting containers..."
docker-compose up -d

echo "⏳ Waiting for FastAPI to become available on http://localhost:$PORT$TEST_ENDPOINT..."

# Wait until the FastAPI service is up (max 30 seconds)
for i in {1..30}; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT$TEST_ENDPOINT)
    if [ "$HTTP_STATUS" -eq 200 ]; then
        echo "✅ FastAPI is up and running!"
        break
    else
        echo "🔁 Waiting... ($i/30)"
        sleep 1
    fi
done

if [ "$HTTP_STATUS" -ne 200 ]; then
    echo "❌ API did not start properly within 30 seconds."
    docker-compose logs $APP_NAME
    exit 1
fi

# Optional: Perform a test API call (replace with your actual endpoint)
echo "🧪 Sending test GET request to root..."
curl -s http://localhost:8000/

echo -e "\n🎉 Deployment script completed successfully!"
