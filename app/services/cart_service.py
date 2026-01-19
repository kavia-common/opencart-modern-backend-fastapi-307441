"""
Cart Service
Business logic for cart operations
"""
from typing import List
from sqlalchemy.orm import Session
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.models.schemas.cart import CartResponse, CartItemResponse, CartTotalLine, CartItemOption
from app.utils.exceptions import ProductNotFoundException, InsufficientStockException


class CartService:
    """Service for cart business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.db = db
    
    # PUBLIC_INTERFACE
    def add_item(self, customer_id: int, product_id: int, quantity: int, options: dict) -> int:
        """
        Add product to cart.
        
        Args:
            customer_id: Customer ID
            product_id: Product ID
            quantity: Quantity to add
            options: Product options
            
        Returns:
            int: Cart item ID
            
        Raises:
            ProductNotFoundException: If product not found
            InsufficientStockException: If not enough stock
        """
        # Validate product exists and is available
        product = self.product_repo.find_by_id(product_id)
        if not product or product.status != 1:
            raise ProductNotFoundException(product_id)
        
        # Check stock
        if product.subtract and product.quantity < quantity:
            raise InsufficientStockException(product_id, product.quantity)
        
        # Check if item already in cart
        existing = self.cart_repo.find_by_product(customer_id, product_id, options)
        if existing:
            new_quantity = existing.quantity + quantity
            # Recheck stock for new quantity
            if product.subtract and product.quantity < new_quantity:
                raise InsufficientStockException(product_id, product.quantity)
            self.cart_repo.update_quantity(existing.cart_id, new_quantity)
            return existing.cart_id
        else:
            cart_item = self.cart_repo.create(customer_id, product_id, quantity, options)
            return cart_item.cart_id
    
    # PUBLIC_INTERFACE
    def get_cart(self, customer_id: int) -> CartResponse:
        """
        Get cart with calculated totals.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            CartResponse: Cart data with items and totals
        """
        cart_items = self.cart_repo.get_items(customer_id)
        
        items = []
        subtotal = 0.0
        
        for cart_item in cart_items:
            # Get product details
            product = self.product_repo.find_by_id(cart_item.product_id)
            if not product:
                continue
            
            # Get description
            desc = next((d for d in product.descriptions if d.language_id == 1), None)
            if not desc:
                continue
            
            item_total = product.price * cart_item.quantity
            subtotal += item_total
            
            items.append(CartItemResponse(
                cart_id=cart_item.cart_id,
                product_id=cart_item.product_id,
                name=desc.name,
                model=product.model,
                image=product.image,
                quantity=cart_item.quantity,
                price=product.price,
                total=item_total,
                options=[]  # Would parse from cart_item.option_data
            ))
        
        # Calculate totals (simplified)
        shipping = 5.00 if subtotal > 0 else 0.0
        tax = subtotal * 0.1  # 10% tax rate (simplified)
        total = subtotal + shipping + tax
        
        totals = [
            CartTotalLine(code="sub_total", title="Sub-Total", value=subtotal),
            CartTotalLine(code="shipping", title="Flat Shipping Rate", value=shipping),
            CartTotalLine(code="tax", title="Tax", value=tax),
            CartTotalLine(code="total", title="Total", value=total)
        ]
        
        return CartResponse(items=items, totals=totals)
    
    # PUBLIC_INTERFACE
    def update_item(self, cart_id: int, quantity: int, customer_id: int) -> None:
        """
        Update cart item quantity.
        
        Args:
            cart_id: Cart item ID
            quantity: New quantity
            customer_id: Customer ID (for authorization)
        """
        # TODO: Verify cart item belongs to customer
        self.cart_repo.update_quantity(cart_id, quantity)
    
    # PUBLIC_INTERFACE
    def remove_item(self, cart_id: int, customer_id: int) -> None:
        """
        Remove item from cart.
        
        Args:
            cart_id: Cart item ID
            customer_id: Customer ID (for authorization)
        """
        # TODO: Verify cart item belongs to customer
        self.cart_repo.delete(cart_id)
    
    # PUBLIC_INTERFACE
    def clear_cart(self, customer_id: int) -> None:
        """
        Clear all items from cart.
        
        Args:
            customer_id: Customer ID
        """
        self.cart_repo.clear_cart(customer_id)
