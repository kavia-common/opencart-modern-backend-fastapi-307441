"""
API Dependencies
Dependency injection for API endpoints
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.customer_repository import CustomerRepository
from app.models.database.customer import Customer

security = HTTPBearer()


# PUBLIC_INTERFACE
def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Customer:
    """
    Get current authenticated customer from JWT token.
    
    Args:
        credentials: HTTP bearer credentials
        db: Database session
        
    Returns:
        Customer: Authenticated customer
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    customer_id = payload.get("sub")
    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    customer_repo = CustomerRepository(db)
    customer = customer_repo.find_by_id(int(customer_id))
    
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return customer


# PUBLIC_INTERFACE
def get_current_admin(
    customer: Customer = Depends(get_current_customer)
) -> Customer:
    """
    Verify customer has admin privileges.
    
    Args:
        customer: Current authenticated customer
        
    Returns:
        Customer: Admin customer
        
    Raises:
        HTTPException: If not admin
    """
    if customer.customer_group_id != 1:  # Admin group
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return customer
