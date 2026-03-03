"""
Database initialization and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models import Base


# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables
    """
    Base.metadata.create_all(bind=engine)


def seed_sample_data():
    """
    Seed the database with sample data for testing and demonstration
    """
    db = SessionLocal()
    
    try:
        # Check if data already exists
        from app.models import Customer, Seller, Product, Warehouse
        
        if db.query(Warehouse).first() is None:
            # Add sample warehouses
            warehouses = [
                Warehouse(
                    name="BLR_Warehouse",
                    location={"lat": 12.99999, "lng": 37.923273}
                ),
                Warehouse(
                    name="MUMB_Warehouse",
                    location={"lat": 11.99999, "lng": 27.923273}
                ),
                Warehouse(
                    name="DELHI_Warehouse",
                    location={"lat": 28.70406, "lng": 77.102496}
                ),
            ]
            db.add_all(warehouses)
            
        if db.query(Customer).first() is None:
            # Add sample customers
            customers = [
                Customer(
                    name="Shree Kirana Store",
                    phone_number="9847123456",
                    location={"lat": 11.232, "lng": 23.445495}
                ),
                Customer(
                    name="Andheri Mini Mart",
                    phone_number="9101456789",
                    location={"lat": 17.232, "lng": 33.445495}
                ),
                Customer(
                    name="Delhi General Store",
                    phone_number="9876543210",
                    location={"lat": 28.7041, "lng": 77.1025}
                ),
            ]
            db.add_all(customers)
            
        if db.query(Seller).first() is None:
            # Add sample sellers
            sellers = [
                Seller(
                    name="Nestle Seller",
                    location={"lat": 13.0827, "lng": 80.2707}  # Chennai
                ),
                Seller(
                    name="Rice Seller",
                    location={"lat": 19.0760, "lng": 72.8777}  # Mumbai
                ),
                Seller(
                    name="Sugar Seller",
                    location={"lat": 15.2993, "lng": 75.8243}  # Hubli
                ),
            ]
            db.add_all(sellers)
            
        if db.query(Product).first() is None:
            # Add sample products
            products = [
                Product(
                    name="Maggie 500g Packet",
                    seller_id=1,
                    price=10.0,
                    weight_kg=0.5,
                    dimensions="10cmx10cmx10cm"
                ),
                Product(
                    name="Rice Bag 10Kg",
                    seller_id=2,
                    price=500.0,
                    weight_kg=10.0,
                    dimensions="1000cmx800cmx500cm"
                ),
                Product(
                    name="Sugar Bag 25kg",
                    seller_id=3,
                    price=700.0,
                    weight_kg=25.0,
                    dimensions="1000cmx900cmx600cm"
                ),
            ]
            db.add_all(products)
            
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()
