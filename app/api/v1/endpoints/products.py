"""
Product Endpoints
Product catalog operations
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.schemas.product import ProductDetail, ProductListResponse
from app.services.product_service import ProductService

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=ProductListResponse,
    tags=["products"],
    summary="List products",
    description="List products with pagination, optional filtering, and sorting.",
    operation_id="listProducts",
)
def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Items per page",
    ),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search term for product name/description"),
    sort: str = Query("sort_order", description="Sort field: name, price, date, sort_order"),
    order: str = Query("asc", description="Sort order: asc, desc"),
    db: Session = Depends(get_db),
) -> ProductListResponse:
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
        order=order,
    )


# PUBLIC_INTERFACE
@router.get(
    "/{product_id}",
    response_model=ProductDetail,
    tags=["products"],
    summary="Get product detail",
    description="Get detailed information for a single product by product_id.",
    operation_id="getProductDetail",
)
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductDetail:
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
