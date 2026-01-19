"""
Product Service
Business logic for product operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.schemas.product import ProductDetail, ProductResponse
from app.utils.exceptions import ProductNotFoundException


class ProductService:
    """Service for product business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = ProductRepository(db)
        self.db = db
    
    # PUBLIC_INTERFACE
    def get_products(
        self,
        page: int = 1,
        limit: int = 20,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        sort: str = "sort_order",
        order: str = "asc"
    ) -> dict:
        """
        Get paginated product list with filtering.
        
        Args:
            page: Page number
            limit: Items per page
            category_id: Filter by category
            search: Search term
            sort: Sort field
            order: Sort order
            
        Returns:
            dict: Paginated product list with metadata
        """
        offset = (page - 1) * limit
        
        products = self.repository.find_all(
            category_id=category_id,
            search=search,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset
        )
        
        total = self.repository.count(category_id=category_id, search=search)
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        # Build response items
        items = []
        for product in products:
            # Get primary description
            desc = next((d for d in product.descriptions if d.language_id == 1), None)
            if desc:
                items.append(ProductResponse(
                    product_id=product.product_id,
                    name=desc.name,
                    model=product.model,
                    price=product.price,
                    image=product.image,
                    special_price=None,  # Would calculate from oc_product_special
                    rating=None,  # Would calculate from oc_review
                    reviews_count=0
                ))
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }
    
    # PUBLIC_INTERFACE
    def get_product_detail(self, product_id: int) -> ProductDetail:
        """
        Get detailed product information.
        
        Args:
            product_id: Product ID
            
        Returns:
            ProductDetail: Detailed product data
            
        Raises:
            ProductNotFoundException: If product not found
        """
        product = self.repository.find_by_id(product_id)
        if not product or product.status != 1:
            raise ProductNotFoundException(product_id)
        
        # Get primary description
        desc = next((d for d in product.descriptions if d.language_id == 1), None)
        if not desc:
            raise ProductNotFoundException(product_id)
        
        # Get images
        images = self.repository.get_images(product_id)
        
        # Get options
        options = self.repository.get_options(product_id)
        
        # Get related products
        related = self.repository.get_related(product_id)
        
        # Increment view count
        product.viewed += 1
        self.db.commit()
        
        return ProductDetail(
            product_id=product.product_id,
            name=desc.name,
            model=product.model,
            description=desc.description or "",
            price=product.price,
            special_price=None,  # Would calculate from oc_product_special
            tax=0.0,  # Would calculate based on tax_class_id
            quantity=product.quantity,
            minimum=product.minimum,
            image=product.image,
            images=images,
            manufacturer=None,  # Would join oc_manufacturer
            sku=product.sku,
            options=options,
            related_products=related,
            rating=None,
            reviews_count=0
        )
