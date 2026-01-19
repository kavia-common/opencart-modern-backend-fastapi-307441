"""
Cart Endpoint Tests
Tests for shopping cart operations
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.integration
def test_get_empty_cart(client: TestClient, auth_headers):
    """Test getting empty cart."""
    response = client.get("/api/v1/cart", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert "totals" in data


@pytest.mark.integration
def test_add_to_cart_success(client: TestClient, auth_headers, test_product):
    """Test adding product to cart."""
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 2,
        "options": {}
    }
    
    response = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert "cart_id" in data
    assert data["message"] == "Item added to cart"


@pytest.mark.integration
def test_add_to_cart_without_auth(client: TestClient, test_product):
    """Test adding to cart without authentication fails."""
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 1,
        "options": {}
    }
    
    response = client.post("/api/v1/cart/items", json=cart_item)
    
    assert response.status_code == 403  # Forbidden


@pytest.mark.integration
def test_add_to_cart_invalid_product(client: TestClient, auth_headers):
    """Test adding non-existent product to cart fails."""
    cart_item = {
        "product_id": 99999,
        "quantity": 1,
        "options": {}
    }
    
    response = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    
    assert response.status_code == 404


@pytest.mark.integration
def test_add_to_cart_insufficient_stock(client: TestClient, auth_headers, test_product):
    """Test adding more quantity than available stock fails."""
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 1000,  # More than available
        "options": {}
    }
    
    response = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    
    assert response.status_code == 400
    data = response.json()
    assert "stock" in data["detail"].lower()


@pytest.mark.integration
def test_get_cart_with_items(client: TestClient, auth_headers, test_product):
    """Test getting cart after adding items."""
    # Add item to cart first
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 2,
        "options": {}
    }
    client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    
    # Get cart
    response = client.get("/api/v1/cart", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product.product_id
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["name"] == "Test Product"
    
    # Check totals
    assert len(data["totals"]) > 0
    total_line = next((t for t in data["totals"] if t["code"] == "total"), None)
    assert total_line is not None
    assert total_line["value"] > 0


@pytest.mark.integration
def test_update_cart_item(client: TestClient, auth_headers, test_product):
    """Test updating cart item quantity."""
    # Add item first
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 2,
        "options": {}
    }
    add_response = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    cart_id = add_response.json()["cart_id"]
    
    # Update quantity
    update_data = {"quantity": 5}
    response = client.put(f"/api/v1/cart/items/{cart_id}", json=update_data, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Cart item updated"


@pytest.mark.integration
def test_remove_cart_item(client: TestClient, auth_headers, test_product):
    """Test removing item from cart."""
    # Add item first
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 2,
        "options": {}
    }
    add_response = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    cart_id = add_response.json()["cart_id"]
    
    # Remove item
    response = client.delete(f"/api/v1/cart/items/{cart_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item removed from cart"
    
    # Verify cart is empty
    cart_response = client.get("/api/v1/cart", headers=auth_headers)
    assert len(cart_response.json()["items"]) == 0


@pytest.mark.integration
def test_add_same_product_twice_increments_quantity(client: TestClient, auth_headers, test_product):
    """Test adding the same product twice increments quantity instead of creating duplicate."""
    cart_item = {
        "product_id": test_product.product_id,
        "quantity": 2,
        "options": {}
    }
    
    # Add first time
    response1 = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    cart_id1 = response1.json()["cart_id"]
    
    # Add second time
    response2 = client.post("/api/v1/cart/items", json=cart_item, headers=auth_headers)
    cart_id2 = response2.json()["cart_id"]
    
    # Should return same cart_id
    assert cart_id1 == cart_id2
    
    # Verify quantity is updated
    cart_response = client.get("/api/v1/cart", headers=auth_headers)
    items = cart_response.json()["items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 4  # 2 + 2
