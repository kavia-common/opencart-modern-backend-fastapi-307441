"""
Authentication Endpoints
Customer registration and login
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.schemas.auth import CustomerLogin, CustomerRegister, CustomerResponse, TokenResponse
from app.services.customer_service import CustomerService

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/register",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
    summary="Register a customer",
    description="Create a new customer account and return the created customer profile.",
    operation_id="registerCustomer",
)
def register_customer(
    customer_data: CustomerRegister,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    """
    Register a new customer account.

    Creates a new customer with the provided registration data.
    Password is automatically hashed before storage.

    Args:
        customer_data: Customer registration information
        db: Database session

    Returns:
        CustomerResponse: Created customer data (without password)

    Raises:
        HTTPException 400: If email already exists
    """
    service = CustomerService(db)
    return service.register_customer(customer_data.model_dump())


# PUBLIC_INTERFACE
@router.post(
    "/login",
    response_model=TokenResponse,
    tags=["auth"],
    summary="Login",
    description="Authenticate a customer and return a JWT bearer token.",
    operation_id="loginCustomer",
)
def login_customer(
    credentials: CustomerLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate customer and return JWT access token.

    Validates customer credentials and returns a JWT bearer token
    for subsequent authenticated requests.

    Args:
        credentials: Customer email and password
        db: Database session

    Returns:
        TokenResponse: JWT token and customer data

    Raises:
        HTTPException 401: If credentials are invalid
    """
    service = CustomerService(db)
    return service.authenticate_customer(credentials.email, credentials.password)
