"""
Cart Service Unit Tests
Tests for cart business logic
"""
import pytest
from sqlalchemy.orm import Session
from app.services.cart_service import CartService
from app.utils.exceptions import ProductNotFoundException, InsufficientStockException


@pytest.mark.unit
@pytest.mark.database
def test_add_item_to_cart_success(db: Session, test_customer, test_product):
    """Test adding item to cart."""
    service = CartService(db)
    
    cart_id = service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=2,
        options={}
    )
    
    assert cart_id is not None
    assert isinstance(cart_id, int)


@pytest.mark.unit
@pytest.mark.database
def test_add_item_invalid_product(db: Session, test_customer):
    """Test adding non-existent product raises exception."""
    service = CartService(db)
    
    with pytest.raises(ProductNotFoundException):
        service.add_item(
            customer_id=test_customer.customer_id,
            product_id=99999,
            quantity=1,
            options={}
        )


@pytest.mark.unit
@pytest.mark.database
def test_add_item_insufficient_stock(db: Session, test_customer, test_product):
    """Test adding more than available stock raises exception."""
    service = CartService(db)
    
    with pytest.raises(InsufficientStockException):
        service.add_item(
            customer_id=test_customer.customer_id,
            product_id=test_product.product_id,
            quantity=1000,  # More than available
            options={}
        )


@pytest.mark.unit
@pytest.mark.database
def test_add_same_item_twice_increments_quantity(db: Session, test_customer, test_product):
    """Test adding same product twice increments quantity."""
    service = CartService(db)
    
    cart_id1 = service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=2,
        options={}
    )
    
    cart_id2 = service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=3,
        options={}
    )
    
    # Should return same cart item
    assert cart_id1 == cart_id2
    
    # Verify total quantity
    cart = service.get_cart(test_customer.customer_id)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 5


@pytest.mark.unit
@pytest.mark.database
def test_get_empty_cart(db: Session, test_customer):
    """Test getting empty cart."""
    service = CartService(db)
    cart = service.get_cart(test_customer.customer_id)
    
    assert len(cart.items) == 0
    assert len(cart.totals) > 0  # Should still have total lines


@pytest.mark.unit
@pytest.mark.database
def test_get_cart_with_items(db: Session, test_customer, test_product):
    """Test getting cart with items."""
    service = CartService(db)
    
    # Add item
    service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=2,
        options={}
    )
    
    # Get cart
    cart = service.get_cart(test_customer.customer_id)
    
    assert len(cart.items) == 1
    assert cart.items[0].product_id == test_product.product_id
    assert cart.items[0].quantity == 2
    assert cart.items[0].name == "Test Product"
    
    # Verify totals calculation
    subtotal = next((t for t in cart.totals if t.code == "sub_total"), None)
    assert subtotal is not None
    assert subtotal.value == test_product.price * 2


@pytest.mark.unit
@pytest.mark.database
def test_update_cart_item_quantity(db: Session, test_customer, test_product):
    """Test updating cart item quantity."""
    service = CartService(db)
    
    # Add item
    cart_id = service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=2,
        options={}
    )
    
    # Update quantity
    service.update_item(cart_id, 5, test_customer.customer_id)
    
    # Verify
    cart = service.get_cart(test_customer.customer_id)
    assert cart.items[0].quantity == 5


@pytest.mark.unit
@pytest.mark.database
def test_remove_cart_item(db: Session, test_customer, test_product):
    """Test removing item from cart."""
    service = CartService(db)
    
    # Add item
    cart_id = service.add_item(
        customer_id=test_customer.customer_id,
        product_id=test_product.product_id,
        quantity=2,
        options={}
    )
    
    # Remove item
    service.remove_item(cart_id, test_customer.customer_id)
    
    # Verify cart is empty
    cart = service.get_cart(test_customer.customer_id)
    assert len(cart.items) == 0


@pytest.mark.unit
@pytest.mark.database
def test_clear_cart(db: Session, test_customer, test_product):
    """Test clearing entire cart."""
    service = CartService(db)
    
    # Add multiple items
    service.add_item(test_customer.customer_id, test_product.product_id, 2, {})
    
    # Clear cart
    service.clear_cart(test_customer.customer_id)
    
    # Verify cart is empty
    cart = service.get_cart(test_customer.customer_id)
    assert len(cart.items) == 0


@pytest.mark.unit
@pytest.mark.database
def test_cart_totals_calculation(db: Session, test_customer, test_product):
    """Test cart totals are calculated correctly."""
    service = CartService(db)
    
    # Add item with known price
    service.add_item(test_customer.customer_id, test_product.product_id, 2, {})
    
    cart = service.get_cart(test_customer.customer_id)
    
    # Verify totals structure
    total_codes = [t.code for t in cart.totals]
    assert "sub_total" in total_codes
    assert "shipping" in total_codes
    assert "tax" in total_codes
    assert "total" in total_codes
    
    # Verify calculations
    subtotal = next(t for t in cart.totals if t.code == "sub_total")
    total = next(t for t in cart.totals if t.code == "total")
    
    assert subtotal.value == test_product.price * 2
    assert total.value > subtotal.value  # Should include shipping and tax
