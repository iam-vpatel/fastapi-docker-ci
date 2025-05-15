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
