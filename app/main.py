"""
FastAPI Application Entry Point
OpenCart Modern Backend - FastAPI Migration
"""
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import api_router
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
setup_logging(
    log_level=settings.LOG_LEVEL,
    use_json=(settings.LOG_FORMAT.lower() == "json")
)

logger = get_logger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise

# PUBLIC_INTERFACE
def create_application() -> FastAPI:
    """
    Create and configure FastAPI application instance.
    
    This function initializes the FastAPI app with:
    - OpenAPI/Swagger documentation
    - CORS middleware
    - API routes
    - Global exception handlers
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        ## Modern REST API for OpenCart E-commerce Platform
        
        This API provides comprehensive e-commerce functionality including:
        - Customer authentication and registration
        - Product catalog with search and filtering
        - Shopping cart management
        - Order processing and checkout
        - Admin operations
        
        ### Authentication
        Most endpoints require JWT authentication. Include the token in the Authorization header:
        ```
        Authorization: Bearer <your-jwt-token>
        ```
        
        ### Rate Limiting
        API requests may be rate-limited. Check response headers for rate limit information.
        
        ### Support
        For questions or issues, refer to the API documentation or contact support.
        """,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
        openapi_tags=[
            {
                "name": "root",
                "description": "Root endpoints for API information and health checks"
            },
            {
                "name": "auth",
                "description": "Authentication and registration operations. Use these endpoints to register new customers and obtain JWT tokens for API access."
            },
            {
                "name": "products",
                "description": "Product catalog operations. Browse, search, and filter products with pagination support."
            },
            {
                "name": "categories",
                "description": "Category management operations. Navigate the hierarchical category structure."
            },
            {
                "name": "cart",
                "description": "Shopping cart operations. Add, update, and remove items from the cart. Requires authentication."
            },
            {
                "name": "checkout",
                "description": "Checkout and order placement operations. Complete the purchase process. Requires authentication."
            },
            {
                "name": "orders",
                "description": "Order history and details operations. View past orders and their status. Requires authentication."
            },
            {
                "name": "customers",
                "description": "Customer profile operations. Manage customer information. Requires authentication."
            },
            {
                "name": "admin",
                "description": "Administrative operations. Manage orders and system configuration. Requires admin role."
            },
        ],
        contact={
            "name": "OpenCart Modern API Support",
            "url": "https://github.com/opencart/opencart",
        },
        license_info={
            "name": "GPL v3",
            "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
        },
    )
    
    logger.info(f"Initializing {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS configured with origins: {settings.ALLOWED_ORIGINS}")
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    logger.info(f"API routes registered at {settings.API_V1_PREFIX}")
    
    return app


app = create_application()


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with structured response.
    
    Args:
        request: FastAPI request object
        exc: Validation error exception
        
    Returns:
        JSONResponse with error details
    """
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions with structured response.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSONResponse with error details
    """
    logger.warning(f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors globally.
    
    Args:
        request: FastAPI request object
        exc: Exception that occurred
        
    Returns:
        JSONResponse with generic error message
    """
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    
    # Don't expose internal errors in production
    detail = str(exc) if settings.DEBUG else "An unexpected error occurred"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": detail
            }
        }
    )


# Lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    """
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Documentation available at: {settings.DOCS_URL}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    """
    logger.info(f"{settings.APP_NAME} shutting down")


# PUBLIC_INTERFACE
@app.get("/", tags=["root"], summary="API Information")
async def root():
    """
    Root endpoint providing API information and navigation links.
    
    Returns:
        dict: API metadata including version, status, and documentation links
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "documentation": {
            "swagger": settings.DOCS_URL,
            "redoc": settings.REDOC_URL,
            "openapi": settings.OPENAPI_URL
        },
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "api": settings.API_V1_PREFIX
        }
    }


# PUBLIC_INTERFACE
@app.get("/health", tags=["root"], summary="Health Check")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    This endpoint always returns 200 OK if the application is running.
    It indicates the application process is alive but doesn't check dependencies.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}


# PUBLIC_INTERFACE
@app.get("/ready", tags=["root"], summary="Readiness Check")
async def readiness_check():
    """
    Readiness check endpoint for monitoring and orchestration.
    
    This endpoint verifies that the application is ready to accept traffic
    by checking critical dependencies like database connectivity.
    
    Returns:
        dict: Readiness status with dependency checks
        
    Raises:
        HTTPException: If any critical dependency is unavailable
    """
    checks = {
        "database": "unknown",
        "overall": "ready"
    }
    
    # Check database connectivity
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            # Simple query to verify database is accessible
            db.execute(text("SELECT 1"))
            checks["database"] = "connected"
        except SQLAlchemyError as e:
            logger.error(f"Database check failed: {e}")
            checks["database"] = "disconnected"
            checks["overall"] = "not_ready"
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Failed to check database: {e}")
        checks["database"] = "error"
        checks["overall"] = "not_ready"
    
    if checks["overall"] != "ready":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        )
    
    return {
        "status": checks["overall"],
        "checks": checks
    }
