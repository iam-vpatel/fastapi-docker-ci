## 🧩 Part 1: Python and API Development

    The FastAPI application has been developed with the following features:

    Framework: FastAPI

    Database: SQLite using SQLAlchemy

    Validation: Pydantic models for request and response validation

    Endpoints:

    POST /users/: Create a new user

    GET /users/: Retrieve a list of users

    GET /users/{user_id}: Retrieve a specific user by ID

    PUT /users/{user_id}: Update a user's information

    DELETE /users/{user_id}: Delete a user

    Testing: Comprehensive unit tests using Pytest covering all endpoints

## ⚙️ Part 2: DevOps Integration

    1. Dockerfile
        Create a Dockerfile in the project root to containerize the FastAPI application:
    2. docker-compose.yml
        Create a docker-compose.yml file to define and run the multi-container Docker application:
    3. .dockerignore
        Create a .dockerignore file to prevent unnecessary files from being included in the Docker image:

```dockerignore
        __pycache__
        *.pyc
        *.pyo
        *.pyd
        *.db
        *.sqlite3
        .env
        venv
        build
        develop-eggs
        dist
        downloads
        eggs
        .eggs
        lib
        lib64
        parts
        sdist
        var
        *.egg-info
        .installed.cfg
        *.egg
```

    4. requirements.txt
        Ensure requirements.txt includes all necessary dependencies:

```
fastapi
uvicorn
pydantic
pytest
httpx
```

    5. Running the Application with Docker
        To build and run the application using Docker:

```
# Build the Docker image
docker-compose build

# Run the Docker container
docker-compose up
```

The FastAPI application will be accessible at http://localhost:8000.

    6. Running Tests Inside Docker
        To run the Pytest test suite inside the Docker container:

```
# Access the running container
docker exec -it fastapi_app bash

# Run tests
pytest
```

## 🧪 Evaluation Criteria

### Code Quality

Clarity: The code is organized into modular components (models.py, schemas.py, crud.py, main.py) for better readability.

### Maintainability: Use of Pydantic models and SQLAlchemy ORM promotes maintainable code.

### Best Practices: Adherence to FastAPI and Docker best practices, including environment variable management and containerization.

### Functionality

CRUD Operations: All CRUD endpoints are implemented and tested.

### API Behavior: Endpoints return appropriate HTTP status codes and JSON responses.

### Error Handling

Validation Errors: Handled using Pydantic's built-in validation.

### Resource Not Found: Returns 404 errors with descriptive messages when resources are not found.

### Docker Integration

Containerization: Application is fully containerized using Docker.

### docker-compose: Simplifies the process of building and running the application.

### Documentation

How_To_README.md: This file provides clear instructions for setting up and running the application using both Docker and non-Docker methods. It also includes details on testing and the CI/CD onboarding process for this application.

Project_README.md: This file outlines high-level and end-to-end details of the project, covering the overall architecture and implementation at a high level.

### Comments:

Code is commented where necessary to explain complex logic.

# ✅ Part 1: Build and Run FastAPI App Locally (Without Docker)

## 🔧 1. Install Python & pip (if not installed)

MacOS comes with Python, but it’s better to install the latest version via Homebrew:

```
brew install python
```

Check version:

```
python3 --version
pip3 --version

```

## 📁 2. Create Project Folder Structure

```
mkdir python_api && cd python_api

mkdir app tests
touch app/main.py app/schemas.py tests/test_main.py requirements.txt

```

## 🧱 3. Define Dependencies (requirements.txt)

Add this to requirements.txt:

```
fastapi
uvicorn
pydantic

```

## 🧑‍💻 4.Add API Code & Data Storage schema definitions

python_api/
├── app/
│ ├── main.py
│ ├── models.py
│ └── schemas.py
├── tests/
│ └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── deploy.sh
├── How_To_README.md
└── Project_README.md

### app/main.py - API Specification

        ✅ Framework: Use FastAPI to create the API.
        ✅ Endpoints: Define routes for creating, retrieving, updating, and deleting items of the chosen resource.
        ✅ Validation: Implement validation for incoming data on creation and update endpoints.

```python
from fastapi import FastAPI, HTTPException  # FastAPI core framework
from app.schemas import Item  # Use relative import inside package

app = FastAPI(title="Item API", version="1.0.0", description="A simple CRUD API for managing items")

# Simulated in-memory "database"
items_db = {}

# ✅ Create Item
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    """
    Creates a new item.
    Returns 400 if an item with the same ID already exists.
    """
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists with this ID")
    items_db[item.id] = item
    return item

# ✅ Retrieve Item
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Retrieves an item by its ID.
    Returns 404 if not found.
    """
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# ✅ Update Item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    """
    Updates an item by its ID.
    Returns 404 if not found.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = updated_item
    return updated_item

# ✅ Delete Item
@app.delete("/items/{item_id}", status_code=200)
def delete_item(item_id: int):
    """
    Deletes an item by ID.
    Returns 404 if not found.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"detail": f"Item {item_id} deleted successfully"}

# ✅ Health Check (Optional)
@app.get("/")
def read_root():
    """
    Root endpoint for health check or welcome message.
    """
    return {"message": "Welcome to the Item API. Visit /docs for Swagger UI."}
```

### app/schemas.py - Data Storage

    ✅ Database: Use SQLite for data storage.
    ✅ Schema: Design a simple schema relevant to the managed resource.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Item(BaseModel):
    """
    Defines the structure and validation rules for an Item.
    """
    id: int = Field(..., gt=0, description="ID must be greater than 0")
    name: str = Field(..., min_length=3, max_length=50, description="Name must be between 3 and 50 characters")
    description: Optional[str] = Field(default=None, max_length=200, description="Optional description, max 200 characters")

    @field_validator("name")
    def name_must_not_be_blank(cls, v):
        """
        Ensures the name is not blank or whitespace.
        """
        if not v.strip():
            raise ValueError("Name cannot be blank or just spaces")
        return v
```

## 📦 5. Install Requirements & Run

```python
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run FastAPI app with auto-reload enabled
uvicorn app.main:app --reload
```

## This command works perfectly with your listed dependencies:

- fastapi is the framework

- uvicorn is the ASGI server

- pydantic is used by FastAPI under the hood for data validation

### 📄 Code Overview

- `app/schemas.py` – Pydantic models
- `app/main.py` – FastAPI endpoints (CRUD)
- `requirements.txt` – Dependency file

✅ Visit: http://127.0.0.1:8000/docs to test API

## 🔗 Test in Swagger UI

Once you run FastAPI (via uvicorn or Docker), visit:

http://127.0.0.1:8000/docs

This auto-generated Swagger UI will allow you to test all endpoints interactively.

## ✅ Step-by-Step: Add Data Validation

We'll apply validation rules such as:
• id must be positive
• name must not be empty and should have a minimum length
• description should be optional but limited in length

### ❌ Invalid Create Request (Fails)

```
POST /items/
{
  "id": 0,
  "name": "  ",
  "description": "Too short"
}
Response:
{
  "detail": [
    {"loc": ["body", "id"], "msg": "ensure this value is greater than 0"},
    {"loc": ["body", "name"], "msg": "Name cannot be blank or just spaces"}
  ]
}
```

✅ Valid Create Request (Passes)

```
{
  "id": 1,
  "name": "Laptop",
  "description": "Development device"
}
```

## 📦 Summary Validation Rules

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

## 🧪 6. Add Test Code and Test Locally Run Unit Test (Part 1 – if no Docker)

### tests/test_main.py - Testing

    ✅ Framework: Write unit tests for each endpoint using pytest or another testing framework.
    ✅ Coverage: Ensure that tests cover all API functionalities.

This section includes unit tests for validating API functionality using `pytest` and `TestClient`.

```python
import sys
import os

# Allow imports from parent directory so app can be loaded
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    """
    Test creating a new item.
    """
    response = client.post("/items/", json={"id": 1, "name": "Item1", "description": "A test item"})
    assert response.status_code == 201  # Created status
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
    # Your app returns: {"detail": "Item 1 deleted successfully"}
    assert response.json()["detail"] == "Item 1 deleted successfully"

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

# 🐳 Part 2: Containerize with Docker (DevOps Approach)

## 🔧 1. Install Docker for Mac / Linux / Window

If not installed:
https://www.docker.com/products/docker-desktop/

Verify:

```
docker --version
```

## 🧾 2. Create Dockerfile

### Dockerfile - Dockerize Python Application

    ✅ Create a Dockerfile for your application, optimizing for minimal image size.

Create file Dockerfile in root folder:

```dockerfile
# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY ./app ./app

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Start the FastAPI app with live reload (for development)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## ⚙️ 3. Create docker-compose.yml

### Docker Compose - To run the API and a separate SQLite database container

    ✅ Compose File: Create a docker-compose.yml file to run the API and a separate SQLite database container.
    ✅ Volumes: Use volumes for database data persistence and optional live code reloading.

```yaml
version: "3.8"

services:
  fastapi:
    build: .
    container_name: fastapi_app
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
      - db_data:/app/db
    environment:
      - DATABASE_URL=sqlite:///./db/database.db
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```

## 🛠️ 4. Build & Run the App with Docker Compose

```
docker-compose up --build

```

✅ Go to: http://localhost:8000/docs

## 🛑 To Stop Docker App

In the terminal where it’s running:

```
CTRL+C
docker-compose down

```

## ✅ Summary

| Task               | Command or URL                                           |
| ------------------ | -------------------------------------------------------- |
| Install packages   | `pip install -r requirements.txt`                        |
| Run locally (dev)  | `uvicorn app.main:app --reload`                          |
| Docker build & run | `docker-compose up --build`                              |
| API Docs (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Stop Docker        | `CTRL+C` then `docker-compose down`                      |

## 🚀 5.Deployment Script

### Deployment Script - Here’s a complete summary of bash deployment script that:

    ✅ Script: Write a script (bash or shell) to build the Docker image, run the containers, and make a test request to check if the API is up.

### 📄 How to Use deployment script

            ✅ Builds the Docker image.
            ✅ Starts the containers with docker-compose.
            ✅ Waits for FastAPI to be available.
            ✅ Sends a test HTTP request to verify the API is live.

```bash
#!/bin/bash
APP_NAME="fastapi_app"
PORT=8000
TEST_ENDPOINT="/docs"

echo "🚀 Building Docker image..."
docker compose build

echo "📦 Starting containers..."
docker compose up -d

echo "⏳ Waiting for FastAPI to become available on http://localhost:$PORT$TEST_ENDPOINT..."

for i in {1..60}; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT$TEST_ENDPOINT) || echo "curl failed"
    if [ "$HTTP_STATUS" -eq 200 ]; then
        echo "✅ FastAPI is up and running!"
        break
    else
        echo "🔁 Waiting... ($i/60) - Status: $HTTP_STATUS"
        sleep 2
    fi
done

if [ "$HTTP_STATUS" -ne 200 ]; then
    echo "❌ API did not start properly within 120 seconds."
    docker compose logs $APP_NAME
    exit 1
fi

echo "🧪 Sending test GET request to root..."
curl -s http://localhost:8000/

echo -e "\n🎉 Deployment script completed successfully!"
```

Save the script above as deploy.sh in your project root.

Make it executable:

```bash
chmod +x deploy.sh
./deploy.sh
```

### 🧪Deployment Script Notes

      • It uses curl to check FastAPI is available.
      • We can update the test endpoint (/docs or /) to match your actual root or health check route.
      • Adjust container name (fastapi_app) if different in docker-compose.yml

## 🛠️ 6.Bonus: CI/CD Integration (Optional)

### CI/CD Integration (Optional) - Here's a complete steps for going from scratch on your Mac to running CI/CD with GitHub Actions for a FastAPI Docker app.

## 🧠 Goal: Start on your Mac → Create GitHub repo → Push FastAPI app → Auto CI/CD using GitHub Actions.

### ✅ Step-by-Step Instructions

🔧 PART 1: LOCAL SETUP ON MAC

1️⃣ Install Prerequisites (Skip if Already Installed)
➤ Install Python & pip:

```
brew install python
python3 --version
pip3 --version

```

➤ Install Git:

```
brew install git
git --version

```

➤ Install Docker:

Download Docker Desktop: https://www.docker.com/products/docker-desktop/

➤ Install GitHub CLI (optional but useful):

```
brew install gh

```

2️⃣ Create FastAPI Project(Skip if Already Installed your Pyhton Application)

```
mkdir python_api && cd python_api
mkdir app tests
touch app/main.py app/test_main.py requirements.txt Dockerfile docker-compose.yml

```

➤ app/main.py:
➤ app/schemas.py:
➤ app/test_main.py:
➤ requirements.txt:
➤ Dockerfile:
➤ docker-compose.yml:

3️⃣ Run Locally to Verify

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

```

Visit: http://127.0.0.1:8000/docs

Or run with Docker:

```
docker-compose up --build
```

### 🟩 PART 2: PUSH TO GITHUB & SETUP CI/CD

4️⃣ Initialize Git and Push to GitHub

```
git init
git add .
git commit -m "Initial FastAPI Docker app"

```

➤ Create GitHub repo from CLI:

```
gh auth login  # Log in with GitHub CLI if not done
gh repo create fastapi-docker-ci --public --source=. --remote=origin --push
```

Or manually create repo at https://github.com/new, then:

```
git remote add origin https://github.com/<your-username>/fastapi-docker-ci.git
git push -u origin main
```

5️⃣ Add GitHub Actions CI/CD Pipeline

Create folder:

```
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

➤ Paste into .github/workflows/ci.yml:

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

      - name: Set up Docker Compose
        run: |
          curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose

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

      - name: Run Docker container
        run: docker-compose up -d

      - name: Wait for FastAPI to be ready
        run: |
          for i in {1..60}; do
              STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs) || echo "curl failed"
              if [ "$STATUS" = "200" ]; then
                  echo "✅ FastAPI is ready"
                  break
              else
                  echo "🔁 Waiting for FastAPI... ($i/60) — Status: $STATUS"
                  sleep 2
              fi
          done

      - name: Run tests
        run: pytest

      - name: Cleanup
        run: docker-compose down
```

6️⃣ Push Workflow File to Trigger GitHub Actions

```
git add .github
git commit -m "Add GitHub Actions CI/CD pipeline"
git push
```

7️⃣ ✅ Validate GitHub Actions Run
Go to your repo:

- 📍 GitHub Repo → Actions → CI - FastAPI Docker

* You’ll see the job running. If everything is correct, it should:

* Build image

* Run container

* Validate /docs

* Run tests

* Shut down

## 🧠 Optional Enhancements

Add Slack notifications, code coverage, DockerHub push, or AWS deploy.

🔚 Summary Table

| Step             | Command / Action                        |
| ---------------- | --------------------------------------- |
| Create project   | `mkdir python_api && cd python_api`     |
| Test locally     | `uvicorn app.main:app --reload`         |
| Docker run       | `docker-compose up --build`             |
| Initialize git   | `git init`                              |
| Push to GitHub   | `gh repo create` or manual + `git push` |
| Add CI file      | `.github/workflows/ci.yml`              |
| Trigger pipeline | `git push`                              |
