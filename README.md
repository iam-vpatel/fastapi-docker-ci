# 🧰 FastAPI + DevOps Full Stack Project

## 🎯 Objectives

### ✅ Part 1: Build a Python REST API

This part focuses on developing a robust, standards-compliant RESTful API.

Develop the API using FastAPI, a modern, high-performance Python framework.

Implement full CRUD operations (Create, Read, Update, Delete).

Use Pydantic for request/response validation and schema enforcement.

Handle errors gracefully using appropriate HTTP status codes and exception handling.

Enable auto-generated, interactive documentation via Swagger UI and ReDoc.

Ensure clean, modular project structure for maintainability and clarity.

### ✅ Part 2: Containerize the API with Docker

This part validates your ability to apply DevOps principles for deployment consistency.

Write a Dockerfile to package the FastAPI application and its dependencies.

Create a docker-compose.yml file to orchestrate the application stack.

Ensure all dependencies are installed during container build time.

Enable volume mounting for live code reloading in development mode.

Simulate database persistence using volumes with an SQLite file.

Run and test the API inside the container for a fully portable environment.

### This project demonstrates how to build, test, containerize, and deploy a FastAPI-based Python API using DevOps best practices.

### It includes full local setup, Docker support, GitHub Actions CI/CD, and proper structuring for maintainability and extensibility.

## 🔧 Part 1: Python and API Development

### ⚙️ Framework and Tools

- **Framework**: FastAPI – modern, fast, and auto-doc-enabled.
- **Data Validation**: Pydantic – used for clean validation schemas.
- **Data Storage**: In-memory dictionary (for simplicity).

### 📁 Project Structure

```
python_api/
├── app/
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── deploy.sh
├── How_To_README.md
└── Project_README.md

```

### 📄 Code Overview

- `app/schemas.py` – Pydantic models
- `app/main.py` – FastAPI endpoints (CRUD)
- `requirements.txt` – Dependency file

## 🐳 Part 2: DevOps and Containerization

### 🐋 Dockerization

**Dockerfile**

```dockerfile
# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY ./app ./app

# Expose port
EXPOSE 8000

# Start the FastAPI app
# The --reload flag enables live code reloading, ideal for development.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 🔗 Docker Compose

**docker-compose.yml**

```yaml
version: "3.8"

services:
  fastapi:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app # Live code reload
      - db_data:/app/db # Mount for SQLite file persistence
    depends_on:
      - sqlite
    environment:
      - DATABASE_URL=sqlite:///./db/database.db # I use DATABASE_URL=sqlite:///./db/database.db

  # SQLite does not need a running DB container, but I create a dummy container sqlite.
  # Just to keep the volume mount organized and simulate DB separation.
  sqlite:
    image: alpine
    container_name: sqlite_dummy
    volumes:
      - db_data:/db # db_data volume ensures data persists between runs.
    command: tail -f /dev/null # Dummy container to simulate DB persistence

volumes:
  db_data:
```

### 📖 API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🚀 Deployment and Execution

### 🛠 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- `curl` for testing (CLI)

### ▶️ Run Locally (No Docker)

```bash
brew install python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### ▶️ Run with Docker

```bash
docker-compose up --build
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📦 Validation Rules

| Field         | Rule                                           |
| ------------- | ---------------------------------------------- |
| `id`          | Must be an integer > 0                         |
| `name`        | Cannot be empty or whitespace, 3–50 characters |
| `description` | Optional, max 200 characters                   |

## ✅ Sample Endpoints

| Method | Route         | Description       |
| ------ | ------------- | ----------------- |
| POST   | `/items/`     | Create a new item |
| GET    | `/items/{id}` | Retrieve by ID    |
| PUT    | `/items/{id}` | Update item       |
| DELETE | `/items/{id}` | Delete item       |

## 🧪 Testing Locally

**tests/test_main.py**

```python
import sys
import os

# Allow imports from parent directory so app can be loaded
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient  # Import TestClient for API testing
from app.main import app  # Import the FastAPI app

client = TestClient(app)  # Create a test client instance

def test_create_item():
    """
    Test creating a new item.
    """
    response = client.post("/items/", json={"id": 1, "name": "Item1", "description": "A test item"})
    assert response.status_code == 200
    assert response.json()["name"] == "Item1"

def test_get_item():
    """
    Test retrieving an existing item by ID.
    """
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_item_404():
    """
    Test retrieving a non-existent item by ID (expect 404).
    """
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item():
    """
    Test updating an existing item.
    """
    updated_data = {"id": 1, "name": "UpdatedItem", "description": "Updated description"}
    response = client.put("/items/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedItem"

def test_update_item_404():
    """
    Test updating a non-existent item (expect 404).
    """
    updated_data = {"id": 999, "name": "NonExistent", "description": "Does not exist"}
    response = client.put("/items/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item():
    """
    Test deleting an existing item.
    """
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted"

def test_delete_item_404():
    """
    Test deleting a non-existent item (expect 404).
    """
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
```

Run:

```bash
pytest tests/test_main.py
```

## 📜 Deployment Script

**deploy.sh**

```bash
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

```

Make it executable:

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔁 GitHub Actions CI/CD

### 📁 Directory Structure

```
.github/
└── workflows/
    └── ci.yml
```

### ✨ ci.yml

```yaml
name: CI - FastAPI Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install fastapi uvicorn pytest httpx

      - name: Build Docker image
        run: docker-compose build

      - name: Run containers
        run: docker-compose up -d

      - name: Wait for API
        run: |
          for i in {1..30}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
            if [ "$STATUS" = "200" ]; then
              echo "FastAPI is up!"
              break
            fi
            sleep 2
          done

      - name: Run tests
        run: pytest tests/test_main.py

      - name: Tear down
        run: docker-compose down
```

## 🧠 Conclusion

This project demonstrates how to:

- Develop a Python FastAPI application
- Validate and document it automatically
- Containerize it with Docker
- Manage persistent data with SQLite and volumes
- Automate testing and deployment with GitHub Actions

By following this runbook, you ensure repeatable and reliable deployments — the true spirit of a DevOps/SRE engineer.
