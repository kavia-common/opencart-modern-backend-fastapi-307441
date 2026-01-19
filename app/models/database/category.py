"""
Category Database Models
SQLAlchemy ORM models for category-related tables
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    """Category main table."""
    __tablename__ = "oc_category"
    
    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String(255))
    parent_id = Column(Integer, default=0)
    top = Column(Integer, default=0)
    column_count = Column(Integer, default=1)
    sort_order = Column(Integer, default=0)
    status = Column(Integer, default=1)
    date_added = Column(Text, nullable=False)
    date_modified = Column(Text, nullable=False)
    
    # Relationships
    descriptions = relationship("CategoryDescription", back_populates="category", cascade="all, delete-orphan")
    products = relationship("ProductToCategory", back_populates="category", cascade="all, delete-orphan")


class CategoryDescription(Base):
    """Category description and localization."""
    __tablename__ = "oc_category_description"
    
    category_id = Column(Integer, ForeignKey("oc_category.category_id", ondelete="CASCADE"), primary_key=True)
    language_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    meta_keyword = Column(String(255))
    
    # Relationship
    category = relationship("Category", back_populates="descriptions")
