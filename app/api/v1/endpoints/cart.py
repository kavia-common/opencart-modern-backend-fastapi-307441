"""
Cart Endpoints
Shopping cart operations
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_customer
from app.services.cart_service import CartService
from app.models.schemas.cart import (
    CartResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemAddResponse,
    CartUpdateResponse,
    CartDeleteResponse
)
from app.models.database.customer import Customer

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("", response_model=CartResponse, tags=["cart"])
def get_cart(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Get current user's shopping cart.
    
    Returns all cart items with calculated totals including
    subtotal, shipping, tax, and grand total.
    
    Args:
        current_customer: Authenticated customer
        db: Database session
        
    Returns:
        CartResponse: Cart items and totals
    """
    service = CartService(db)
    return service.get_cart(current_customer.customer_id)


# PUBLIC_INTERFACE
@router.post("/items", response_model=CartItemAddResponse, status_code=status.HTTP_201_CREATED, tags=["cart"])
def add_to_cart(
    item: CartItemCreate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Add item to shopping cart.
    
    Adds a product to the cart with specified quantity and options.
    If the item already exists, quantity is incremented.
    
    Args:
        item: Cart item data (product_id, quantity, options)
        current_customer: Authenticated customer
        db: Database session
        
    Returns:
        CartItemAddResponse: Cart item ID and confirmation message
        
    Raises:
        HTTPException 404: If product not found
        HTTPException 400: If insufficient stock
    """
    service = CartService(db)
    cart_id = service.add_item(
        current_customer.customer_id,
        item.product_id,
        item.quantity,
        item.options or {}
    )
    return CartItemAddResponse(cart_id=cart_id)


# PUBLIC_INTERFACE
@router.put("/items/{cart_id}", response_model=CartUpdateResponse, tags=["cart"])
def update_cart_item(
    cart_id: int,
    update_data: CartItemUpdate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Update cart item quantity.
    
    Modifies the quantity of an existing cart item.
    
    Args:
        cart_id: Cart item ID
        update_data: New quantity
        current_customer: Authenticated customer
        db: Database session
        
    Returns:
        CartUpdateResponse: Confirmation message
    """
    service = CartService(db)
    service.update_item(cart_id, update_data.quantity, current_customer.customer_id)
    return CartUpdateResponse()


# PUBLIC_INTERFACE
@router.delete("/items/{cart_id}", response_model=CartDeleteResponse, tags=["cart"])
def remove_from_cart(
    cart_id: int,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Remove item from cart.
    
    Deletes a cart item by ID.
    
    Args:
        cart_id: Cart item ID to remove
        current_customer: Authenticated customer
        db: Database session
        
    Returns:
        CartDeleteResponse: Confirmation message
    """
    service = CartService(db)
    service.remove_item(cart_id, current_customer.customer_id)
    return CartDeleteResponse()
