"""
Customer Database Models
SQLAlchemy ORM models for customer-related tables
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Customer(Base):
    """Customer main table."""
    __tablename__ = "oc_customer"
    
    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_group_id = Column(Integer, nullable=False, default=1)
    store_id = Column(Integer, default=0)
    language_id = Column(Integer, nullable=False, default=1)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    email = Column(String(96), nullable=False, unique=True, index=True)
    telephone = Column(String(32), nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String(9))
    newsletter = Column(Integer, default=0)
    status = Column(Integer, nullable=False, default=1)
    approved = Column(Integer, nullable=False, default=1)
    safe = Column(Integer, nullable=False, default=0)
    token = Column(Text)
    ip = Column(String(40))
    date_added = Column(Text, nullable=False)
    
    # Relationships
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer")


class Address(Base):
    """Customer address table."""
    __tablename__ = "oc_address"
    
    address_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("oc_customer.customer_id", ondelete="CASCADE"), nullable=False)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    company = Column(String(60))
    address_1 = Column(String(128), nullable=False)
    address_2 = Column(String(128))
    city = Column(String(128), nullable=False)
    postcode = Column(String(10), nullable=False)
    country_id = Column(Integer, nullable=False)
    zone_id = Column(Integer, nullable=False)
    is_default = Column(Integer, default=0)
    
    # Relationship
    customer = relationship("Customer", back_populates="addresses")
