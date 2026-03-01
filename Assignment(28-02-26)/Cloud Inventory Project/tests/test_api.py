import pytest
from src.app import create_app
from src.models.mysql_models import db

@pytest.fixture
def app():
    # Setup test app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for tests to bypass MySQL container
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_register_mysql(client):
    response = client.post('/api/auth/register', json={
        "db_choice": "mysql",
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123"
    })
    
    # We expect 201 during mock integration testing
    assert response.status_code == 201
    assert response.json['message'] == 'Registration successful'

def test_create_product(client):
    response = client.post('/api/products/', json={
        "name": "Test Product",
        "price": 99.99,
        "description": "A test product",
        "quantity": 10
    })
    
    assert response.status_code == 201
    assert 'product' in response.json

def test_get_products(client):
    client.post('/api/products/', json={
        "name": "Test Product 2",
        "price": 19.99,
        "quantity": 5
    })
    
    response = client.get('/api/products/')
    assert response.status_code == 200
    assert len(response.json['products']) > 0
