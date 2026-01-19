"""
Cart Database Models
SQLAlchemy ORM models for cart-related tables
"""
from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Cart(Base):
    """Shopping cart table."""
    __tablename__ = "oc_cart"
    
    cart_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, default=0, index=True)
    session_id = Column(String(32), index=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    option_data = Column(Text)  # JSON string of product options
    date_added = Column(Text, nullable=False)
