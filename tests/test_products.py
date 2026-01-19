"""
Product Endpoint Tests
Tests for product catalog operations
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.integration
def test_list_products_empty(client: TestClient, db: Session):
    """Test listing products when none exist."""
    response = client.get("/api/v1/products")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.integration
def test_list_products_with_data(client: TestClient, test_products):
    """Test listing products with pagination."""
    response = client.get("/api/v1/products?page=1&limit=3")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 3
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["limit"] == 3
    assert data["pages"] == 2


@pytest.mark.integration
def test_list_products_second_page(client: TestClient, test_products):
    """Test pagination to second page."""
    response = client.get("/api/v1/products?page=2&limit=3")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2  # Remaining 2 items
    assert data["page"] == 2


@pytest.mark.integration
def test_list_products_filter_by_category(client: TestClient, test_products, test_category):
    """Test filtering products by category."""
    response = client.get(f"/api/v1/products?category_id={test_category.category_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5  # All test products belong to this category


@pytest.mark.integration
def test_list_products_search(client: TestClient, test_products):
    """Test searching products by name."""
    response = client.get("/api/v1/products?search=Product 1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1  # At least one match


@pytest.mark.integration
def test_list_products_sort_by_price(client: TestClient, test_products):
    """Test sorting products by price."""
    response = client.get("/api/v1/products?sort=price&order=asc")
    
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    # Verify ascending price order
    for i in range(len(items) - 1):
        assert items[i]["price"] <= items[i + 1]["price"]


@pytest.mark.integration
def test_get_product_detail_success(client: TestClient, test_product):
    """Test getting product details."""
    response = client.get(f"/api/v1/products/{test_product.product_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == test_product.product_id
    assert data["name"] == "Test Product"
    assert data["model"] == "TEST-001"
    assert data["price"] == 29.99
    assert "description" in data
    assert "images" in data


@pytest.mark.integration
def test_get_product_detail_not_found(client: TestClient):
    """Test getting non-existent product fails."""
    response = client.get("/api/v1/products/99999")
    
    assert response.status_code == 404


@pytest.mark.integration
def test_get_product_detail_increments_view_count(client: TestClient, test_product, db: Session):
    """Test that viewing a product increments the view counter."""
    initial_views = test_product.viewed
    
    response = client.get(f"/api/v1/products/{test_product.product_id}")
    
    assert response.status_code == 200
    
    # Refresh from database
    db.refresh(test_product)
    assert test_product.viewed == initial_views + 1


@pytest.mark.integration
def test_list_products_invalid_page(client: TestClient, test_products):
    """Test listing products with invalid page number."""
    response = client.get("/api/v1/products?page=0")
    
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_list_products_large_limit(client: TestClient, test_products):
    """Test listing products with limit exceeding max."""
    response = client.get("/api/v1/products?limit=200")
    
    # Should be constrained by MAX_PAGE_SIZE (100)
    assert response.status_code == 422
