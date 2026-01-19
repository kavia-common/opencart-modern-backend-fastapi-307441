"""
Customer Service
Business logic for customer operations
"""
from sqlalchemy.orm import Session
from app.repositories.customer_repository import CustomerRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.schemas.auth import CustomerResponse, TokenResponse
from app.models.database.customer import Customer
from app.utils.exceptions import InvalidCredentialsException
from datetime import timedelta
from app.core.config import settings


class CustomerService:
    """Service for customer business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = CustomerRepository(db)
    
    # PUBLIC_INTERFACE
    def register_customer(self, customer_data: dict) -> CustomerResponse:
        """
        Register a new customer.
        
        Args:
            customer_data: Customer registration data
            
        Returns:
            CustomerResponse: Created customer data
            
        Raises:
            HTTPException: If email already exists
        """
        from fastapi import HTTPException, status
        
        # Check if email exists
        existing = self.repository.find_by_email(customer_data["email"])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(customer_data["password"])
        
        # Create customer
        customer = self.repository.create({
            **customer_data,
            "password": hashed_password
        })
        
        return CustomerResponse(
            customer_id=customer.customer_id,
            email=customer.email,
            firstname=customer.firstname,
            lastname=customer.lastname,
            telephone=customer.telephone
        )
    
    # PUBLIC_INTERFACE
    def authenticate_customer(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate customer and return token.
        
        Args:
            email: Customer email
            password: Plain password
            
        Returns:
            TokenResponse: JWT token and customer data
            
        Raises:
            InvalidCredentialsException: If credentials invalid
        """
        # Find customer
        customer = self.repository.find_by_email(email)
        if not customer:
            raise InvalidCredentialsException()
        
        # Verify password
        if not verify_password(password, customer.password):
            raise InvalidCredentialsException()
        
        # Check if customer is active
        if not customer.status or not customer.approved:
            raise InvalidCredentialsException()
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(customer.customer_id)},
            expires_delta=access_token_expires
        )
        
        customer_response = CustomerResponse(
            customer_id=customer.customer_id,
            email=customer.email,
            firstname=customer.firstname,
            lastname=customer.lastname,
            telephone=customer.telephone
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            customer=customer_response
        )
