"""
Product Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    model: str
    price: float = Field(ge=0, description="Product price")


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    description: Optional[str] = None
    quantity: int = 0
    image: Optional[str] = None
    status: int = 1
    manufacturer_id: Optional[int] = None
    sku: Optional[str] = None


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    model: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    quantity: Optional[int] = None
    image: Optional[str] = None
    status: Optional[int] = None


class ProductResponse(BaseModel):
    """Schema for product list response."""
    product_id: int
    name: str
    model: str
    price: float
    image: Optional[str] = None
    special_price: Optional[float] = None
    rating: Optional[float] = None
    reviews_count: int = 0
    
    class Config:
        from_attributes = True


class ProductOptionValue(BaseModel):
    """Product option value schema."""
    value_id: int
    name: str
    price_prefix: str = "+"
    price: float = 0.0


class ProductOption(BaseModel):
    """Product option schema."""
    product_option_id: int
    name: str
    type: str
    required: bool = False
    values: List[ProductOptionValue] = []


class ProductDetail(BaseModel):
    """Schema for detailed product response."""
    product_id: int
    name: str
    model: str
    description: Optional[str] = None
    price: float
    special_price: Optional[float] = None
    tax: float = 0.0
    quantity: int
    minimum: int = 1
    image: Optional[str] = None
    images: List[str] = []
    manufacturer: Optional[str] = None
    sku: Optional[str] = None
    options: List[ProductOption] = []
    related_products: List[int] = []
    rating: Optional[float] = None
    reviews_count: int = 0
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list."""
    items: List[ProductResponse]
    total: int
    page: int
    limit: int
    pages: int
