"""
Product Repository
Data access layer for product operations
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from app.models.database.product import Product, ProductDescription, ProductImage, ProductToCategory
from app.models.database.category import Category


class ProductRepository:
    """Repository for product data access."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    # PUBLIC_INTERFACE
    def find_all(
        self,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        sort: str = "sort_order",
        order: str = "asc",
        limit: int = 20,
        offset: int = 0,
        language_id: int = 1
    ) -> List[Product]:
        """
        Find all products with filtering and pagination.
        
        Args:
            category_id: Filter by category
            search: Search term for product name/description
            sort: Sort field
            order: Sort order (asc/desc)
            limit: Maximum results
            offset: Pagination offset
            language_id: Language for descriptions
            
        Returns:
            List of Product objects
        """
        query = self.db.query(Product).join(ProductDescription).filter(
            ProductDescription.language_id == language_id,
            Product.status == 1
        )
        
        if category_id:
            query = query.join(ProductToCategory).filter(
                ProductToCategory.category_id == category_id
            )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ProductDescription.name.like(search_term),
                    ProductDescription.description.like(search_term),
                    Product.model.like(search_term)
                )
            )
        
        # Apply sorting
        if sort == "name":
            sort_col = ProductDescription.name
        elif sort == "price":
            sort_col = Product.price
        else:
            sort_col = Product.sort_order
        
        if order == "desc":
            query = query.order_by(sort_col.desc())
        else:
            query = query.order_by(sort_col.asc())
        
        return query.offset(offset).limit(limit).all()
    
    # PUBLIC_INTERFACE
    def count(
        self,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        language_id: int = 1
    ) -> int:
        """
        Count products matching filters.
        
        Args:
            category_id: Filter by category
            search: Search term
            language_id: Language for descriptions
            
        Returns:
            int: Count of matching products
        """
        query = self.db.query(Product).join(ProductDescription).filter(
            ProductDescription.language_id == language_id,
            Product.status == 1
        )
        
        if category_id:
            query = query.join(ProductToCategory).filter(
                ProductToCategory.category_id == category_id
            )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ProductDescription.name.like(search_term),
                    ProductDescription.description.like(search_term),
                    Product.model.like(search_term)
                )
            )
        
        return query.count()
    
    # PUBLIC_INTERFACE
    def find_by_id(self, product_id: int, language_id: int = 1) -> Optional[Product]:
        """
        Find product by ID.
        
        Args:
            product_id: Product ID
            language_id: Language for descriptions
            
        Returns:
            Optional[Product]: Product if found
        """
        return self.db.query(Product).options(
            joinedload(Product.descriptions),
            joinedload(Product.images)
        ).filter(Product.product_id == product_id).first()
    
    # PUBLIC_INTERFACE
    def get_images(self, product_id: int) -> List[str]:
        """
        Get product image URLs.
        
        Args:
            product_id: Product ID
            
        Returns:
            List[str]: Image URLs
        """
        images = self.db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).order_by(ProductImage.sort_order).all()
        
        return [img.image for img in images if img.image]
    
    # PUBLIC_INTERFACE
    def get_options(self, product_id: int) -> List[dict]:
        """
        Get product options (simplified for now).
        
        Args:
            product_id: Product ID
            
        Returns:
            List[dict]: Product options
        """
        # Placeholder - would query oc_product_option tables
        return []
    
    # PUBLIC_INTERFACE
    def get_related(self, product_id: int) -> List[int]:
        """
        Get related product IDs.
        
        Args:
            product_id: Product ID
            
        Returns:
            List[int]: Related product IDs
        """
        # Placeholder - would query oc_product_related table
        return []
    
    # PUBLIC_INTERFACE
    def create(self, product_data: dict, language_id: int = 1) -> Product:
        """
        Create a new product.
        
        Args:
            product_data: Product data dictionary
            language_id: Language for description
            
        Returns:
            Product: Created product
        """
        from datetime import datetime
        
        now = datetime.utcnow().isoformat()
        
        product = Product(
            model=product_data["model"],
            price=product_data.get("price", 0.0),
            quantity=product_data.get("quantity", 0),
            status=product_data.get("status", 1),
            image=product_data.get("image"),
            sku=product_data.get("sku"),
            manufacturer_id=product_data.get("manufacturer_id"),
            date_added=now,
            date_modified=now
        )
        
        self.db.add(product)
        self.db.flush()
        
        # Add description
        description = ProductDescription(
            product_id=product.product_id,
            language_id=language_id,
            name=product_data["name"],
            description=product_data.get("description", "")
        )
        
        self.db.add(description)
        self.db.commit()
        self.db.refresh(product)
        
        return product
