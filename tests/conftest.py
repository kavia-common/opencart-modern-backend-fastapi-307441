"""
Test Configuration and Fixtures
Provides common test fixtures and setup for pytest
"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

from app.main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.models.database.customer import Customer
from app.models.database.product import Product, ProductDescription, ProductToCategory
from app.models.database.category import Category, CategoryDescription
from app.models.database.cart import Cart

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test_opencart.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_customer(db: Session) -> Customer:
    """
    Create a test customer.
    """
    customer = Customer(
        customer_group_id=1,
        store_id=0,
        language_id=1,
        firstname="Test",
        lastname="Customer",
        email="test@example.com",
        telephone="1234567890",
        password=get_password_hash("password123"),
        newsletter=0,
        ip="127.0.0.1",
        status=1,
        approved=1,
        safe=0,
        token="",
        date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@pytest.fixture
def test_customer_token(test_customer: Customer) -> str:
    """
    Create JWT token for test customer.
    """
    return create_access_token({"sub": str(test_customer.customer_id)})


@pytest.fixture
def auth_headers(test_customer_token: str) -> dict:
    """
    Create authorization headers with bearer token.
    """
    return {"Authorization": f"Bearer {test_customer_token}"}


@pytest.fixture
def test_category(db: Session) -> Category:
    """
    Create a test category.
    """
    category = Category(
        image="",
        parent_id=0,
        top=1,
        column_count=1,
        sort_order=0,
        status=1,
        date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        date_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    # Add description
    category_desc = CategoryDescription(
        category_id=category.category_id,
        language_id=1,
        name="Test Category",
        description="Test category description",
        meta_title="Test Category",
        meta_description="",
        meta_keyword=""
    )
    db.add(category_desc)
    db.commit()
    
    return category


@pytest.fixture
def test_product(db: Session, test_category: Category) -> Product:
    """
    Create a test product.
    """
    product = Product(
        model="TEST-001",
        sku="SKU-001",
        quantity=100,
        stock_status_id=7,
        image="catalog/test.jpg",
        manufacturer_id=0,
        shipping=1,
        price=29.99,
        points=0,
        tax_class_id=0,
        weight=1.0,
        weight_class_id=1,
        length=0.0,
        width=0.0,
        height=0.0,
        length_class_id=1,
        subtract=1,
        minimum=1,
        sort_order=0,
        status=1,
        viewed=0,
        date_available=datetime.now().strftime("%Y-%m-%d"),
        date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        date_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Add description
    product_desc = ProductDescription(
        product_id=product.product_id,
        language_id=1,
        name="Test Product",
        description="This is a test product description",
        tag="test,product",
        meta_title="Test Product",
        meta_description="Test product meta",
        meta_keyword="test"
    )
    db.add(product_desc)
    
    # Link to category
    product_to_cat = ProductToCategory(
        product_id=product.product_id,
        category_id=test_category.category_id
    )
    db.add(product_to_cat)
    
    db.commit()
    db.refresh(product)
    
    return product


@pytest.fixture
def test_products(db: Session, test_category: Category) -> list[Product]:
    """
    Create multiple test products.
    """
    products = []
    for i in range(5):
        product = Product(
            model=f"TEST-{i+1:03d}",
            sku=f"SKU-{i+1:03d}",
            quantity=100 + i * 10,
            stock_status_id=7,
            image=f"catalog/test{i+1}.jpg",
            manufacturer_id=0,
            shipping=1,
            price=19.99 + i * 10,
            points=0,
            tax_class_id=0,
            weight=1.0,
            weight_class_id=1,
            subtract=1,
            minimum=1,
            sort_order=i,
            status=1,
            viewed=0,
            date_available=datetime.now().strftime("%Y-%m-%d"),
            date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            date_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(product)
        db.flush()
        
        # Add description
        product_desc = ProductDescription(
            product_id=product.product_id,
            language_id=1,
            name=f"Test Product {i+1}",
            description=f"Description for test product {i+1}",
            tag="test",
            meta_title=f"Test Product {i+1}",
            meta_description="",
            meta_keyword="test"
        )
        db.add(product_desc)
        
        # Link to category
        product_to_cat = ProductToCategory(
            product_id=product.product_id,
            category_id=test_category.category_id
        )
        db.add(product_to_cat)
        
        products.append(product)
    
    db.commit()
    return products
