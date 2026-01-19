"""
Cart Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class CartItemCreate(BaseModel):
    """Schema for adding item to cart."""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(1, gt=0, description="Quantity")
    options: Optional[Dict[str, str]] = Field(default_factory=dict, description="Product options")


class CartItemUpdate(BaseModel):
    """Schema for updating cart item."""
    quantity: int = Field(..., gt=0, description="New quantity")


class CartItemOption(BaseModel):
    """Cart item option schema."""
    name: str
    value: str
    price_modifier: float = 0.0


class CartItemResponse(BaseModel):
    """Schema for cart item response."""
    cart_id: int
    product_id: int
    name: str
    model: str
    image: Optional[str] = None
    quantity: int
    price: float
    total: float
    options: List[CartItemOption] = []


class CartTotalLine(BaseModel):
    """Cart total line schema."""
    code: str
    title: str
    value: float


class CartResponse(BaseModel):
    """Schema for cart response."""
    items: List[CartItemResponse]
    totals: List[CartTotalLine]


class CartItemAddResponse(BaseModel):
    """Schema for add to cart response."""
    cart_id: int
    message: str = "Product added to cart"


class CartUpdateResponse(BaseModel):
    """Schema for cart update response."""
    message: str = "Cart updated"


class CartDeleteResponse(BaseModel):
    """Schema for cart delete response."""
    message: str = "Item removed from cart"
