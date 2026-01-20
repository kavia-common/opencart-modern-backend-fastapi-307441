"""
Checkout Endpoints
Checkout and order placement operations
"""
from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_customer
from app.core.database import get_db
from app.models.database.customer import Customer
from app.models.schemas.order import (
    OrderCreate,
    OrderCreateResponse,
    PaymentMethodsResponse,
    ShippingMethodsResponse,
)
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.shipping_service import ShippingService

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/shipping-methods",
    response_model=ShippingMethodsResponse,
    tags=["checkout"],
    summary="List shipping methods",
    description="Return available shipping methods given destination address parameters.",
    operation_id="getShippingMethods",
)
def get_shipping_methods(
    country_id: int = Body(..., embed=True),
    zone_id: int = Body(..., embed=True),
    postcode: str = Body(..., embed=True),
    db: Session = Depends(get_db),
) -> ShippingMethodsResponse:
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
@router.post(
    "/payment-methods",
    response_model=PaymentMethodsResponse,
    tags=["checkout"],
    summary="List payment methods",
    description="Return available payment methods for the store.",
    operation_id="getPaymentMethods",
)
def get_payment_methods(
    db: Session = Depends(get_db),
) -> PaymentMethodsResponse:
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
@router.post(
    "/confirm",
    response_model=OrderCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["checkout"],
    summary="Confirm and place order",
    description="Create an order from the authenticated customer's current cart and clear the cart upon success.",
    operation_id="confirmOrder",
)
def confirm_order(
    order_data: OrderCreate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> OrderCreateResponse:
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
