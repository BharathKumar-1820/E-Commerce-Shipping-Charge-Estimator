"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "E-Commerce Shipping Charge Estimator"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./shipping_estimator.db"
    
    # Shipping rates
    STANDARD_COURIER_CHARGE: float = 10.0
    EXPRESS_EXTRA_CHARGE_PER_KG: float = 1.2
    
    # Transport modes
    AEROPLANE_RATE: float = 1.0  # Rs per km per kg
    TRUCK_RATE: float = 2.0  # Rs per km per kg
    MINI_VAN_RATE: float = 3.0  # Rs per km per kg
    
    # Distance thresholds (in km)
    AEROPLANE_MIN_DISTANCE: float = 500.0
    TRUCK_MIN_DISTANCE: float = 100.0
    MINI_VAN_MAX_DISTANCE: float = 100.0
    
    class Config:
        env_file = ".env"


settings = Settings()
