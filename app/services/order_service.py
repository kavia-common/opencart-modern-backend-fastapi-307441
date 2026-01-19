"""
Order Service
Business logic for order operations
"""
from typing import List
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.customer_repository import CustomerRepository
from app.services.cart_service import CartService
from app.models.schemas.order import OrderDetailResponse, OrderResponse, OrderProductResponse, OrderTotalResponse
from app.utils.exceptions import EmptyCartException, OrderNotFoundException


class OrderService:
    """Service for order business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = OrderRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.cart_service = CartService(db)
        self.db = db
    
    # PUBLIC_INTERFACE
    def create_order(self, customer_id: int, order_data: dict) -> dict:
        """
        Create order from cart.
        
        Args:
            customer_id: Customer ID
            order_data: Order details (addresses, methods)
            
        Returns:
            dict: Order creation result
            
        Raises:
            EmptyCartException: If cart is empty
        """
        # Get cart
        cart = self.cart_service.get_cart(customer_id)
        
        if not cart.items:
            raise EmptyCartException()
        
        # Get customer
        customer = self.customer_repo.find_by_id(customer_id)
        
        # Prepare order data
        order_dict = {
            "customer_id": customer_id,
            "firstname": order_data["payment_address"]["firstname"],
            "lastname": order_data["payment_address"]["lastname"],
            "email": customer.email,
            "telephone": customer.telephone,
            "payment_address_1": order_data["payment_address"]["address_1"],
            "payment_city": order_data["payment_address"]["city"],
            "payment_method": order_data["payment_method"],
            "shipping_method": order_data["shipping_method"],
            "total": cart.totals[-1].value,
            "order_status_id": 1  # Pending
        }
        
        # Create order in transaction
        order_id = self.repository.create_order(order_dict, cart.items, cart.totals)
        
        # Clear cart
        self.cart_service.clear_cart(customer_id)
        
        return {
            "order_id": order_id,
            "invoice_no": 1000 + order_id,
            "total": order_dict["total"]
        }
    
    # PUBLIC_INTERFACE
    def get_customer_orders(self, customer_id: int) -> List[OrderResponse]:
        """
        Get customer's order history.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[OrderResponse]: Customer orders
        """
        orders = self.repository.find_by_customer(customer_id)
        
        result = []
        for order in orders:
            # Get status name (simplified)
            status_name = "Pending" if order.order_status_id == 1 else "Processing"
            
            result.append(OrderResponse(
                order_id=order.order_id,
                invoice_no=order.invoice_no,
                status=status_name,
                total=order.total,
                date_added=order.date_added
            ))
        
        return result
    
    # PUBLIC_INTERFACE
    def get_order_detail(self, order_id: int, customer_id: int) -> OrderDetailResponse:
        """
        Get detailed order information.
        
        Args:
            order_id: Order ID
            customer_id: Customer ID (for authorization)
            
        Returns:
            OrderDetailResponse: Detailed order data
            
        Raises:
            OrderNotFoundException: If order not found or unauthorized
        """
        order = self.repository.find_by_id(order_id)
        
        if not order or order.customer_id != customer_id:
            raise OrderNotFoundException(order_id)
        
        # Build products list
        products = [
            OrderProductResponse(
                name=p.name,
                model=p.model,
                quantity=p.quantity,
                price=p.price,
                total=p.total
            )
            for p in order.products
        ]
        
        # Build totals list
        totals = [
            OrderTotalResponse(title=t.title, value=t.value)
            for t in sorted(order.totals, key=lambda x: x.sort_order)
        ]
        
        # Get status name
        status_name = "Pending" if order.order_status_id == 1 else "Processing"
        
        return OrderDetailResponse(
            order_id=order.order_id,
            invoice_no=order.invoice_no,
            status=status_name,
            customer={
                "firstname": order.firstname,
                "lastname": order.lastname,
                "email": order.email
            },
            payment_address={
                "firstname": order.payment_firstname or order.firstname,
                "lastname": order.payment_lastname or order.lastname,
                "address_1": order.payment_address_1 or "",
                "city": order.payment_city or ""
            },
            shipping_address=None,  # Would populate if different
            products=products,
            totals=totals,
            date_added=order.date_added
        )
