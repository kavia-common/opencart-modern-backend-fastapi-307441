"""
Customer Repository
Data access layer for customer operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database.customer import Customer, Address


class CustomerRepository:
    """Repository for customer data access."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Find customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Optional[Customer]: Customer if found
        """
        return self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
    
    # PUBLIC_INTERFACE
    def find_by_email(self, email: str) -> Optional[Customer]:
        """
        Find customer by email.
        
        Args:
            email: Customer email
            
        Returns:
            Optional[Customer]: Customer if found
        """
        return self.db.query(Customer).filter(
            Customer.email == email
        ).first()
    
    # PUBLIC_INTERFACE
    def create(self, customer_data: dict) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer data dictionary
            
        Returns:
            Customer: Created customer
        """
        from datetime import datetime
        
        customer = Customer(
            firstname=customer_data["firstname"],
            lastname=customer_data["lastname"],
            email=customer_data["email"],
            telephone=customer_data["telephone"],
            password=customer_data["password"],
            customer_group_id=1,
            language_id=1,
            status=1,
            approved=1,
            safe=0,
            date_added=datetime.utcnow().isoformat()
        )
        
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        
        return customer
