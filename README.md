# OpenCart Modern Backend - FastAPI

Modern REST API backend for OpenCart e-commerce platform, migrated from PHP to FastAPI with SQLite database.

## Overview

This is a **standalone FastAPI backend** that runs independently using SQLite. It does NOT require the legacy PHP OpenCart container (opencart-307441) to be running.

This is a behavior-preserving migration of OpenCart 3.0.7.4 from PHP to FastAPI (Python), providing:

- RESTful API endpoints for all core e-commerce functionality
- JWT-based authentication
- SQLite database (compatible with OpenCart schema)
- Auto-generated OpenAPI/Swagger documentation
- Modular, maintainable architecture
- **Independent operation** - no runtime dependencies on PHP services

## Features

- **Authentication**: Customer registration and login with JWT tokens
- **Product Catalog**: Browse, search, and filter products with pagination
- **Categories**: Hierarchical category navigation
- **Shopping Cart**: Add, update, remove items with real-time totals
- **Checkout**: Place orders with shipping and payment method selection
- **Order Management**: View order history and details
- **Admin Panel**: Order management and status updates

## Architecture

### Standalone Operation

The FastAPI backend is completely self-contained:
- Uses SQLite for data persistence (no external database required)
- Implements all business logic internally
- No runtime checks or dependencies on the PHP OpenCart container
- Can be started, tested, and used independently
- All environment variables have sane defaults

### Application Structure

The application follows a layered architecture:

```
app/
├── api/            # API endpoints (thin controllers)
├── services/       # Business logic layer
├── repositories/   # Data access layer
├── models/
│   ├── database/   # SQLAlchemy ORM models
│   └── schemas/    # Pydantic request/response models
├── core/           # Core utilities (config, security, database)
└── utils/          # Helper functions
```

## Prerequisites

- Python 3.8+
- pip or pipenv

## Installation

1. **Clone the repository** (if not already done)

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env and set SECRET_KEY to a random string
```

**Note**: The application will run with default configuration even without a `.env` file.

5. **Initialize database**:
The database will be created automatically on first run. Tables are created via SQLAlchemy on startup.

## Quick Start

For the impatient, here's the fastest way to get started:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Open your browser to http://localhost:8000/docs
```

That's it! The database will be created automatically, and you can start exploring the API through Swagger UI.

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Options:
- `--reload` - Auto-reload on code changes
- `--host 0.0.0.0` - Listen on all interfaces
- `--port 8000` - Port number

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, consider:
- Multiple workers (`--workers 4`)
- Process manager (systemd, supervisord)
- Reverse proxy (nginx, Apache)
- HTTPS/TLS termination

### Using Environment Variables

```bash
# Set environment variables
export LOG_LEVEL=DEBUG
export ENVIRONMENT=production

# Or use .env file
cp .env.example .env
# Edit .env with your settings

# Run the server
uvicorn app.main:app
```

The server will start immediately without waiting for any external services.

### Accessing the API

Once running:
1. **Swagger UI**: http://localhost:8000/docs - Interactive API testing
2. **ReDoc**: http://localhost:8000/redoc - Alternative documentation
3. **Health check**: http://localhost:8000/health - Verify server is up
4. **API Info**: http://localhost:8000/ - Get API metadata

## API Documentation

Once the server is running, you can access comprehensive interactive API documentation:

### Swagger UI (Recommended)
**URL**: http://localhost:8000/docs

Swagger UI provides:
- Interactive API exploration and testing
- Try out API endpoints directly from the browser
- View request/response schemas
- Authentication support (click "Authorize" to add JWT token)
- Request examples and response codes

### ReDoc
**URL**: http://localhost:8000/redoc

ReDoc provides:
- Clean, three-panel documentation layout
- Detailed schema descriptions
- Code samples in multiple languages
- Searchable endpoint reference

### OpenAPI Specification
**URL**: http://localhost:8000/openapi.json

Download the raw OpenAPI 3.0 specification for:
- Code generation tools
- API clients in various languages
- Integration with third-party tools
- Custom documentation generation

### Root API Information
**URL**: http://localhost:8000/

Get API metadata and quick links to all documentation endpoints.

## Monitoring and Health Checks

The API provides several endpoints for monitoring and orchestration:

### Health Check
**Endpoint**: `GET /health`

Always returns `200 OK` if the application is running. Use this for:
- Load balancer health checks
- Basic uptime monitoring
- Container orchestration liveness probes

**Response**:
```json
{
  "status": "healthy"
}
```

### Readiness Check
**Endpoint**: `GET /ready`

Verifies the application is ready to accept traffic by checking:
- Database connectivity
- Critical dependencies

Returns `200 OK` when ready, `503 Service Unavailable` when not ready. Use this for:
- Kubernetes readiness probes
- Deployment verification
- Service orchestration

**Response** (when ready):
```json
{
  "status": "ready",
  "checks": {
    "database": "connected",
    "overall": "ready"
  }
}
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new customer
- `POST /api/v1/auth/login` - Login and get JWT token

### Products
- `GET /api/v1/products` - List products (with pagination, search, filters)
- `GET /api/v1/products/{id}` - Get product details

### Categories
- `GET /api/v1/categories` - List all categories

### Cart (Authenticated)
- `GET /api/v1/cart` - Get current cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{id}` - Update cart item
- `DELETE /api/v1/cart/items/{id}` - Remove cart item

### Checkout (Authenticated)
- `POST /api/v1/checkout/shipping-methods` - Get shipping options
- `POST /api/v1/checkout/payment-methods` - Get payment options
- `POST /api/v1/checkout/confirm` - Place order

### Orders (Authenticated)
- `GET /api/v1/orders` - Get order history
- `GET /api/v1/orders/{id}` - Get order details

### Admin (Admin Only)
- `GET /api/v1/admin/orders` - List all orders
- `PUT /api/v1/admin/orders/{id}/status` - Update order status

## Authentication

Most endpoints require JWT authentication. Include the token in requests:

```
Authorization: Bearer <your-jwt-token>
```

Get a token by registering or logging in via the `/auth` endpoints.

## Database

The application uses SQLite with a schema compatible with OpenCart's MySQL structure:

- **Location**: `data/opencart.db`
- **Tables**: Products, Categories, Customers, Orders, Cart, etc.
- **Migrations**: Managed via Alembic (optional)
- **Auto-initialization**: Tables created automatically on first startup

## Testing

Run tests with pytest:

```bash
pytest
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options:

#### Application Settings
- `APP_NAME` - Application name (default: OpenCart Modern API)
- `APP_VERSION` - API version (default: 1.0.0)
- `DEBUG` - Enable debug mode (default: False)
- `ENVIRONMENT` - Environment name: development, staging, production (default: development)

#### Server Settings
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of worker processes (default: 1)

#### Logging
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- `LOG_FORMAT` - Log format: text or json (default: text)

#### Security
- `SECRET_KEY` - JWT signing key (MUST be changed in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time (default: 60)

#### Database
- `DATABASE_URL` - Database connection string (default: sqlite:///./data/opencart.db)

#### CORS
- `ALLOWED_ORIGINS` - Allowed origins for CORS (default: localhost:3000, localhost:5173)
  - Can be JSON array: `["http://localhost:3000","http://localhost:5173"]`
  - Or comma-separated: `http://localhost:3000,http://localhost:5173`

#### API Configuration
- `API_V1_PREFIX` - API v1 URL prefix (default: /api/v1)
- `DOCS_URL` - Swagger UI path (default: /docs)
- `REDOC_URL` - ReDoc path (default: /redoc)
- `OPENAPI_URL` - OpenAPI spec path (default: /openapi.json)

#### Pagination
- `DEFAULT_PAGE_SIZE` - Default page size (default: 20)
- `MAX_PAGE_SIZE` - Maximum page size (default: 100)

**All variables have sane defaults** - the application will run without a `.env` file.

### Logging

The application uses structured logging with configurable levels and formats:

- **Text format** (default): Human-readable console output
- **JSON format**: Structured logs for log aggregation systems

To enable JSON logging, set `LOG_FORMAT=json` in your `.env` file.

Log levels (from most to least verbose):
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages (recommended for production)
- `WARNING` - Warning messages for potentially harmful situations
- `ERROR` - Error messages for failures
- `CRITICAL` - Critical errors that may cause shutdown

Example log output (text format):
```
2024-01-15 10:30:45 - app.main - INFO - OpenCart Modern API v1.0.0 starting up
2024-01-15 10:30:45 - app.main - INFO - Environment: development
2024-01-15 10:30:45 - app.main - INFO - Documentation available at: /docs
```

Example log output (JSON format):
```json
{"timestamp": "2024-01-15T10:30:45.123456", "level": "INFO", "logger": "app.main", "message": "OpenCart Modern API v1.0.0 starting up"}
```

## Migration from PHP OpenCart

This backend is a 1:1 behavioral migration from OpenCart PHP. It preserves:

- Business logic and workflows
- Data structures and relationships
- API contracts and response formats

**Important**: While this backend was migrated from PHP OpenCart, it is now a standalone service. There is no runtime dependency on the PHP codebase or container.

See `/docs` for detailed migration documentation.

## Development

### Adding New Endpoints

1. Create endpoint in `app/api/v1/endpoints/`
2. Add business logic in `app/services/`
3. Add data access in `app/repositories/`
4. Define schemas in `app/models/schemas/`
5. Register router in `app/api/v1/router.py`

### Code Style

- Follow PEP 8
- Use type hints
- Document all public functions with docstrings
- Mark public interfaces with `# PUBLIC_INTERFACE` comment

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate secure `SECRET_KEY`
3. Configure CORS origins for your frontend
4. Use a production ASGI server (e.g., uvicorn with multiple workers)
5. Set up reverse proxy (nginx/Apache)
6. Enable HTTPS

## Troubleshooting

### Backend won't start

- **Check Python version**: Requires Python 3.8+
- **Verify dependencies**: Run `pip install -r requirements.txt`
- **Check port availability**: Default port 8000 might be in use
- **Database permissions**: Ensure write access to `data/` directory

### No external dependencies required

This backend is designed to start immediately without:
- External database servers
- PHP services
- Legacy OpenCart containers
- Configuration from external sources

If the backend refuses to start, check only Python and dependency issues, not external services.

## License

Same as OpenCart (GPL v3)

## Support

For questions or issues:
- Review API documentation at `/docs`
- Check migration docs in `/docs` folder
- Refer to OpenCart source for behavior verification
