"""
Authentication Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel, EmailStr, Field


class CustomerRegister(BaseModel):
    """Schema for customer registration."""
    firstname: str = Field(..., min_length=1, max_length=32)
    lastname: str = Field(..., min_length=1, max_length=32)
    email: EmailStr
    telephone: str = Field(..., min_length=7, max_length=32)
    password: str = Field(..., min_length=6)


class CustomerLogin(BaseModel):
    """Schema for customer login."""
    email: EmailStr
    password: str


class CustomerResponse(BaseModel):
    """Schema for customer data response."""
    customer_id: int
    email: str
    firstname: str
    lastname: str
    telephone: str
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    customer: CustomerResponse
