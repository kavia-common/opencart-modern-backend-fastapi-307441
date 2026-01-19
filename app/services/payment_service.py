"""
Payment Service
Business logic for payment methods
"""
from typing import List
from sqlalchemy.orm import Session


class PaymentService:
    """Service for payment methods."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def get_methods(self) -> List[dict]:
        """
        Get available payment methods.
        
        Returns:
            List[dict]: Available payment methods
        """
        # Simplified - return fixed methods
        return [
            {
                "code": "bank_transfer",
                "title": "Bank Transfer"
            },
            {
                "code": "cod",
                "title": "Cash On Delivery"
            }
        ]
