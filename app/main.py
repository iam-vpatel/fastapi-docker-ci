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

