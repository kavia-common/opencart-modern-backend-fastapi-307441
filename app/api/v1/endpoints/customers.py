"""
Customer Endpoints
Customer profile operations
"""
from fastapi import APIRouter, Depends
from app.api.deps import get_current_customer
from app.models.schemas.auth import CustomerResponse
from app.models.database.customer import Customer

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/profile", response_model=CustomerResponse, tags=["customers"])
def get_customer_profile(
    current_customer: Customer = Depends(get_current_customer)
):
    """
    Get current customer profile.
    
    Returns the authenticated customer's profile information.
    
    Args:
        current_customer: Authenticated customer
        
    Returns:
        CustomerResponse: Customer profile data
    """
    return CustomerResponse(
        customer_id=current_customer.customer_id,
        email=current_customer.email,
        firstname=current_customer.firstname,
        lastname=current_customer.lastname,
        telephone=current_customer.telephone
    )
