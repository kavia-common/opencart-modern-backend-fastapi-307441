"""
Cart Endpoints
Shopping cart operations
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_customer
from app.core.database import get_db
from app.models.database.customer import Customer
from app.models.schemas.cart import (
    CartDeleteResponse,
    CartItemAddResponse,
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
    CartUpdateResponse,
)
from app.services.cart_service import CartService

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=CartResponse,
    tags=["cart"],
    summary="Get current cart",
    description="Return the authenticated customer's cart items and calculated totals.",
    operation_id="getCart",
)
def get_cart(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> CartResponse:
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
@router.post(
    "/items",
    response_model=CartItemAddResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["cart"],
    summary="Add item to cart",
    description="Add a product to the authenticated customer's cart (increments quantity if already present).",
    operation_id="addCartItem",
)
def add_to_cart(
    item: CartItemCreate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> CartItemAddResponse:
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
        item.options or {},
    )
    return CartItemAddResponse(cart_id=cart_id)


# PUBLIC_INTERFACE
@router.put(
    "/items/{cart_id}",
    response_model=CartUpdateResponse,
    tags=["cart"],
    summary="Update cart item quantity",
    description="Update the quantity for a specific cart item belonging to the authenticated customer.",
    operation_id="updateCartItem",
)
def update_cart_item(
    cart_id: int,
    update_data: CartItemUpdate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> CartUpdateResponse:
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
@router.delete(
    "/items/{cart_id}",
    response_model=CartDeleteResponse,
    tags=["cart"],
    summary="Remove item from cart",
    description="Remove a specific cart item from the authenticated customer's cart.",
    operation_id="removeCartItem",
)
def remove_from_cart(
    cart_id: int,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> CartDeleteResponse:
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
