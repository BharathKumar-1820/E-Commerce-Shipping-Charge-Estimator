"""
Database models for E-Commerce Shipping Charge Estimator
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    """
    Customer model representing Kirana stores
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    location = Column(JSON, nullable=False)  # {lat: float, lng: float}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name})>"


class Seller(Base):
    """
    Seller model representing sellers in the marketplace
    """
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(JSON, nullable=False)  # {lat: float, lng: float}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Seller(id={self.id}, name={self.name})>"


class Product(Base):
    """
    Product model with attributes like weight and dimensions
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    seller_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    dimensions = Column(String(255), nullable=False)  # e.g., "10cmx10cmx10cm"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"


class Warehouse(Base):
    """
    Warehouse model for marketplace distribution centers
    """
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    location = Column(JSON, nullable=False)  # {lat: float, lng: float}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Warehouse(id={self.id}, name={self.name})>"


class ShippingLog(Base):
    """
    Shipping log model for tracking shipping charges
    """
    __tablename__ = "shipping_logs"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    shipping_charge = Column(Float, nullable=False)
    delivery_speed = Column(String(50), nullable=False)
    distance_km = Column(Float, nullable=False)
    transport_mode = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ShippingLog(id={self.id}, shipping_charge={self.shipping_charge})>"
