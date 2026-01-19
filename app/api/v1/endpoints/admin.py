"""
Admin Endpoints
Administrative operations
"""
from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.repositories.order_repository import OrderRepository
from app.models.schemas.order import OrderListResponse, OrderResponse
from app.models.database.customer import Customer

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/orders", response_model=OrderListResponse, tags=["admin"])
def list_all_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_admin: Customer = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all orders (admin view).
    
    Returns paginated list of all orders in the system.
    Requires admin authentication.
    
    Args:
        page: Page number
        limit: Items per page
        current_admin: Authenticated admin user
        db: Database session
        
    Returns:
        OrderListResponse: List of all orders
    """
    repository = OrderRepository(db)
    offset = (page - 1) * limit
    orders = repository.find_all(limit=limit, offset=offset)
    
    result = []
    for order in orders:
        status_name = "Pending" if order.order_status_id == 1 else "Processing"
        result.append(OrderResponse(
            order_id=order.order_id,
            invoice_no=order.invoice_no,
            status=status_name,
            total=order.total,
            date_added=order.date_added
        ))
    
    return OrderListResponse(orders=result, total=len(result), page=page)


# PUBLIC_INTERFACE
@router.put("/orders/{order_id}/status", tags=["admin"])
def update_order_status(
    order_id: int,
    order_status_id: int = Body(..., embed=True),
    current_admin: Customer = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update order status.
    
    Changes the status of an order. Requires admin authentication.
    
    Args:
        order_id: Order ID
        order_status_id: New status ID
        current_admin: Authenticated admin user
        db: Database session
        
    Returns:
        dict: Confirmation message
    """
    repository = OrderRepository(db)
    repository.update_status(order_id, order_status_id)
    return {"message": "Order status updated"}
