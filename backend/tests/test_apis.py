"""
Unit tests for the Shipping Charge Estimator API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Customer, Seller, Product, Warehouse


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_test_data():
    """Setup test data before each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Add test warehouses
    warehouses = [
        Warehouse(
            name="TEST_WH_1",
            location={"lat": 12.99999, "lng": 37.923273}
        ),
        Warehouse(
            name="TEST_WH_2",
            location={"lat": 11.99999, "lng": 27.923273}
        ),
    ]
    db.add_all(warehouses)
    
    # Add test customers
    customers = [
        Customer(
            name="Test Store 1",
            phone_number="9876543210",
            location={"lat": 11.232, "lng": 23.445495}
        ),
        Customer(
            name="Test Store 2",
            phone_number="9999999999",
            location={"lat": 17.232, "lng": 33.445495}
        ),
    ]
    db.add_all(customers)
    
    # Add test sellers
    sellers = [
        Seller(
            name="Test Seller 1",
            location={"lat": 13.0827, "lng": 80.2707}
        ),
        Seller(
            name="Test Seller 2",
            location={"lat": 19.0760, "lng": 72.8777}
        ),
    ]
    db.add_all(sellers)
    
    # Add test products
    products = [
        Product(
            name="Test Product 1",
            seller_id=1,
            price=100.0,
            weight_kg=5.0,
            dimensions="10cmx10cmx10cm"
        ),
        Product(
            name="Test Product 2",
            seller_id=2,
            price=500.0,
            weight_kg=10.0,
            dimensions="20cmx20cmx20cm"
        ),
    ]
    db.add_all(products)
    
    db.commit()
    yield db
    db.close()


class TestHealthCheck:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestNearestWarehouse:
    """Tests for nearest warehouse endpoint"""
    
    def test_nearest_warehouse_success(self, setup_test_data):
        """Test successful nearest warehouse retrieval"""
        response = client.get("/api/v1/warehouse/nearest?sellerId=1&productId=1")
        assert response.status_code == 200
        data = response.json()
        assert "warehouseId" in data
        assert "warehouseLocation" in data
        assert "lat" in data["warehouseLocation"]
        assert "lng" in data["warehouseLocation"]
    
    def test_nearest_warehouse_missing_params(self, setup_test_data):
        """Test nearest warehouse with missing parameters"""
        response = client.get("/api/v1/warehouse/nearest?sellerId=1")
        assert response.status_code == 400
        assert "error" in response.json()
    
    def test_nearest_warehouse_invalid_seller(self, setup_test_data):
        """Test nearest warehouse with invalid seller ID"""
        response = client.get("/api/v1/warehouse/nearest?sellerId=999&productId=1")
        assert response.status_code == 404
        assert "error" in response.json()
    
    def test_nearest_warehouse_invalid_product(self, setup_test_data):
        """Test nearest warehouse with invalid product ID"""
        response = client.get("/api/v1/warehouse/nearest?sellerId=1&productId=999")
        assert response.status_code == 404
        assert "error" in response.json()


class TestShippingCharge:
    """Tests for shipping charge endpoint"""
    
    def test_shipping_charge_standard(self, setup_test_data):
        """Test shipping charge calculation with standard delivery"""
        response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=standard"
        )
        assert response.status_code == 200
        data = response.json()
        assert "shippingCharge" in data
        assert data["shippingCharge"] > 0
        assert "distance_km" in data
        assert "transport_mode" in data
    
    def test_shipping_charge_express(self, setup_test_data):
        """Test shipping charge calculation with express delivery"""
        response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=express"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["shippingCharge"] > 0
    
    def test_shipping_charge_invalid_speed(self, setup_test_data):
        """Test shipping charge with invalid delivery speed"""
        response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=invalid"
        )
        assert response.status_code == 400
        assert "error" in response.json()
    
    def test_shipping_charge_missing_params(self, setup_test_data):
        """Test shipping charge with missing parameters"""
        response = client.get("/api/v1/shipping-charge?warehouseId=1")
        assert response.status_code == 400
    
    def test_shipping_charge_invalid_warehouse(self, setup_test_data):
        """Test shipping charge with invalid warehouse ID"""
        response = client.get(
            "/api/v1/shipping-charge?warehouseId=999&customerId=1&deliverySpeed=standard"
        )
        assert response.status_code == 404


class TestCalculateShipping:
    """Tests for shipping charge calculation endpoint"""
    
    def test_calculate_shipping_success(self, setup_test_data):
        """Test successful shipping charge calculation"""
        payload = {
            "sellerId": 1,
            "customerId": 1,
            "deliverySpeed": "standard"
        }
        response = client.post("/api/v1/shipping-charge/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "shippingCharge" in data
        assert "nearestWarehouse" in data
        assert data["nearestWarehouse"]["warehouseId"] > 0
    
    def test_calculate_shipping_with_product(self, setup_test_data):
        """Test shipping charge calculation with product ID"""
        payload = {
            "sellerId": 1,
            "customerId": 1,
            "deliverySpeed": "express",
            "productId": 1
        }
        response = client.post("/api/v1/shipping-charge/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "shippingCharge" in data
    
    def test_calculate_shipping_invalid_seller(self, setup_test_data):
        """Test calculation with invalid seller"""
        payload = {
            "sellerId": 999,
            "customerId": 1,
            "deliverySpeed": "standard"
        }
        response = client.post("/api/v1/shipping-charge/calculate", json=payload)
        assert response.status_code == 404
    
    def test_calculate_shipping_invalid_speed(self, setup_test_data):
        """Test calculation with invalid delivery speed"""
        payload = {
            "sellerId": 1,
            "customerId": 1,
            "deliverySpeed": "invalid"
        }
        response = client.post("/api/v1/shipping-charge/calculate", json=payload)
        assert response.status_code == 400


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_shipping_charge_comparison(self, setup_test_data):
        """Test that express is more expensive than standard"""
        standard_response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=standard"
        )
        express_response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=express"
        )
        
        standard_charge = standard_response.json()["shippingCharge"]
        express_charge = express_response.json()["shippingCharge"]
        
        assert express_charge > standard_charge
    
    def test_transport_mode_selection(self, setup_test_data):
        """Test that correct transport mode is selected based on distance"""
        response = client.get(
            "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=standard"
        )
        data = response.json()
        assert data["transport_mode"] in ["aeroplane", "truck", "mini_van"]
