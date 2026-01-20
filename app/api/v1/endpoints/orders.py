"""
Order Endpoints
Order history and details operations
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_customer
from app.core.database import get_db
from app.models.database.customer import Customer
from app.models.schemas.order import OrderDetailResponse, OrderListResponse
from app.services.order_service import OrderService

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=OrderListResponse,
    tags=["orders"],
    summary="List my orders",
    description="Return the authenticated customer's order history (newest first).",
    operation_id="listOrders",
)
def list_orders(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> OrderListResponse:
    """
    List customer's order history.

    Returns all orders placed by the authenticated customer,
    sorted by date (newest first).

    Args:
        current_customer: Authenticated customer
        db: Database session

    Returns:
        OrderListResponse: List of customer orders
    """
    service = OrderService(db)
    orders = service.get_customer_orders(current_customer.customer_id)
    return OrderListResponse(orders=orders, total=len(orders))


# PUBLIC_INTERFACE
@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse,
    tags=["orders"],
    summary="Get order detail",
    description="Return detailed information for a single order belonging to the authenticated customer.",
    operation_id="getOrderDetail",
)
def get_order_detail(
    order_id: int,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
) -> OrderDetailResponse:
    """
    Get detailed order information.

    Returns comprehensive order data including products, addresses,
    totals breakdown, and current status.

    Args:
        order_id: Order ID
        current_customer: Authenticated customer
        db: Database session

    Returns:
        OrderDetailResponse: Detailed order information

    Raises:
        HTTPException 404: If order not found or unauthorized
    """
    service = OrderService(db)
    return service.get_order_detail(order_id, current_customer.customer_id)
