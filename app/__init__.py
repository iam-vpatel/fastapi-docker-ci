# app/__init__.py

# This will make your app package explicitly expose these objects when imported

from .main import app        # FastAPI instance
from .schemas import Item    # Pydantic model

__all__ = ["app", "Item"]