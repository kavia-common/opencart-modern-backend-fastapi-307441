"""
Authentication Endpoint Tests
Tests for customer registration and login
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import verify_password


@pytest.mark.integration
def test_register_customer_success(client: TestClient, db: Session):
    """Test successful customer registration."""
    customer_data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "telephone": "1234567890",
        "password": "SecurePass123"
    }
    
    response = client.post("/api/v1/auth/register", json=customer_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == customer_data["email"]
    assert data["firstname"] == customer_data["firstname"]
    assert data["lastname"] == customer_data["lastname"]
    assert "password" not in data  # Password should not be returned


@pytest.mark.integration
def test_register_customer_duplicate_email(client: TestClient, test_customer):
    """Test registration with duplicate email fails."""
    customer_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "email": test_customer.email,  # Use existing email
        "telephone": "0987654321",
        "password": "SecurePass123"
    }
    
    response = client.post("/api/v1/auth/register", json=customer_data)
    
    assert response.status_code == 400
    data = response.json()
    assert "already exists" in data["detail"].lower()


@pytest.mark.integration
def test_register_customer_short_password(client: TestClient):
    """Test registration with short password fails validation."""
    customer_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "email": "jane@example.com",
        "telephone": "0987654321",
        "password": "123"  # Too short, minimum is 6 characters
    }
    
    response = client.post("/api/v1/auth/register", json=customer_data)
    
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_login_success(client: TestClient, test_customer):
    """Test successful customer login."""
    credentials = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", json=credentials)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "customer" in data
    assert data["customer"]["email"] == credentials["email"]


@pytest.mark.integration
def test_login_invalid_email(client: TestClient):
    """Test login with non-existent email fails."""
    credentials = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", json=credentials)
    
    assert response.status_code == 401
    data = response.json()
    assert "invalid" in data["detail"].lower()


@pytest.mark.integration
def test_login_invalid_password(client: TestClient, test_customer):
    """Test login with wrong password fails."""
    credentials = {
        "email": test_customer.email,
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=credentials)
    
    assert response.status_code == 401
    data = response.json()
    assert "invalid" in data["detail"].lower()


@pytest.mark.integration
def test_register_customer_missing_fields(client: TestClient):
    """Test registration with missing required fields fails."""
    customer_data = {
        "email": "incomplete@example.com",
        "password": "SecurePass123"
        # Missing other required fields
    }
    
    response = client.post("/api/v1/auth/register", json=customer_data)
    
    assert response.status_code == 422  # Validation error
