"""
Custom Exception Classes
Domain-specific HTTP exceptions
"""
from fastapi import HTTPException, status


class ProductNotFoundException(HTTPException):
    """Raised when a product is not found."""
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )


class InsufficientStockException(HTTPException):
    """Raised when product stock is insufficient."""
    def __init__(self, product_id: int, available: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for product {product_id}. Available: {available}"
        )


class EmptyCartException(HTTPException):
    """Raised when attempting to checkout with empty cart."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )


class InvalidCredentialsException(HTTPException):
    """Raised when login credentials are invalid."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


class CustomerNotFoundException(HTTPException):
    """Raised when a customer is not found."""
    def __init__(self, customer_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer {customer_id} not found"
        )


class OrderNotFoundException(HTTPException):
    """Raised when an order is not found."""
    def __init__(self, order_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
