"""
Cart Repository
Data access layer for cart operations
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database.cart import Cart
import json


class CartRepository:
    """Repository for cart data access."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def get_items(self, customer_id: int) -> List[Cart]:
        """
        Get all cart items for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Cart]: Cart items
        """
        return self.db.query(Cart).filter(
            Cart.customer_id == customer_id
        ).all()
    
    # PUBLIC_INTERFACE
    def find_by_product(
        self,
        customer_id: int,
        product_id: int,
        options: dict
    ) -> Optional[Cart]:
        """
        Find cart item by product and options.
        
        Args:
            customer_id: Customer ID
            product_id: Product ID
            options: Product options
            
        Returns:
            Optional[Cart]: Cart item if exists
        """
        option_str = json.dumps(options, sort_keys=True) if options else ""
        
        return self.db.query(Cart).filter(
            and_(
                Cart.customer_id == customer_id,
                Cart.product_id == product_id,
                Cart.option_data == option_str
            )
        ).first()
    
    # PUBLIC_INTERFACE
    def create(
        self,
        customer_id: int,
        product_id: int,
        quantity: int,
        options: dict
    ) -> Cart:
        """
        Create a new cart item.
        
        Args:
            customer_id: Customer ID
            product_id: Product ID
            quantity: Quantity
            options: Product options
            
        Returns:
            Cart: Created cart item
        """
        from datetime import datetime
        
        option_str = json.dumps(options) if options else ""
        
        cart_item = Cart(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            option_data=option_str,
            date_added=datetime.utcnow().isoformat()
        )
        
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        
        return cart_item
    
    # PUBLIC_INTERFACE
    def update_quantity(self, cart_id: int, quantity: int) -> None:
        """
        Update cart item quantity.
        
        Args:
            cart_id: Cart item ID
            quantity: New quantity
        """
        cart_item = self.db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart_item:
            cart_item.quantity = quantity
            self.db.commit()
    
    # PUBLIC_INTERFACE
    def delete(self, cart_id: int) -> None:
        """
        Delete a cart item.
        
        Args:
            cart_id: Cart item ID
        """
        cart_item = self.db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()
    
    # PUBLIC_INTERFACE
    def clear_cart(self, customer_id: int) -> None:
        """
        Clear all items from customer's cart.
        
        Args:
            customer_id: Customer ID
        """
        self.db.query(Cart).filter(Cart.customer_id == customer_id).delete()
        self.db.commit()
