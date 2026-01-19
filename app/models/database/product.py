"""
Product Database Models
SQLAlchemy ORM models for product-related tables
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    """Product main table."""
    __tablename__ = "oc_product"
    
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model = Column(String(64), nullable=False)
    sku = Column(String(64))
    upc = Column(String(12))
    ean = Column(String(14))
    jan = Column(String(13))
    isbn = Column(String(17))
    mpn = Column(String(64))
    location = Column(String(128))
    quantity = Column(Integer, default=0)
    stock_status_id = Column(Integer)
    image = Column(String(255))
    manufacturer_id = Column(Integer)
    shipping = Column(Integer, default=1)
    price = Column(Float, default=0.0)
    points = Column(Integer, default=0)
    tax_class_id = Column(Integer)
    date_available = Column(Text)
    weight = Column(Float, default=0.0)
    weight_class_id = Column(Integer, default=0)
    length = Column(Float, default=0.0)
    width = Column(Float, default=0.0)
    height = Column(Float, default=0.0)
    length_class_id = Column(Integer, default=0)
    subtract = Column(Integer, default=1)
    minimum = Column(Integer, default=1)
    sort_order = Column(Integer, default=0)
    status = Column(Integer, default=0)
    viewed = Column(Integer, default=0)
    date_added = Column(Text, nullable=False)
    date_modified = Column(Text, nullable=False)
    
    # Relationships
    descriptions = relationship("ProductDescription", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    categories = relationship("ProductToCategory", back_populates="product", cascade="all, delete-orphan")


class ProductDescription(Base):
    """Product description and localization."""
    __tablename__ = "oc_product_description"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id", ondelete="CASCADE"), primary_key=True)
    language_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tag = Column(Text)
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    meta_keyword = Column(String(255))
    
    # Relationship
    product = relationship("Product", back_populates="descriptions")


class ProductImage(Base):
    """Product additional images."""
    __tablename__ = "oc_product_image"
    
    product_image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("oc_product.product_id", ondelete="CASCADE"), nullable=False)
    image = Column(String(255))
    sort_order = Column(Integer, default=0)
    
    # Relationship
    product = relationship("Product", back_populates="images")


class ProductToCategory(Base):
    """Product to category mapping."""
    __tablename__ = "oc_product_to_category"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("oc_category.category_id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    product = relationship("Product", back_populates="categories")
    category = relationship("Category", back_populates="products")
