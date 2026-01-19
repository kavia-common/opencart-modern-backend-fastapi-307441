"""
Product Endpoints
Product catalog operations
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.product_service import ProductService
from app.models.schemas.product import ProductListResponse, ProductDetail
from app.core.config import settings

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("", response_model=ProductListResponse, tags=["products"])
def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Items per page"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search term for product name/description"),
    sort: str = Query("sort_order", description="Sort field: name, price, date, sort_order"),
    order: str = Query("asc", description="Sort order: asc, desc"),
    db: Session = Depends(get_db)
):
    """
    List products with pagination and filtering.
    
    Returns a paginated list of products with optional filtering by category,
    search term, and custom sorting.
    
    Args:
        page: Page number (1-indexed)
        limit: Number of items per page
        category_id: Optional category filter
        search: Optional search term
        sort: Sort field
        order: Sort order (asc/desc)
        db: Database session
        
    Returns:
        ProductListResponse: Paginated product list with metadata
    """
    service = ProductService(db)
    return service.get_products(
        page=page,
        limit=limit,
        category_id=category_id,
        search=search,
        sort=sort,
        order=order
    )


# PUBLIC_INTERFACE
@router.get("/{product_id}", response_model=ProductDetail, tags=["products"])
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed product information.
    
    Returns comprehensive product data including description, images,
    options, pricing, and related products.
    
    Args:
        product_id: Product ID
        db: Database session
        
    Returns:
        ProductDetail: Detailed product information
        
    Raises:
        HTTPException 404: If product not found
    """
    service = ProductService(db)
    return service.get_product_detail(product_id)
