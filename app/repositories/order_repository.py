"""
Order Repository
Data access layer for order operations
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.database.order import Order, OrderProduct, OrderTotal


class OrderRepository:
    """Repository for order data access."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def find_by_customer(self, customer_id: int) -> List[Order]:
        """
        Find all orders for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Order]: Customer's orders
        """
        return self.db.query(Order).filter(
            Order.customer_id == customer_id
        ).order_by(Order.date_added.desc()).all()
    
    # PUBLIC_INTERFACE
    def find_by_id(self, order_id: int) -> Optional[Order]:
        """
        Find order by ID with related data.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Order]: Order if found
        """
        return self.db.query(Order).options(
            joinedload(Order.products),
            joinedload(Order.totals)
        ).filter(Order.order_id == order_id).first()
    
    # PUBLIC_INTERFACE
    def create_order(self, order_data: dict, items: List[dict], totals: List[dict]) -> int:
        """
        Create a new order with products and totals.
        
        Args:
            order_data: Order data dictionary
            items: List of cart items
            totals: List of total lines
            
        Returns:
            int: Created order ID
        """
        from datetime import datetime
        
        now = datetime.utcnow().isoformat()
        
        # Create order
        order = Order(
            customer_id=order_data["customer_id"],
            firstname=order_data["firstname"],
            lastname=order_data["lastname"],
            email=order_data["email"],
            telephone=order_data.get("telephone", ""),
            payment_address_1=order_data.get("payment_address_1", ""),
            payment_city=order_data.get("payment_city", ""),
            payment_method=order_data.get("payment_method", ""),
            shipping_method=order_data.get("shipping_method", ""),
            total=order_data["total"],
            order_status_id=order_data.get("order_status_id", 1),
            currency_code="USD",
            currency_value=1.0,
            date_added=now,
            date_modified=now
        )
        
        self.db.add(order)
        self.db.flush()
        
        # Assign invoice number
        order.invoice_no = 1000 + order.order_id
        
        # Add order products
        for item in items:
            order_product = OrderProduct(
                order_id=order.order_id,
                product_id=item.product_id,
                name=item.name if hasattr(item, 'name') else "Product",
                model=item.model if hasattr(item, 'model') else "",
                quantity=item.quantity,
                price=item.price if hasattr(item, 'price') else 0.0,
                total=item.total if hasattr(item, 'total') else 0.0,
                tax=0.0
            )
            self.db.add(order_product)
        
        # Add order totals
        for idx, total in enumerate(totals):
            order_total = OrderTotal(
                order_id=order.order_id,
                code=total["code"],
                title=total["title"],
                value=total["value"],
                sort_order=idx
            )
            self.db.add(order_total)
        
        self.db.commit()
        self.db.refresh(order)
        
        return order.order_id
    
    # PUBLIC_INTERFACE
    def find_all(self, limit: int = 50, offset: int = 0) -> List[Order]:
        """
        Find all orders (admin view).
        
        Args:
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            List[Order]: Orders
        """
        return self.db.query(Order).order_by(
            Order.date_added.desc()
        ).offset(offset).limit(limit).all()
    
    # PUBLIC_INTERFACE
    def update_status(self, order_id: int, status_id: int) -> None:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            status_id: New status ID
        """
        from datetime import datetime
        
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if order:
            order.order_status_id = status_id
            order.date_modified = datetime.utcnow().isoformat()
            self.db.commit()
