"""
Category Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel
from typing import Optional, List


class CategoryResponse(BaseModel):
    """Schema for category response."""
    category_id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    parent_id: int = 0
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for category list."""
    categories: List[CategoryResponse]
