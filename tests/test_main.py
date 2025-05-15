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
