# Low-Level Design - Backend Modules (FastAPI)

**Document**: Phase 4a - Backend Implementation Specifications  
**Migration**: OpenCart PHP → FastAPI Python Backend  
**Version**: 1.0  
**Date**: 2025-01-19

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Database Schema Design](#database-schema-design)
3. [API Endpoint Specifications](#api-endpoint-specifications)
4. [Pydantic Models](#pydantic-models)
5. [Business Logic Services](#business-logic-services)
6. [Authentication & Authorization](#authentication--authorization)
7. [Error Handling Strategy](#error-handling-strategy)
8. [Configuration Management](#configuration-management)

---

## Project Structure

### Directory Organization

```
opencart-modern-backend-fastapi-307441/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration settings
│   │   ├── security.py              # JWT handling, password hashing
│   │   ├── database.py              # Database connection and session
│   │   └── dependencies.py          # Dependency injection utilities
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database/                # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── product.py           # Product tables
│   │   │   ├── customer.py          # Customer tables
│   │   │   ├── order.py             # Order tables
│   │   │   ├── category.py          # Category tables
│   │   │   └── cart.py              # Cart tables
│   │   │
│   │   └── schemas/                 # Pydantic request/response models
│   │       ├── __init__.py
│   │       ├── product.py           # Product DTOs
│   │       ├── customer.py          # Customer DTOs
│   │       ├── order.py             # Order DTOs
│   │       ├── cart.py              # Cart DTOs
│   │       └── auth.py              # Auth DTOs
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                  # API dependencies (auth, db session)
│   │   │
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py            # Main API router
│   │       │
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py          # Authentication endpoints
│   │           ├── products.py      # Product endpoints
│   │           ├── categories.py    # Category endpoints
│   │           ├── cart.py          # Cart endpoints
│   │           ├── checkout.py      # Checkout endpoints
│   │           ├── orders.py        # Order endpoints
│   │           ├── customers.py     # Customer profile endpoints
│   │           └── admin.py         # Admin-specific endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py       # Product business logic
│   │   ├── cart_service.py          # Cart calculations and logic
│   │   ├── order_service.py         # Order processing logic
│   │   ├── customer_service.py      # Customer management logic
│   │   ├── payment_service.py       # Payment method handling
│   │   ├── shipping_service.py      # Shipping calculations
│   │   └── tax_service.py           # Tax calculations
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── product_repository.py    # Product data access
│   │   ├── cart_repository.py       # Cart data access
│   │   ├── order_repository.py      # Order data access
│   │   └── customer_repository.py   # Customer data access
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py            # Custom validation functions
│       ├── formatters.py            # Data formatting utilities
│       └── exceptions.py            # Custom exception classes
│
├── alembic/                         # Database migration tool
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_orders.py
│   └── test_auth.py
│
├── data/
│   └── opencart.db                  # SQLite database file
│
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── alembic.ini                     # Alembic configuration
└── README.md
```

### Key Design Patterns

**1. Layered Architecture**
- **API Layer**: FastAPI route handlers (thin layer)
- **Service Layer**: Business logic (thick layer)
- **Repository Layer**: Data access abstraction
- **Model Layer**: Database entities and DTOs

**2. Dependency Injection**
- Database sessions injected into endpoints
- Services injected with repository dependencies
- Repositories injected with database sessions

**3. Separation of Concerns**
- Routes handle HTTP concerns only
- Services contain all business logic
- Repositories handle database queries
- Models define data structure

---

## Database Schema Design

### SQLite Schema Structure

The database schema mirrors OpenCart's MySQL structure with SQLite-compatible adaptations.

### Core Tables

#### Product Tables

**oc_product**
```sql
CREATE TABLE oc_product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model VARCHAR(64) NOT NULL,
    sku VARCHAR(64),
    upc VARCHAR(12),
    ean VARCHAR(14),
    jan VARCHAR(13),
    isbn VARCHAR(17),
    mpn VARCHAR(64),
    location VARCHAR(128),
    quantity INTEGER DEFAULT 0,
    stock_status_id INTEGER,
    image VARCHAR(255),
    manufacturer_id INTEGER,
    shipping INTEGER DEFAULT 1,
    price REAL DEFAULT 0.0000,
    points INTEGER DEFAULT 0,
    tax_class_id INTEGER,
    date_available TEXT,
    weight REAL DEFAULT 0.0,
    weight_class_id INTEGER DEFAULT 0,
    length REAL DEFAULT 0.0,
    width REAL DEFAULT 0.0,
    height REAL DEFAULT 0.0,
    length_class_id INTEGER DEFAULT 0,
    subtract INTEGER DEFAULT 1,
    minimum INTEGER DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    status INTEGER DEFAULT 0,
    viewed INTEGER DEFAULT 0,
    date_added TEXT NOT NULL,
    date_modified TEXT NOT NULL
);
```

**oc_product_description**
```sql
CREATE TABLE oc_product_description (
    product_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tag TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(255),
    meta_keyword VARCHAR(255),
    PRIMARY KEY (product_id, language_id),
    FOREIGN KEY (product_id) REFERENCES oc_product(product_id) ON DELETE CASCADE
);
```

**oc_product_to_category**
```sql
CREATE TABLE oc_product_to_category (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES oc_product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES oc_category(category_id) ON DELETE CASCADE
);
```

**oc_product_image**
```sql
CREATE TABLE oc_product_image (
    product_image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    image VARCHAR(255),
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES oc_product(product_id) ON DELETE CASCADE
);
```

#### Customer Tables

**oc_customer**
```sql
CREATE TABLE oc_customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_group_id INTEGER NOT NULL,
    store_id INTEGER DEFAULT 0,
    language_id INTEGER NOT NULL,
    firstname VARCHAR(32) NOT NULL,
    lastname VARCHAR(32) NOT NULL,
    email VARCHAR(96) NOT NULL UNIQUE,
    telephone VARCHAR(32) NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(9),
    newsletter INTEGER DEFAULT 0,
    status INTEGER NOT NULL,
    approved INTEGER NOT NULL,
    safe INTEGER NOT NULL,
    token TEXT,
    ip VARCHAR(40),
    date_added TEXT NOT NULL
);
```

**oc_address**
```sql
CREATE TABLE oc_address (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    firstname VARCHAR(32) NOT NULL,
    lastname VARCHAR(32) NOT NULL,
    company VARCHAR(60),
    address_1 VARCHAR(128) NOT NULL,
    address_2 VARCHAR(128),
    city VARCHAR(128) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    country_id INTEGER NOT NULL,
    zone_id INTEGER NOT NULL,
    is_default INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES oc_customer(customer_id) ON DELETE CASCADE
);
```

#### Order Tables

**oc_order**
```sql
CREATE TABLE oc_order (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no INTEGER DEFAULT 0,
    invoice_prefix VARCHAR(26),
    store_id INTEGER DEFAULT 0,
    store_name VARCHAR(64),
    store_url VARCHAR(255),
    customer_id INTEGER NOT NULL,
    customer_group_id INTEGER DEFAULT 0,
    firstname VARCHAR(32) NOT NULL,
    lastname VARCHAR(32) NOT NULL,
    email VARCHAR(96) NOT NULL,
    telephone VARCHAR(32) NOT NULL,
    payment_firstname VARCHAR(32),
    payment_lastname VARCHAR(32),
    payment_address_1 VARCHAR(128),
    payment_city VARCHAR(128),
    payment_postcode VARCHAR(10),
    payment_country VARCHAR(128),
    payment_method VARCHAR(128),
    shipping_firstname VARCHAR(32),
    shipping_method VARCHAR(128),
    order_status_id INTEGER DEFAULT 0,
    currency_code VARCHAR(3),
    currency_value REAL DEFAULT 1.0,
    total REAL DEFAULT 0.0,
    date_added TEXT NOT NULL,
    date_modified TEXT NOT NULL
);
```

**oc_order_product**
```sql
CREATE TABLE oc_order_product (
    order_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(64),
    quantity INTEGER NOT NULL,
    price REAL DEFAULT 0.0,
    total REAL DEFAULT 0.0,
    tax REAL DEFAULT 0.0,
    FOREIGN KEY (order_id) REFERENCES oc_order(order_id) ON DELETE CASCADE
);
```

**oc_order_total**
```sql
CREATE TABLE oc_order_total (
    order_total_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    code VARCHAR(32) NOT NULL,
    title VARCHAR(255) NOT NULL,
    value REAL DEFAULT 0.0,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES oc_order(order_id) ON DELETE CASCADE
);
```

#### Cart Table

**oc_cart**
```sql
CREATE TABLE oc_cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER DEFAULT 0,
    session_id VARCHAR(32),
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    option_data TEXT,
    date_added TEXT NOT NULL
);
```

#### Category Tables

**oc_category**
```sql
CREATE TABLE oc_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    image VARCHAR(255),
    parent_id INTEGER DEFAULT 0,
    top INTEGER DEFAULT 0,
    column_count INTEGER DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    status INTEGER DEFAULT 1,
    date_added TEXT NOT NULL,
    date_modified TEXT NOT NULL
);
```

**oc_category_description**
```sql
CREATE TABLE oc_category_description (
    category_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    meta_title VARCHAR(255),
    meta_description VARCHAR(255),
    meta_keyword VARCHAR(255),
    PRIMARY KEY (category_id, language_id),
    FOREIGN KEY (category_id) REFERENCES oc_category(category_id) ON DELETE CASCADE
);
```

### SQLAlchemy ORM Models

**Example: Product Model**

```python
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "oc_product"
    
    product_id = Column(Integer, primary_key=True, index=True)
    model = Column(String(64), nullable=False)
    sku = Column(String(64))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    image = Column(String(255))
    manufacturer_id = Column(Integer)
    status = Column(Integer, default=1)
    viewed = Column(Integer, default=0)
    date_added = Column(Text, nullable=False)
    date_modified = Column(Text, nullable=False)
    
    # Relationships
    descriptions = relationship("ProductDescription", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    categories = relationship("ProductToCategory", back_populates="product")

class ProductDescription(Base):
    __tablename__ = "oc_product_description"
    
    product_id = Column(Integer, ForeignKey("oc_product.product_id"), primary_key=True)
    language_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    
    # Relationship
    product = relationship("Product", back_populates="descriptions")
```

---

## API Endpoint Specifications

### Authentication Endpoints

**Base Path**: `/api/v1/auth`

#### POST /auth/register
**Purpose**: Register new customer account

**Request Body**:
```json
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john@example.com",
  "telephone": "555-1234",
  "password": "securepass123"
}
```

**Response (201 Created)**:
```json
{
  "customer_id": 123,
  "email": "john@example.com",
  "firstname": "John",
  "lastname": "Doe"
}
```

#### POST /auth/login
**Purpose**: Authenticate customer and return JWT token

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "customer": {
    "customer_id": 123,
    "email": "john@example.com",
    "firstname": "John",
    "lastname": "Doe"
  }
}
```

### Product Endpoints

**Base Path**: `/api/v1/products`

#### GET /products
**Purpose**: List products with pagination and filtering

**Query Parameters**:
- `page` (int, default: 1)
- `limit` (int, default: 20, max: 100)
- `category_id` (int, optional)
- `search` (string, optional)
- `sort` (string: "name", "price", "date", default: "sort_order")
- `order` (string: "asc", "desc", default: "asc")

**Response (200 OK)**:
```json
{
  "items": [
    {
      "product_id": 42,
      "name": "Product Name",
      "model": "PROD-001",
      "price": 29.99,
      "special_price": null,
      "image": "/images/products/product-42.jpg",
      "rating": 4.5,
      "reviews_count": 12
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

#### GET /products/{product_id}
**Purpose**: Get detailed product information

**Response (200 OK)**:
```json
{
  "product_id": 42,
  "name": "Product Name",
  "model": "PROD-001",
  "description": "Full product description...",
  "price": 29.99,
  "special_price": 24.99,
  "tax": 2.50,
  "quantity": 100,
  "minimum": 1,
  "image": "/images/products/product-42.jpg",
  "images": [
    "/images/products/product-42-1.jpg",
    "/images/products/product-42-2.jpg"
  ],
  "manufacturer": "Brand Name",
  "options": [
    {
      "product_option_id": 5,
      "name": "Size",
      "type": "select",
      "required": true,
      "values": [
        {"value_id": 10, "name": "Small", "price_prefix": "+", "price": 0.00},
        {"value_id": 11, "name": "Large", "price_prefix": "+", "price": 5.00}
      ]
    }
  ],
  "related_products": [43, 44, 45]
}
```

### Cart Endpoints

**Base Path**: `/api/v1/cart`

#### GET /cart
**Purpose**: Get current user's cart

**Headers**: `Authorization: Bearer <token>`

**Response (200 OK)**:
```json
{
  "items": [
    {
      "cart_id": 1,
      "product_id": 42,
      "name": "Product Name",
      "model": "PROD-001",
      "image": "/images/products/product-42.jpg",
      "quantity": 2,
      "price": 29.99,
      "total": 59.98,
      "options": [
        {"name": "Size", "value": "Large", "price_modifier": 5.00}
      ]
    }
  ],
  "totals": [
    {"code": "sub_total", "title": "Sub-Total", "value": 64.98},
    {"code": "shipping", "title": "Flat Rate", "value": 5.00},
    {"code": "tax", "title": "VAT (20%)", "value": 13.00},
    {"code": "total", "title": "Total", "value": 82.98}
  ]
}
```

#### POST /cart/items
**Purpose**: Add item to cart

**Request Body**:
```json
{
  "product_id": 42,
  "quantity": 2,
  "options": {
    "5": "11"
  }
}
```

**Response (201 Created)**:
```json
{
  "cart_id": 1,
  "message": "Product added to cart"
}
```

#### PUT /cart/items/{cart_id}
**Purpose**: Update cart item quantity

**Request Body**:
```json
{
  "quantity": 3
}
```

**Response (200 OK)**:
```json
{
  "message": "Cart updated"
}
```

#### DELETE /cart/items/{cart_id}
**Purpose**: Remove item from cart

**Response (200 OK)**:
```json
{
  "message": "Item removed from cart"
}
```

### Checkout Endpoints

**Base Path**: `/api/v1/checkout`

#### POST /checkout/shipping-methods
**Purpose**: Get available shipping methods for cart

**Request Body**:
```json
{
  "country_id": 1,
  "zone_id": 5,
  "postcode": "12345"
}
```

**Response (200 OK)**:
```json
{
  "methods": [
    {
      "code": "flat.flat",
      "title": "Flat Rate",
      "cost": 5.00,
      "tax_class_id": 0
    },
    {
      "code": "weight.weight_1",
      "title": "Weight Based",
      "cost": 7.50,
      "tax_class_id": 0
    }
  ]
}
```

#### POST /checkout/payment-methods
**Purpose**: Get available payment methods

**Response (200 OK)**:
```json
{
  "methods": [
    {
      "code": "bank_transfer",
      "title": "Bank Transfer"
    },
    {
      "code": "cod",
      "title": "Cash On Delivery"
    }
  ]
}
```

#### POST /checkout/confirm
**Purpose**: Place order

**Request Body**:
```json
{
  "shipping_address": {
    "firstname": "John",
    "lastname": "Doe",
    "address_1": "123 Main St",
    "city": "New York",
    "postcode": "10001",
    "country_id": 1,
    "zone_id": 5
  },
  "payment_address": {
    "firstname": "John",
    "lastname": "Doe",
    "address_1": "123 Main St",
    "city": "New York",
    "postcode": "10001",
    "country_id": 1,
    "zone_id": 5
  },
  "shipping_method": "flat.flat",
  "payment_method": "bank_transfer",
  "comment": ""
}
```

**Response (201 Created)**:
```json
{
  "order_id": 567,
  "invoice_no": 1001,
  "total": 82.98,
  "message": "Order placed successfully"
}
```

### Order Endpoints

**Base Path**: `/api/v1/orders`

#### GET /orders
**Purpose**: List customer's orders

**Headers**: `Authorization: Bearer <token>`

**Response (200 OK)**:
```json
{
  "orders": [
    {
      "order_id": 567,
      "invoice_no": 1001,
      "status": "Processing",
      "total": 82.98,
      "date_added": "2025-01-19T10:30:00Z"
    }
  ]
}
```

#### GET /orders/{order_id}
**Purpose**: Get order details

**Response (200 OK)**:
```json
{
  "order_id": 567,
  "invoice_no": 1001,
  "status": "Processing",
  "customer": {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com"
  },
  "payment_address": {
    "firstname": "John",
    "lastname": "Doe",
    "address_1": "123 Main St",
    "city": "New York"
  },
  "products": [
    {
      "name": "Product Name",
      "model": "PROD-001",
      "quantity": 2,
      "price": 29.99,
      "total": 59.98
    }
  ],
  "totals": [
    {"title": "Sub-Total", "value": 59.98},
    {"title": "Shipping", "value": 5.00},
    {"title": "Tax", "value": 13.00},
    {"title": "Total", "value": 82.98}
  ],
  "date_added": "2025-01-19T10:30:00Z"
}
```

### Admin Endpoints

**Base Path**: `/api/v1/admin`

All admin endpoints require admin authentication.

#### GET /admin/orders
**Purpose**: List all orders (admin view)

**Response (200 OK)**:
```json
{
  "orders": [
    {
      "order_id": 567,
      "customer": "John Doe",
      "status": "Processing",
      "total": 82.98,
      "date_added": "2025-01-19T10:30:00Z"
    }
  ],
  "total": 50,
  "page": 1
}
```

#### PUT /admin/orders/{order_id}/status
**Purpose**: Update order status

**Request Body**:
```json
{
  "order_status_id": 5,
  "comment": "Order shipped",
  "notify": true
}
```

**Response (200 OK)**:
```json
{
  "message": "Order status updated"
}
```

---

## Pydantic Models

### Request/Response Schemas

**Product Schemas** (`app/models/schemas/product.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    model: str
    price: float = Field(ge=0)
    
class ProductCreate(ProductBase):
    description: Optional[str] = None
    quantity: int = 0
    image: Optional[str] = None

class ProductResponse(ProductBase):
    product_id: int
    image: Optional[str]
    special_price: Optional[float]
    rating: Optional[float]
    reviews_count: int
    
    class Config:
        from_attributes = True

class ProductDetail(ProductResponse):
    description: str
    quantity: int
    minimum: int
    images: List[str]
    manufacturer: Optional[str]
    options: List[dict]
    related_products: List[int]

class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    limit: int
    pages: int
```

**Cart Schemas** (`app/models/schemas/cart.py`)

```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    options: Optional[Dict[str, str]] = {}

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    cart_id: int
    product_id: int
    name: str
    model: str
    image: Optional[str]
    quantity: int
    price: float
    total: float
    options: List[dict]

class CartTotalLine(BaseModel):
    code: str
    title: str
    value: float

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    totals: List[CartTotalLine]
```

**Order Schemas** (`app/models/schemas/order.py`)

```python
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class AddressSchema(BaseModel):
    firstname: str
    lastname: str
    address_1: str
    address_2: Optional[str] = None
    city: str
    postcode: str
    country_id: int
    zone_id: int

class OrderCreate(BaseModel):
    shipping_address: AddressSchema
    payment_address: AddressSchema
    shipping_method: str
    payment_method: str
    comment: Optional[str] = None

class OrderProductResponse(BaseModel):
    name: str
    model: str
    quantity: int
    price: float
    total: float

class OrderResponse(BaseModel):
    order_id: int
    invoice_no: int
    status: str
    total: float
    date_added: datetime

class OrderDetailResponse(OrderResponse):
    customer: dict
    payment_address: dict
    shipping_address: dict
    products: List[OrderProductResponse]
    totals: List[dict]
```

**Authentication Schemas** (`app/models/schemas/auth.py`)

```python
from pydantic import BaseModel, EmailStr

class CustomerRegister(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    telephone: str
    password: str

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    customer: dict

class CustomerResponse(BaseModel):
    customer_id: int
    email: str
    firstname: str
    lastname: str
    telephone: str
    
    class Config:
        from_attributes = True
```

---

## Business Logic Services

### Service Layer Architecture

Services contain all business logic and orchestrate repository calls.

**Product Service** (`app/services/product_service.py`)

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.schemas.product import ProductResponse, ProductDetail

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def get_products(
        self,
        page: int = 1,
        limit: int = 20,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        sort: str = "sort_order",
        order: str = "asc"
    ) -> dict:
        """Get paginated product list with filtering"""
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
        pages = (total + limit - 1) // limit
        
        return {
            "items": products,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }
    
    def get_product_detail(self, product_id: int) -> Optional[ProductDetail]:
        """Get detailed product information"""
        product = self.repository.find_by_id(product_id)
        if not product:
            return None
        
        # Load related data
        images = self.repository.get_images(product_id)
        options = self.repository.get_options(product_id)
        related = self.repository.get_related(product_id)
        
        return ProductDetail(
            **product.__dict__,
            images=images,
            options=options,
            related_products=related
        )
```

**Cart Service** (`app/services/cart_service.py`)

```python
from sqlalchemy.orm import Session
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.services.tax_service import TaxService
from app.services.shipping_service import ShippingService

class CartService:
    def __init__(self, db: Session):
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.tax_service = TaxService(db)
        self.shipping_service = ShippingService(db)
    
    def add_item(self, customer_id: int, product_id: int, quantity: int, options: dict):
        """Add product to cart"""
        # Validate product exists and is available
        product = self.product_repo.find_by_id(product_id)
        if not product or product.status != 1:
            raise ValueError("Product not available")
        
        # Check stock
        if product.quantity < quantity:
            raise ValueError("Insufficient stock")
        
        # Check if item already in cart
        existing = self.cart_repo.find_by_product(customer_id, product_id, options)
        if existing:
            self.cart_repo.update_quantity(existing.cart_id, existing.quantity + quantity)
        else:
            self.cart_repo.create(customer_id, product_id, quantity, options)
    
    def get_cart(self, customer_id: int) -> dict:
        """Get cart with calculated totals"""
        items = self.cart_repo.get_items(customer_id)
        
        # Calculate totals
        subtotal = sum(item.price * item.quantity for item in items)
        
        # Get shipping cost (simplified)
        shipping = self.shipping_service.calculate(customer_id, items)
        
        # Calculate tax
        tax = self.tax_service.calculate(customer_id, subtotal, shipping)
        
        total = subtotal + shipping + tax
        
        totals = [
            {"code": "sub_total", "title": "Sub-Total", "value": subtotal},
            {"code": "shipping", "title": "Shipping", "value": shipping},
            {"code": "tax", "title": "Tax", "value": tax},
            {"code": "total", "title": "Total", "value": total}
        ]
        
        return {
            "items": items,
            "totals": totals
        }
```

**Order Service** (`app/services/order_service.py`)

```python
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.services.cart_service import CartService
from datetime import datetime

class OrderService:
    def __init__(self, db: Session):
        self.repository = OrderRepository(db)
        self.cart_service = CartService(db)
    
    def create_order(self, customer_id: int, order_data: dict) -> int:
        """Create order from cart"""
        # Get cart
        cart = self.cart_service.get_cart(customer_id)
        
        if not cart["items"]:
            raise ValueError("Cart is empty")
        
        # Prepare order data
        order = {
            "customer_id": customer_id,
            "firstname": order_data["payment_address"]["firstname"],
            "lastname": order_data["payment_address"]["lastname"],
            "email": order_data["customer_email"],
            "payment_address_1": order_data["payment_address"]["address_1"],
            "payment_city": order_data["payment_address"]["city"],
            "payment_method": order_data["payment_method"],
            "shipping_method": order_data["shipping_method"],
            "total": cart["totals"][-1]["value"],
            "order_status_id": 1,  # Pending
            "date_added": datetime.utcnow().isoformat(),
            "date_modified": datetime.utcnow().isoformat()
        }
        
        # Create order in transaction
        order_id = self.repository.create_order(order, cart["items"], cart["totals"])
        
        # Clear cart
        self.cart_service.clear_cart(customer_id)
        
        return order_id
```

---

## Authentication & Authorization

### JWT Token Implementation

**Security Module** (`app/core/security.py`)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

**Authentication Dependencies** (`app/api/deps.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.customer_repository import CustomerRepository

security = HTTPBearer()

def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated customer"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    customer_id = payload.get("sub")
    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    customer_repo = CustomerRepository(db)
    customer = customer_repo.find_by_id(int(customer_id))
    
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer not found"
        )
    
    return customer

def get_current_admin(
    customer = Depends(get_current_customer)
):
    """Verify customer has admin privileges"""
    if customer.customer_group_id != 1:  # Admin group
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return customer
```

---

## Error Handling Strategy

### Custom Exception Classes

**Exceptions Module** (`app/utils/exceptions.py`)

```python
from fastapi import HTTPException, status

class ProductNotFoundException(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )

class InsufficientStockException(HTTPException):
    def __init__(self, product_id: int, available: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for product {product_id}. Available: {available}"
        )

class EmptyCartException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
```

### Global Exception Handler

**Main Application** (`app/main.py`)

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="OpenCart Modern API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors()
            }
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
```

---

## Configuration Management

**Configuration Module** (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "OpenCart Modern API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/opencart.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**Environment Variables** (`.env.example`)

```
# Application
APP_NAME=OpenCart Modern API
DEBUG=False

# Database
DATABASE_URL=sqlite:///./data/opencart.db

# Security (CHANGE IN PRODUCTION)
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

## Summary

This Low-Level Design document provides comprehensive specifications for implementing the FastAPI backend, including:

- **Project Structure**: Organized in layers (API, Service, Repository, Model)
- **Database Schema**: SQLite-compatible schema preserving OpenCart structure
- **API Endpoints**: RESTful endpoints for all major modules
- **Pydantic Models**: Request/response validation schemas
- **Business Logic**: Service layer implementing cart calculations, order processing
- **Authentication**: JWT-based token authentication
- **Error Handling**: Structured exception handling
- **Configuration**: Environment-based configuration management

All implementations must maintain 100% behavioral parity with the original PHP OpenCart system while leveraging modern Python and FastAPI patterns.

---

**Next Document**: [05b-lld-frontend-modules.md](./05b-lld-frontend-modules.md) - Frontend detailed design specifications
