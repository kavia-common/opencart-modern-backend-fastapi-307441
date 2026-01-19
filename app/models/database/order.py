"""
Order Database Models
SQLAlchemy ORM models for order-related tables
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    """Order main table."""
    __tablename__ = "oc_order"
    
    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_no = Column(Integer, default=0)
    invoice_prefix = Column(String(26))
    store_id = Column(Integer, default=0)
    store_name = Column(String(64))
    store_url = Column(String(255))
    customer_id = Column(Integer, ForeignKey("oc_customer.customer_id"), nullable=False)
    customer_group_id = Column(Integer, default=0)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    email = Column(String(96), nullable=False)
    telephone = Column(String(32), nullable=False)
    payment_firstname = Column(String(32))
    payment_lastname = Column(String(32))
    payment_address_1 = Column(String(128))
    payment_city = Column(String(128))
    payment_postcode = Column(String(10))
    payment_country = Column(String(128))
    payment_method = Column(String(128))
    shipping_firstname = Column(String(32))
    shipping_lastname = Column(String(32))
    shipping_address_1 = Column(String(128))
    shipping_city = Column(String(128))
    shipping_postcode = Column(String(10))
    shipping_country = Column(String(128))
    shipping_method = Column(String(128))
    order_status_id = Column(Integer, default=0)
    currency_code = Column(String(3))
    currency_value = Column(Float, default=1.0)
    total = Column(Float, default=0.0)
    date_added = Column(Text, nullable=False)
    date_modified = Column(Text, nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    totals = relationship("OrderTotal", back_populates="order", cascade="all, delete-orphan")


class OrderProduct(Base):
    """Order products table."""
    __tablename__ = "oc_order_product"
    
    order_product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("oc_order.order_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    model = Column(String(64))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    
    # Relationship
    order = relationship("Order", back_populates="products")


class OrderTotal(Base):
    """Order totals breakdown table."""
    __tablename__ = "oc_order_total"
    
    order_total_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("oc_order.order_id", ondelete="CASCADE"), nullable=False)
    code = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    value = Column(Float, default=0.0)
    sort_order = Column(Integer, default=0)
    
    # Relationship
    order = relationship("Order", back_populates="totals")
