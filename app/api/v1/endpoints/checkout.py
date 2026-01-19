"""
Checkout Endpoints
Checkout and order placement operations
"""
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_customer
from app.services.order_service import OrderService
from app.services.shipping_service import ShippingService
from app.services.payment_service import PaymentService
from app.models.schemas.order import (
    OrderCreate,
    OrderCreateResponse,
    ShippingMethodsResponse,
    PaymentMethodsResponse
)
from app.models.database.customer import Customer

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/shipping-methods", response_model=ShippingMethodsResponse, tags=["checkout"])
def get_shipping_methods(
    country_id: int = Body(..., embed=True),
    zone_id: int = Body(..., embed=True),
    postcode: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Get available shipping methods for the order.
    
    Returns available shipping options based on delivery address.
    
    Args:
        country_id: Delivery country ID
        zone_id: Delivery zone/state ID
        postcode: Delivery postal code
        db: Database session
        
    Returns:
        ShippingMethodsResponse: Available shipping methods with costs
    """
    service = ShippingService(db)
    methods = service.get_methods(country_id, zone_id, postcode)
    return ShippingMethodsResponse(methods=methods)


# PUBLIC_INTERFACE
@router.post("/payment-methods", response_model=PaymentMethodsResponse, tags=["checkout"])
def get_payment_methods(
    db: Session = Depends(get_db)
):
    """
    Get available payment methods.
    
    Returns all available payment options for the store.
    
    Args:
        db: Database session
        
    Returns:
        PaymentMethodsResponse: Available payment methods
    """
    service = PaymentService(db)
    methods = service.get_methods()
    return PaymentMethodsResponse(methods=methods)


# PUBLIC_INTERFACE
@router.post("/confirm", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED, tags=["checkout"])
def confirm_order(
    order_data: OrderCreate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Place order and complete checkout.
    
    Creates an order from the current cart with the specified
    shipping/payment details. Cart is cleared upon successful order creation.
    
    Args:
        order_data: Order details (addresses, methods, comment)
        current_customer: Authenticated customer
        db: Database session
        
    Returns:
        OrderCreateResponse: Created order details
        
    Raises:
        HTTPException 400: If cart is empty
    """
    service = OrderService(db)
    result = service.create_order(current_customer.customer_id, order_data.dict())
    return OrderCreateResponse(**result)
