"""
Tax Service
Business logic for tax calculations
"""
from sqlalchemy.orm import Session


class TaxService:
    """Service for tax calculations."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def calculate(self, customer_id: int, subtotal: float, shipping: float) -> float:
        """
        Calculate tax for order.
        
        Args:
            customer_id: Customer ID
            subtotal: Order subtotal
            shipping: Shipping cost
            
        Returns:
            float: Tax amount
        """
        # Simplified tax calculation - 10% on subtotal
        return subtotal * 0.1
