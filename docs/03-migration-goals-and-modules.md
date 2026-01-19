# Migration Goals and Module Scope

**Document Version**: 1.0  
**Last Updated**: 2025-01-19  
**Purpose**: Define migration principles, scope boundaries, and module mapping strategy

---

## Table of Contents

1. [Migration Principles](#migration-principles)
2. [Scope Definition](#scope-definition)
3. [Backend vs Frontend Responsibilities](#backend-vs-frontend-responsibilities)
4. [Module Mapping](#module-mapping)
5. [Non-Functional Requirements](#non-functional-requirements)

---

## Migration Principles

### Core Principles

#### 1. **100% Behavior Preservation**

The migrated system must reproduce identical business logic and workflows from the legacy PHP implementation.

**What This Means:**
- All product browsing features function identically
- Cart calculations produce same results
- Checkout flow maintains same validation rules
- Order processing follows same business rules
- Admin panel operations have same capabilities

**Exceptions:**
- Performance optimizations that don't change outcomes
- Security improvements
- Modern UX enhancements that don't alter functionality

#### 2. **Data Integrity and Consistency**

All data transformations must be lossless and verifiable.

**Requirements:**
- Database migration from MySQL to SQLite must preserve all data
- Product prices, taxes, and calculations remain accurate
- Customer data, order history, and relationships intact
- No data truncation or precision loss

#### 3. **API-First Architecture**

The new system decouples frontend and backend through well-defined REST APIs.

**Benefits:**
- Frontend (React) and backend (FastAPI) can be deployed independently
- Multiple clients can consume the same APIs (web, mobile, third-party)
- Clear contract between layers via OpenAPI specification
- Easier testing and mocking

#### 4. **Maintainability and Scalability**

Modern codebase must be easier to maintain and scale than legacy PHP.

**Improvements:**
- Type safety (Python type hints, TypeScript potential)
- Automated testing (unit, integration, E2E)
- Clear separation of concerns
- Stateless backend for horizontal scaling
- Modern tooling and frameworks

#### 5. **Security by Design**

Security must be enhanced while preserving functionality.

**Enhancements:**
- JWT-based authentication (replacing PHP sessions)
- CORS configuration for API access
- Input validation with Pydantic schemas
- SQL injection prevention via ORM/parameterized queries
- Rate limiting and throttling on API endpoints

#### 6. **Auditability and Traceability**

Every migration decision must be documented and traceable.

**Documentation:**
- Source-to-target mapping for all modules
- Justification for architectural changes
- Known deviations with explanations
- Test coverage demonstrating parity

---

## Scope Definition

### In-Scope Features

#### Customer-Facing (Storefront)

**Product Catalog:**
- ✅ Product browsing with pagination
- ✅ Product detail pages with images and options
- ✅ Category navigation (hierarchical)
- ✅ Product search and filtering
- ✅ Product reviews and ratings
- ✅ Manufacturer/brand pages
- ✅ Special offers and discounts

**Shopping Cart:**
- ✅ Add/remove/update cart items
- ✅ Cart quantity management
- ✅ Product options selection (size, color, etc.)
- ✅ Cart persistence (session-based)
- ✅ Cart totals calculation (sub-total, tax, shipping, total)

**Customer Account:**
- ✅ Registration and login
- ✅ Profile management
- ✅ Address book (billing/shipping addresses)
- ✅ Order history and tracking
- ✅ Wishlist management
- ✅ Password reset flow

**Checkout:**
- ✅ Multi-step checkout process
- ✅ Guest checkout option
- ✅ Address selection/entry
- ✅ Shipping method selection
- ✅ Payment method selection
- ✅ Order confirmation
- ✅ Email notifications

**Static Content:**
- ✅ Information pages (About, Terms, Privacy)
- ✅ Contact form
- ✅ Sitemap

#### Admin Panel

**Catalog Management:**
- ✅ Product CRUD operations
- ✅ Category management
- ✅ Manufacturer management
- ✅ Product options and attributes
- ✅ Product reviews moderation
- ✅ Image uploads

**Order Management:**
- ✅ Order listing with filters
- ✅ Order detail view
- ✅ Order status updates
- ✅ Order history tracking
- ✅ Invoice generation

**Customer Management:**
- ✅ Customer listing
- ✅ Customer detail view
- ✅ Customer group management
- ✅ Address management

**Settings:**
- ✅ Store settings (name, email, etc.)
- ✅ Localization (currency, language, tax)
- ✅ Payment method configuration
- ✅ Shipping method configuration

**Reports:**
- ✅ Sales reports
- ✅ Product views/purchases
- ✅ Customer activity

### Out-of-Scope Features

#### Phase 1 Exclusions

These features exist in OpenCart but are excluded from initial migration:

**Extensions/Marketplace:**
- ❌ Extension installation system
- ❌ Theme marketplace integration
- ❌ Third-party module management
- ❌ Custom event triggers

**Advanced Features:**
- ❌ Multi-store management
- ❌ Affiliate program
- ❌ Reward points system
- ❌ Downloadable products
- ❌ Subscription/recurring payments
- ❌ Gift vouchers
- ❌ Product comparisons

**Payment/Shipping Integrations:**
- ❌ Third-party payment gateways (PayPal, Stripe, etc.)
- ❌ Real-time shipping calculators (FedEx, UPS, etc.)
- ❌ Only basic payment methods: Bank Transfer, COD, Cheque, Free Checkout
- ❌ Only basic shipping methods: Flat Rate, Weight-Based, Pickup, Free Shipping

**Admin Advanced:**
- ❌ User roles and permissions (admin only)
- ❌ API key management
- ❌ GDPR compliance tools
- ❌ Email template editor
- ❌ Marketing tools (coupons, promotions) - simplified
- ❌ SEO URL management

**Justification:**
These features add complexity without demonstrating core migration principles. They can be added in Phase 2 after core functionality is validated.

### Modified Features

#### Database: MySQL → SQLite

**Change**: Backend uses SQLite instead of MySQL/MariaDB

**Rationale:**
- Simplified deployment (no separate database server)
- Adequate for demonstration and development
- Can be replaced with PostgreSQL/MySQL in production

**Implications:**
- Schema must be adapted for SQLite syntax
- Transaction handling remains similar
- Full-text search may differ
- Foreign key constraints enabled explicitly

#### Authentication: PHP Sessions → JWT

**Change**: Session-based auth replaced with token-based auth

**Rationale:**
- Stateless backend enables horizontal scaling
- API-first architecture requires token-based auth
- React SPA needs client-side token storage

**Implications:**
- Cart data stored with user account (database) instead of session
- Token expiration and refresh flow required
- CORS configuration for cross-origin requests

#### Frontend: Server-Side Rendering → Client-Side SPA

**Change**: Twig templates replaced with React components

**Rationale:**
- Modern UX with faster interactions
- Decoupled frontend allows independent scaling
- Reusable components improve maintainability

**Implications:**
- Initial page load may be slower (mitigated with SSR in future)
- SEO considerations (React Helmet for meta tags)
- Browser back/forward handling with React Router

---

## Backend vs Frontend Responsibilities

### Backend (FastAPI) Responsibilities

**Data Management:**
- Database CRUD operations
- Business logic execution
- Data validation and sanitization
- Transaction management

**API Endpoints:**
- RESTful API design
- Request/response serialization (JSON)
- Error handling and status codes
- Pagination and filtering

**Authentication & Authorization:**
- User authentication (login/logout)
- JWT token generation and validation
- Password hashing and verification
- Permission checks

**Business Logic:**
- Cart total calculations (tax, shipping, discounts)
- Order processing workflow
- Inventory management
- Price calculations with customer groups

**Integration:**
- Email notifications (SMTP)
- File uploads (product images)
- Payment method interfaces (basic implementations)
- Shipping method calculators (basic implementations)

### Frontend (React) Responsibilities

**User Interface:**
- Component rendering
- Layout and styling
- Responsive design
- Accessibility

**User Interaction:**
- Form handling and client-side validation
- Button clicks and navigation
- Modal dialogs and notifications
- Loading states and error displays

**State Management:**
- Local component state
- Global state (cart, user session)
- Form data and validation errors
- API response caching (optional)

**API Consumption:**
- HTTP requests to backend API
- Token management (storage, inclusion in headers)
- Error handling and retry logic
- Response data transformation

**Routing:**
- Client-side navigation
- URL parameter handling
- Protected routes (authentication required)
- 404 and error pages

---

## Module Mapping

### PHP → FastAPI Backend Mapping

#### Catalog Module

| PHP Component | FastAPI Equivalent | Notes |
|---------------|-------------------|-------|
| `catalog/model/catalog/product.php` | `app/models/product.py` | SQLAlchemy models |
| `catalog/model/catalog/product.php` (queries) | `app/services/product_service.py` | Business logic layer |
| `catalog/controller/product/product.php` | `app/routers/products.py` | API endpoints |
| Product images (file system) | `app/static/images/products/` | Static file serving |

**Key Endpoints:**
```
GET    /api/products              → List products (paginated, filtered)
GET    /api/products/{id}         → Get product details
GET    /api/products/{id}/images  → Get product images
GET    /api/products/{id}/reviews → Get product reviews
POST   /api/products/{id}/reviews → Add review (authenticated)
```

#### Cart Module

| PHP Component | FastAPI Equivalent | Notes |
|---------------|-------------------|-------|
| `system/library/cart/cart.php` | `app/services/cart_service.py` | Cart logic |
| Session storage | Database storage | Persistent cart per user |
| `catalog/controller/checkout/cart.php` | `app/routers/cart.py` | API endpoints |

**Key Endpoints:**
```
GET    /api/cart             → Get current cart
POST   /api/cart/items       → Add item to cart
PUT    /api/cart/items/{id}  → Update cart item quantity
DELETE /api/cart/items/{id}  → Remove cart item
DELETE /api/cart             → Clear cart
GET    /api/cart/totals      → Get cart totals
```

#### Customer Module

| PHP Component | FastAPI Equivalent | Notes |
|---------------|-------------------|-------|
| `catalog/model/account/customer.php` | `app/models/customer.py` | Customer model |
| `catalog/controller/account/` | `app/routers/customers.py` | Customer API |
| `catalog/controller/account/login.php` | `app/routers/auth.py` | Authentication |

**Key Endpoints:**
```
POST   /api/auth/register   → Register new customer
POST   /api/auth/login      → Login (returns JWT)
POST   /api/auth/logout     → Logout (invalidate token)
POST   /api/auth/reset      → Password reset request
GET    /api/customers/me    → Get current customer profile
PUT    /api/customers/me    → Update profile
GET    /api/customers/me/addresses  → List addresses
POST   /api/customers/me/addresses  → Add address
```

#### Order Module

| PHP Component | FastAPI Equivalent | Notes |
|---------------|-------------------|-------|
| `catalog/model/checkout/order.php` | `app/models/order.py` | Order models |
| `catalog/controller/checkout/checkout.php` | `app/routers/checkout.py` | Checkout API |
| `catalog/controller/checkout/confirm.php` | `app/routers/orders.py` | Order placement |

**Key Endpoints:**
```
POST   /api/checkout/validate-address     → Validate address
POST   /api/checkout/shipping-methods     → Get shipping methods
POST   /api/checkout/payment-methods      → Get payment methods
POST   /api/orders                        → Create order
GET    /api/orders                        → List customer orders
GET    /api/orders/{id}                   → Get order details
```

#### Admin Module

| PHP Component | FastAPI Equivalent | Notes |
|---------------|-------------------|-------|
| `admin/controller/catalog/product.php` | `app/routers/admin/products.py` | Admin product API |
| `admin/controller/sale/order.php` | `app/routers/admin/orders.py` | Admin order API |
| `admin/controller/customer/customer.php` | `app/routers/admin/customers.py` | Admin customer API |

**Key Endpoints:**
```
POST   /api/admin/products          → Create product
PUT    /api/admin/products/{id}     → Update product
DELETE /api/admin/products/{id}     → Delete product
POST   /api/admin/products/{id}/images → Upload image
GET    /api/admin/orders            → List all orders
PUT    /api/admin/orders/{id}/status → Update order status
POST   /api/admin/orders/{id}/history → Add order history
```

### PHP → React Frontend Mapping

#### Pages

| PHP Template | React Page Component | Route |
|--------------|---------------------|-------|
| `product/product.twig` | `<ProductDetail />` | `/products/:id` |
| `product/category.twig` | `<CategoryPage />` | `/categories/:id` |
| `product/search.twig` | `<SearchResults />` | `/search` |
| `common/home.twig` | `<HomePage />` | `/` |
| `checkout/cart.twig` | `<CartPage />` | `/cart` |
| `checkout/checkout.twig` | `<CheckoutPage />` | `/checkout` |
| `checkout/success.twig` | `<OrderSuccess />` | `/checkout/success` |
| `account/login.twig` | `<LoginPage />` | `/account/login` |
| `account/register.twig` | `<RegisterPage />` | `/account/register` |
| `account/account.twig` | `<AccountDashboard />` | `/account` |
| `account/order.twig` | `<OrderHistory />` | `/account/orders` |
| `admin/` (all) | Admin React app | `/admin/*` |

#### Components

| PHP Partial | React Component | Usage |
|-------------|-----------------|-------|
| `common/header.twig` | `<Header />` | Site header with nav |
| `common/footer.twig` | `<Footer />` | Site footer |
| `common/menu.twig` | `<MainMenu />` | Category navigation |
| `common/cart.twig` | `<CartIcon />` | Cart badge in header |
| `product/thumb.twig` | `<ProductCard />` | Product listing item |
| `checkout/payment_address.twig` | `<AddressForm />` | Address input form |
| `common/pagination.twig` | `<Pagination />` | Pagination controls |

---

## Non-Functional Requirements

### Performance

**Target Metrics:**
- API response time: < 200ms (p95)
- Page load time: < 2s (first contentful paint)
- Time to interactive: < 3s
- Database query time: < 50ms (p95)

**Optimizations:**
- Database indexing on frequently queried columns
- API response caching (Redis optional)
- React code splitting for faster initial load
- Image optimization and lazy loading
- CDN for static assets (production)

### Scalability

**Backend:**
- Stateless API design (no server-side sessions)
- Horizontal scaling ready (multiple FastAPI instances)
- Database connection pooling
- Async request handling with FastAPI

**Frontend:**
- Static React build can be served from CDN
- API calls batched where possible
- Lazy loading of routes and components

### Reliability

**Availability:**
- Target: 99.9% uptime (development environment)
- Graceful degradation on API failures
- Retry logic for transient errors

**Error Handling:**
- Comprehensive exception handling in backend
- User-friendly error messages in frontend
- Logging of all errors for debugging
- Transaction rollback on failures

### Security

**Authentication:**
- JWT tokens with expiration (1 hour access token)
- Secure password hashing (bcrypt)
- HTTPS required in production
- CORS configuration for allowed origins

**Input Validation:**
- Pydantic schemas validate all API inputs
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via React escaping
- File upload validation (type, size)

**Authorization:**
- JWT token verification on protected endpoints
- Admin-only endpoints require admin role
- Customer can only access own data

### Maintainability

**Code Quality:**
- Type hints in Python (backend)
- ESLint and Prettier for React (frontend)
- Consistent naming conventions
- Comprehensive docstrings and comments

**Testing:**
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Minimum 70% code coverage

**Documentation:**
- Auto-generated API docs (OpenAPI/Swagger)
- Component storybook for React components
- README files in each module
- Architecture decision records (ADRs)

### Observability

**Logging:**
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging for debugging
- Error stack traces captured

**Monitoring:**
- API endpoint metrics (request count, latency)
- Database query performance
- Error rate tracking
- User activity analytics (optional)

---

## Summary

This migration transforms OpenCart from a monolithic PHP application to a modern, decoupled architecture:

**Backend (FastAPI):**
- RESTful API exposing business logic
- SQLite database (adaptable to PostgreSQL/MySQL)
- JWT-based authentication
- Stateless design for scalability

**Frontend (React):**
- Single-page application (SPA)
- Component-based UI
- API-driven data fetching
- Modern user experience

**Key Goals:**
- 100% behavior preservation
- Improved maintainability and scalability
- Enhanced security
- API-first architecture enabling future expansion

**Next Steps:**
- Design target architecture (HLD)
- Define detailed module specifications (LLD)
- Create migration execution plan

---

**Next Document**: [04-migration-architecture-hld.md](./04-migration-architecture-hld.md)
