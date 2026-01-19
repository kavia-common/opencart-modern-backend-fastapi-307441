"""
Dependency Injection Utilities
Common dependencies for FastAPI endpoints
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db


# Placeholder for common dependencies
# Can be extended with caching, logging, etc.
