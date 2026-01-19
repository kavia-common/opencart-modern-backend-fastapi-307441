"""
Product Service Unit Tests
Tests for product business logic
"""
import pytest
from sqlalchemy.orm import Session
from app.services.product_service import ProductService
from app.utils.exceptions import ProductNotFoundException


@pytest.mark.unit
@pytest.mark.database
def test_get_products_empty_database(db: Session):
    """Test getting products from empty database."""
    service = ProductService(db)
    result = service.get_products()
    
    assert result["total"] == 0
    assert len(result["items"]) == 0
    assert result["pages"] == 0


@pytest.mark.unit
@pytest.mark.database
def test_get_products_with_pagination(db: Session, test_products):
    """Test product pagination."""
    service = ProductService(db)
    
    # Get first page
    result = service.get_products(page=1, limit=2)
    
    assert result["total"] == 5
    assert len(result["items"]) == 2
    assert result["page"] == 1
    assert result["limit"] == 2
    assert result["pages"] == 3


@pytest.mark.unit
@pytest.mark.database
def test_get_products_filter_by_category(db: Session, test_products, test_category):
    """Test filtering products by category."""
    service = ProductService(db)
    result = service.get_products(category_id=test_category.category_id)
    
    assert result["total"] == 5
    assert len(result["items"]) == 5


@pytest.mark.unit
@pytest.mark.database
def test_get_products_search(db: Session, test_products):
    """Test product search functionality."""
    service = ProductService(db)
    result = service.get_products(search="Product 1")
    
    # Should find "Test Product 1"
    assert result["total"] >= 1
    product_names = [item.name for item in result["items"]]
    assert any("Product 1" in name for name in product_names)


@pytest.mark.unit
@pytest.mark.database
def test_get_products_sort_by_price_asc(db: Session, test_products):
    """Test sorting products by price ascending."""
    service = ProductService(db)
    result = service.get_products(sort="price", order="asc")
    
    prices = [item.price for item in result["items"]]
    assert prices == sorted(prices)


@pytest.mark.unit
@pytest.mark.database
def test_get_products_sort_by_price_desc(db: Session, test_products):
    """Test sorting products by price descending."""
    service = ProductService(db)
    result = service.get_products(sort="price", order="desc")
    
    prices = [item.price for item in result["items"]]
    assert prices == sorted(prices, reverse=True)


@pytest.mark.unit
@pytest.mark.database
def test_get_product_detail_success(db: Session, test_product):
    """Test getting product detail."""
    service = ProductService(db)
    result = service.get_product_detail(test_product.product_id)
    
    assert result.product_id == test_product.product_id
    assert result.name == "Test Product"
    assert result.model == "TEST-001"
    assert result.price == 29.99
    assert result.description is not None


@pytest.mark.unit
@pytest.mark.database
def test_get_product_detail_not_found(db: Session):
    """Test getting non-existent product raises exception."""
    service = ProductService(db)
    
    with pytest.raises(ProductNotFoundException):
        service.get_product_detail(99999)


@pytest.mark.unit
@pytest.mark.database
def test_get_product_detail_increments_views(db: Session, test_product):
    """Test that getting product detail increments view count."""
    service = ProductService(db)
    initial_views = test_product.viewed
    
    service.get_product_detail(test_product.product_id)
    
    db.refresh(test_product)
    assert test_product.viewed == initial_views + 1
