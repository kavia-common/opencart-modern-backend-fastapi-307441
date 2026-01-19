# Target Architecture - High-Level Design (HLD)

**Document**: Phase 3 - Target System Architecture  
**Migration**: OpenCart PHP → FastAPI + React  
**Version**: 1.0  
**Date**: 2025-01-19

---

## Executive Summary

This document defines the high-level architecture of the target system resulting from the OpenCart migration. The modernized system adopts an API-first, microservices-ready architecture with clear separation between backend business logic (FastAPI) and frontend presentation (React). This architecture ensures scalability, maintainability, and adherence to modern web development best practices.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [System Components](#system-components)
3. [Backend Architecture (FastAPI)](#backend-architecture-fastapi)
4. [Frontend Architecture (React)](#frontend-architecture-react)
5. [API Communication Model](#api-communication-model)
6. [Authentication & Session Management](#authentication--session-management)
7. [Database Architecture](#database-architecture)
8. [Data Flow Diagrams](#data-flow-diagrams)
9. [State Management Strategy](#state-management-strategy)
10. [Deployment Architecture](#deployment-architecture)
11. [Non-Functional Considerations](#non-functional-considerations)

---

## Architecture Overview

### Architectural Paradigm

The target system follows a **3-tier architecture** with complete decoupling between presentation, business logic, and data layers.

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT TIER                          │
│         React SPA (User Interface Layer)                │
│    • Component-based UI                                 │
│    • Client-side routing                                │
│    • State management                                   │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/HTTPS (JSON)
                  │ RESTful API Calls
┌─────────────────▼───────────────────────────────────────┐
│                 APPLICATION TIER                        │
│         FastAPI Backend (Business Logic Layer)          │
│    • RESTful API endpoints                              │
│    • Business logic services                            │
│    • Data validation & transformation                   │
│    • Authentication & authorization                     │
└─────────────────┬───────────────────────────────────────┘
                  │ ORM / SQL
                  │ Database Queries
┌─────────────────▼───────────────────────────────────────┐
│                    DATA TIER                            │
│          SQLite Database (Persistence Layer)            │
│    • Relational data storage                            │
│    • Transaction management                             │
│    • Data integrity constraints                         │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns**: Frontend handles presentation; backend handles business logic; database manages persistence
2. **API-First Design**: All functionality exposed through well-defined RESTful APIs
3. **Stateless Backend**: Backend services are stateless; session state managed via tokens
4. **Behavior Preservation**: Architecture designed to replicate OpenCart functionality exactly
5. **Technology Modernization**: Leverage modern frameworks while maintaining functional equivalence

---

## System Components

### Component Inventory

| Component | Technology | Responsibility | Location |
|-----------|-----------|----------------|----------|
| **Frontend Application** | React 18+ | User interface, client-side routing, state management | `opencart-modern-frontend-react-307441/` |
| **Backend API Server** | FastAPI (Python 3.9+) | Business logic, API endpoints, data validation | `opencart-modern-backend-fastapi-307441/` |
| **Database** | SQLite 3 | Data persistence, transactional storage | `opencart-modern-backend-fastapi-307441/data/` |
| **API Documentation** | OpenAPI/Swagger | Auto-generated API docs | `/docs` endpoint (FastAPI) |
| **Static Assets** | Nginx/CDN (optional) | Image hosting, static file serving | `frontend/public/` |

### Component Interaction

The components interact through well-defined interfaces:

- **Frontend ↔ Backend**: RESTful HTTP/JSON over HTTPS
- **Backend ↔ Database**: SQLAlchemy ORM with SQLite driver
- **Admin ↔ System**: Same API endpoints with role-based access control

---

## Backend Architecture (FastAPI)

### Backend Structure

The FastAPI backend follows a layered architecture pattern:

```
opencart-modern-backend-fastapi-307441/
├── app/
│   ├── main.py                    # Application entry point
│   ├── core/
│   │   ├── config.py              # Configuration management
│   │   ├── security.py            # Authentication/authorization
│   │   └── dependencies.py        # Shared dependencies
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── products.py    # Product endpoints
│   │   │   │   ├── categories.py  # Category endpoints
│   │   │   │   ├── cart.py        # Shopping cart endpoints
│   │   │   │   ├── checkout.py    # Checkout endpoints
│   │   │   │   ├── customers.py   # Customer endpoints
│   │   │   │   ├── orders.py      # Order endpoints
│   │   │   │   └── admin.py       # Admin endpoints
│   │   │   └── router.py          # API router aggregation
│   ├── models/
│   │   ├── database.py            # SQLAlchemy models
│   │   ├── schemas.py             # Pydantic request/response schemas
│   │   └── entities.py            # Domain entities
│   ├── services/
│   │   ├── product_service.py     # Product business logic
│   │   ├── cart_service.py        # Cart business logic
│   │   ├── order_service.py       # Order processing logic
│   │   ├── customer_service.py    # Customer management logic
│   │   └── payment_service.py     # Payment processing logic
│   ├── repositories/
│   │   ├── product_repository.py  # Product data access
│   │   ├── cart_repository.py     # Cart data access
│   │   ├── order_repository.py    # Order data access
│   │   └── customer_repository.py # Customer data access
│   └── utils/
│       ├── validators.py          # Custom validation functions
│       ├── formatters.py          # Data formatting utilities
│       └── helpers.py             # General helper functions
├── alembic/                       # Database migrations
├── tests/                         # Test suite
├── requirements.txt               # Python dependencies
└── .env                           # Environment configuration
```

### Backend Layers

**1. API Layer (`app/api/`)**
- Exposes RESTful endpoints
- Handles HTTP request/response
- Input validation via Pydantic models
- Route definitions and versioning

**2. Service Layer (`app/services/`)**
- Contains business logic
- Orchestrates data operations
- Implements domain rules
- Independent of HTTP concerns

**3. Repository Layer (`app/repositories/`)**
- Data access abstraction
- Database query execution
- ORM interaction
- Transaction management

**4. Model Layer (`app/models/`)**
- Database models (SQLAlchemy)
- Pydantic schemas for validation
- Domain entity definitions

**5. Core Layer (`app/core/`)**
- Configuration management
- Authentication/authorization
- Shared utilities and dependencies

---

## Frontend Architecture (React)

### Frontend Structure

The React frontend follows a component-based architecture with feature-oriented organization:

```
opencart-modern-frontend-react-307441/
├── public/
│   ├── index.html
│   └── assets/                    # Static images, icons
├── src/
│   ├── index.js                   # Application entry point
│   ├── App.js                     # Root component
│   ├── pages/
│   │   ├── Home.js                # Homepage
│   │   ├── ProductList.js         # Product listing page
│   │   ├── ProductDetail.js       # Product detail page
│   │   ├── Cart.js                # Shopping cart page
│   │   ├── Checkout.js            # Checkout page
│   │   ├── Account.js             # Customer account page
│   │   ├── OrderHistory.js        # Order history page
│   │   └── Admin/                 # Admin pages
│   │       ├── Dashboard.js
│   │       ├── ProductManagement.js
│   │       └── OrderManagement.js
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.js          # Site header
│   │   │   ├── Footer.js          # Site footer
│   │   │   ├── Navigation.js      # Navigation menu
│   │   │   └── Breadcrumb.js      # Breadcrumb trail
│   │   ├── product/
│   │   │   ├── ProductCard.js     # Product display card
│   │   │   ├── ProductFilter.js   # Filter component
│   │   │   └── ProductSearch.js   # Search component
│   │   ├── cart/
│   │   │   ├── CartItem.js        # Cart item component
│   │   │   └── CartSummary.js     # Cart total summary
│   │   └── checkout/
│   │       ├── ShippingForm.js    # Shipping address form
│   │       ├── PaymentForm.js     # Payment details form
│   │       └── OrderSummary.js    # Order review component
│   ├── services/
│   │   ├── api.js                 # Axios instance configuration
│   │   ├── productService.js      # Product API calls
│   │   ├── cartService.js         # Cart API calls
│   │   ├── orderService.js        # Order API calls
│   │   └── authService.js         # Authentication API calls
│   ├── context/
│   │   ├── AuthContext.js         # Authentication state
│   │   ├── CartContext.js         # Shopping cart state
│   │   └── ThemeContext.js        # Theme/UI state
│   ├── hooks/
│   │   ├── useAuth.js             # Authentication hook
│   │   ├── useCart.js             # Cart management hook
│   │   └── useApi.js              # API call hook
│   ├── utils/
│   │   ├── formatters.js          # Data formatting utilities
│   │   ├── validators.js          # Form validation
│   │   └── constants.js           # App constants
│   ├── routes/
│   │   └── AppRoutes.js           # Route definitions
│   └── styles/
│       ├── global.css             # Global styles
│       └── theme.css              # Theme variables
├── package.json                   # NPM dependencies
└── .env                           # Environment variables
```

### Frontend Patterns

**1. Component Architecture**
- Functional components with hooks
- Separation of presentational and container components
- Reusable UI components in `components/common/`
- Feature-specific components in dedicated folders

**2. State Management**
- React Context API for global state (auth, cart)
- Local component state for UI-specific data
- Custom hooks for shared logic

**3. Routing**
- React Router v6 for client-side routing
- Protected routes for authenticated pages
- Lazy loading for performance optimization

**4. API Integration**
- Axios for HTTP requests
- Centralized API service layer
- Error handling and retry logic
- Request/response interceptors

---

## API Communication Model

### RESTful API Design

The system uses REST principles with JSON payloads for all client-server communication.

**Base URL**: `http://localhost:8000/api/v1`

### Endpoint Categories

| Category | Base Path | Description |
|----------|-----------|-------------|
| **Products** | `/products` | Product catalog operations |
| **Categories** | `/categories` | Category browsing and filtering |
| **Cart** | `/cart` | Shopping cart management |
| **Checkout** | `/checkout` | Order placement and payment |
| **Customers** | `/customers` | Customer account management |
| **Orders** | `/orders` | Order history and tracking |
| **Admin** | `/admin` | Administrative operations |
| **Auth** | `/auth` | Authentication and token management |

### Standard HTTP Methods

- **GET**: Retrieve resources (idempotent)
- **POST**: Create new resources
- **PUT**: Update existing resources (full replacement)
- **PATCH**: Partial update of resources
- **DELETE**: Remove resources

### Request/Response Format

**Request Example**:
```json
POST /api/v1/cart/items
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "product_id": 123,
  "quantity": 2,
  "options": {
    "size": "M",
    "color": "blue"
  }
}
```

**Response Example**:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "cart_id": "abc123",
    "items": [
      {
        "product_id": 123,
        "name": "Product Name",
        "quantity": 2,
        "price": 29.99,
        "subtotal": 59.98
      }
    ],
    "total": 59.98
  },
  "message": "Item added to cart successfully"
}
```

### Error Handling

All API errors follow a consistent format:

```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "error": {
    "code": "INVALID_PRODUCT_ID",
    "message": "The specified product ID does not exist",
    "details": {
      "product_id": 999
    }
  }
}
```

**Standard HTTP Status Codes**:
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

---

## Authentication & Session Management

### Authentication Strategy

The system uses **JWT (JSON Web Token)** based authentication, replacing PHP session-based authentication.

### Authentication Flow

```
┌─────────┐                  ┌─────────┐                 ┌──────────┐
│  Client │                  │  FastAPI│                 │ Database │
└────┬────┘                  └────┬────┘                 └────┬─────┘
     │                            │                           │
     │  POST /auth/login          │                           │
     │  {email, password}         │                           │
     ├───────────────────────────>│                           │
     │                            │  Verify credentials       │
     │                            ├──────────────────────────>│
     │                            │<──────────────────────────┤
     │                            │  User data                │
     │                            │                           │
     │                            │  Generate JWT token       │
     │<───────────────────────────┤                           │
     │  {token, user_info}        │                           │
     │                            │                           │
     │  GET /products             │                           │
     │  Authorization: Bearer JWT │                           │
     ├───────────────────────────>│                           │
     │                            │  Validate JWT             │
     │                            │  Extract user context     │
     │                            ├──────────────────────────>│
     │                            │<──────────────────────────┤
     │<───────────────────────────┤  Product data             │
     │  {products}                │                           │
```

### JWT Token Structure

**Token Payload**:
```json
{
  "sub": "customer_id_123",
  "email": "customer@example.com",
  "role": "customer",
  "exp": 1234567890,
  "iat": 1234567800
}
```

### Session Equivalence

| PHP Session Behavior | JWT Equivalent |
|---------------------|----------------|
| `$_SESSION['customer_id']` | JWT `sub` claim |
| `$_SESSION['cart']` | Server-side cart linked to customer ID |
| Session timeout | JWT `exp` (expiration time) |
| Session regeneration | Token refresh endpoint |

### Security Measures

1. **Token Storage**: Stored in `httpOnly` cookies or `localStorage` (with XSS protection)
2. **Token Expiration**: Short-lived access tokens (15 minutes) + long-lived refresh tokens (7 days)
3. **HTTPS Only**: All authentication endpoints require HTTPS in production
4. **Password Hashing**: bcrypt with salt for password storage
5. **CSRF Protection**: CSRF tokens for state-changing operations

---

## Database Architecture

### Database Migration: MySQL → SQLite

The target system uses **SQLite** instead of MySQL while maintaining schema compatibility.

### Schema Design Principles

1. **Schema Preservation**: Maintain OpenCart table structure and relationships
2. **Naming Conventions**: Keep original OpenCart table and column names
3. **Data Type Mapping**: Convert MySQL types to SQLite equivalents
4. **Constraints**: Preserve foreign keys, indexes, and unique constraints

### Core Database Tables

**Product Tables**:
- `oc_product`: Product master data
- `oc_product_description`: Localized product info
- `oc_product_to_category`: Product-category relationships
- `oc_product_image`: Product images
- `oc_product_option`: Product options/variants

**Customer Tables**:
- `oc_customer`: Customer accounts
- `oc_address`: Customer addresses
- `oc_customer_group`: Customer groupings

**Order Tables**:
- `oc_order`: Order master records
- `oc_order_product`: Order line items
- `oc_order_total`: Order totals and taxes
- `oc_order_history`: Order status history

**Cart Tables**:
- `oc_cart`: Shopping cart items

**Category Tables**:
- `oc_category`: Category hierarchy
- `oc_category_description`: Localized category info

### Data Type Mapping

| MySQL Type | SQLite Equivalent | Notes |
|-----------|------------------|-------|
| `INT`, `BIGINT` | `INTEGER` | Auto-increment preserved |
| `VARCHAR(n)`, `TEXT` | `TEXT` | No length limit in SQLite |
| `DECIMAL(m,n)` | `REAL` | Floating-point for prices |
| `DATETIME`, `TIMESTAMP` | `TEXT` (ISO8601) | Stored as strings |
| `TINYINT(1)` | `INTEGER` | Boolean values (0/1) |

### ORM: SQLAlchemy

**ORM Features**:
- Declarative model definitions
- Automatic query generation
- Transaction management
- Connection pooling
- Migration support via Alembic

**Example Model**:
```python
from sqlalchemy import Column, Integer, String, Numeric, Text
from app.database import Base

class Product(Base):
    __tablename__ = "oc_product"
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(64), nullable=False)
    sku = Column(String(64))
    quantity = Column(Integer, default=0)
    price = Column(Numeric(15, 4), default=0.0000)
    image = Column(String(255))
    status = Column(Integer, default=1)
    date_added = Column(Text)
    date_modified = Column(Text)
```

---

## Data Flow Diagrams

### Product Browsing Flow

```
User → React Page (ProductList.js)
       ↓
    API Call (GET /products?category=5&page=1)
       ↓
    FastAPI Endpoint (products.py)
       ↓
    Product Service (product_service.py)
       ↓
    Product Repository (product_repository.py)
       ↓
    SQLite Database (oc_product, oc_product_description)
       ↓
    Data Transformation (Pydantic models)
       ↓
    JSON Response → React Component → UI Render
```

### Cart Management Flow

```
User → Add to Cart Button (ProductCard.js)
       ↓
    API Call (POST /cart/items {product_id, quantity})
       ↓
    FastAPI Endpoint (cart.py)
       ↓
    JWT Validation & Customer ID Extraction
       ↓
    Cart Service (cart_service.py)
       ↓
    Cart Repository (cart_repository.py)
       ↓
    SQLite Database (oc_cart)
       ↓
    Updated Cart Data → JSON Response
       ↓
    CartContext Update → UI Refresh
```

### Checkout Flow

```
User → Checkout Page (Checkout.js)
       ↓
    Step 1: Shipping Address
       API Call (POST /checkout/shipping {address})
       ↓
    Step 2: Shipping Method
       API Call (POST /checkout/shipping-method {method_id})
       ↓
    Step 3: Payment Method
       API Call (POST /checkout/payment-method {method_id})
       ↓
    Step 4: Order Confirmation
       API Call (POST /checkout/confirm)
       ↓
    Order Service (order_service.py)
       Transaction: Create order, update inventory, clear cart
       ↓
    SQLite Database (oc_order, oc_order_product, oc_cart)
       ↓
    Order Confirmation → Redirect to Success Page
```

---

## State Management Strategy

### Frontend State Management

**Global State (React Context)**:
- **AuthContext**: User authentication status, profile data
- **CartContext**: Shopping cart items, totals, item count
- **ThemeContext**: UI theme preferences, language settings

**Local Component State**:
- Form input values
- UI toggle states (modals, dropdowns)
- Temporary filtering/sorting preferences

### State Synchronization

1. **Initial Load**: Fetch cart and user data from API on app mount
2. **Real-time Updates**: Update context immediately on user actions
3. **Backend Sync**: API calls ensure server state consistency
4. **Optimistic Updates**: Update UI before API response for better UX
5. **Error Handling**: Revert state if API call fails

---

## Deployment Architecture

### Development Environment

```
Developer Machine
├── React Dev Server (localhost:3000)
│   └── Proxies API calls to backend
└── FastAPI Dev Server (localhost:8000)
    └── SQLite database file
```

### Production Environment

```
                    ┌──────────────┐
                    │   Load       │
                    │   Balancer   │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
        ┌─────▼──────┐          ┌──────▼─────┐
        │   Nginx    │          │   Nginx    │
        │  (Static)  │          │  (Static)  │
        └─────┬──────┘          └──────┬─────┘
              │                         │
              │  Reverse Proxy          │
              │                         │
        ┌─────▼──────┐          ┌──────▼─────┐
        │  FastAPI   │          │  FastAPI   │
        │  Instance  │          │  Instance  │
        └─────┬──────┘          └──────┬─────┘
              │                         │
              └────────────┬────────────┘
                           │
                    ┌──────▼───────┐
                    │   SQLite     │
                    │   Database   │
                    └──────────────┘
```

**Deployment Stack**:
- **Frontend**: Static files served by Nginx or CDN
- **Backend**: FastAPI via Uvicorn ASGI server
- **Database**: SQLite file on persistent volume
- **Reverse Proxy**: Nginx for SSL termination and load balancing
- **Containerization**: Docker containers for reproducible deployments

---

## Non-Functional Considerations

### Performance

1. **API Response Time**: Target < 200ms for catalog queries
2. **Page Load Time**: < 2 seconds for initial page load
3. **Database Indexing**: Proper indexes on frequently queried columns
4. **Caching Strategy**: Redis cache for frequently accessed data (future enhancement)
5. **Lazy Loading**: React components loaded on-demand

### Scalability

1. **Horizontal Scaling**: Stateless backend allows multiple instances
2. **Database Scaling**: SQLite suitable for small-to-medium traffic; future migration to PostgreSQL
3. **CDN Integration**: Static assets served from CDN
4. **API Rate Limiting**: Prevent abuse with request throttling

### Security

1. **Input Validation**: Pydantic models validate all incoming data
2. **SQL Injection Prevention**: ORM parameterized queries
3. **XSS Protection**: React auto-escapes rendered content
4. **CORS Configuration**: Strict CORS policy for API endpoints
5. **Authentication**: JWT with secure token storage

### Maintainability

1. **Code Organization**: Clear separation of concerns across layers
2. **Documentation**: OpenAPI auto-generated docs for all endpoints
3. **Testing**: Unit tests for services, integration tests for APIs
4. **Logging**: Structured logging for debugging and monitoring
5. **Version Control**: Git-based workflow with feature branches

### Reliability

1. **Error Handling**: Graceful degradation and user-friendly error messages
2. **Data Validation**: Multi-layer validation (client + server)
3. **Transaction Management**: ACID compliance for order processing
4. **Backup Strategy**: Regular database backups
5. **Health Checks**: API health endpoints for monitoring

---

## Summary

This high-level architecture document outlines the target system's structure, emphasizing:

- **Modern Technology Stack**: FastAPI + React replacing legacy PHP
- **API-First Design**: RESTful APIs as the backbone of all interactions
- **Separation of Concerns**: Clear boundaries between frontend, backend, and database
- **Behavior Preservation**: Architecture designed to replicate OpenCart functionality
- **Scalability & Maintainability**: Built for future growth and ease of maintenance

The detailed low-level design documents (05a and 05b) will expand on the implementation specifics for backend and frontend modules respectively.

---

**Next Document**: [05a-lld-backend-modules.md](./05a-lld-backend-modules.md) - Backend detailed design specifications
