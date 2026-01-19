"""
Order Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class AddressSchema(BaseModel):
    """Address schema for orders."""
    firstname: str
    lastname: str
    address_1: str
    address_2: Optional[str] = None
    city: str
    postcode: str
    country_id: int
    zone_id: int


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    shipping_address: AddressSchema
    payment_address: AddressSchema
    shipping_method: str
    payment_method: str
    comment: Optional[str] = None


class ShippingMethodResponse(BaseModel):
    """Shipping method schema."""
    code: str
    title: str
    cost: float
    tax_class_id: int = 0


class ShippingMethodsResponse(BaseModel):
    """Shipping methods response schema."""
    methods: List[ShippingMethodResponse]


class PaymentMethodResponse(BaseModel):
    """Payment method schema."""
    code: str
    title: str


class PaymentMethodsResponse(BaseModel):
    """Payment methods response schema."""
    methods: List[PaymentMethodResponse]


class OrderProductResponse(BaseModel):
    """Order product schema."""
    name: str
    model: str
    quantity: int
    price: float
    total: float


class OrderTotalResponse(BaseModel):
    """Order total line schema."""
    title: str
    value: float


class OrderResponse(BaseModel):
    """Schema for order list response."""
    order_id: int
    invoice_no: int
    status: str
    total: float
    date_added: str


class OrderDetailResponse(BaseModel):
    """Schema for detailed order response."""
    order_id: int
    invoice_no: int
    status: str
    customer: dict
    payment_address: dict
    shipping_address: Optional[dict] = None
    products: List[OrderProductResponse]
    totals: List[OrderTotalResponse]
    date_added: str


class OrderListResponse(BaseModel):
    """Schema for order list."""
    orders: List[OrderResponse]
    total: int = 0
    page: int = 1


class OrderCreateResponse(BaseModel):
    """Schema for order creation response."""
    order_id: int
    invoice_no: int
    total: float
    message: str = "Order placed successfully"
