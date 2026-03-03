"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from datetime import datetime


class LocationSchema(BaseModel):
    """Schema for location coordinates"""
    lat: float = Field(..., description="Latitude coordinate")
    lng: float = Field(..., description="Longitude coordinate")


class CustomerSchema(BaseModel):
    """Schema for Customer"""
    id: int
    name: str
    phone_number: str
    location: LocationSchema
    created_at: datetime


class CustomerCreateSchema(BaseModel):
    """Schema for creating a Customer"""
    name: str
    phone_number: str
    location: LocationSchema


class SellerSchema(BaseModel):
    """Schema for Seller"""
    id: int
    name: str
    location: LocationSchema
    created_at: datetime


class SellerCreateSchema(BaseModel):
    """Schema for creating a Seller"""
    name: str
    location: LocationSchema


class ProductSchema(BaseModel):
    """Schema for Product"""
    id: int
    name: str
    seller_id: int
    price: float
    weight_kg: float
    dimensions: str
    created_at: datetime


class ProductCreateSchema(BaseModel):
    """Schema for creating a Product"""
    name: str
    seller_id: int
    price: float
    weight_kg: float
    dimensions: str


class WarehouseSchema(BaseModel):
    """Schema for Warehouse"""
    id: int
    name: str
    location: LocationSchema
    created_at: datetime


class WarehouseCreateSchema(BaseModel):
    """Schema for creating a Warehouse"""
    name: str
    location: LocationSchema


class WarehouseResponseSchema(BaseModel):
    """Response schema for nearest warehouse"""
    warehouseId: int
    warehouseLocation: LocationSchema


class ShippingChargeResponseSchema(BaseModel):
    """Response schema for shipping charge"""
    shippingCharge: float = Field(..., description="Total shipping charge in Rs")
    distance_km: Optional[float] = Field(None, description="Distance in kilometers")
    transport_mode: Optional[str] = Field(None, description="Mode of transport used")


class ShippingChargeCalculateRequestSchema(BaseModel):
    """Request schema for calculating shipping charge"""
    sellerId: int = Field(..., description="Seller ID", gt=0)
    customerId: int = Field(..., description="Customer ID", gt=0)
    deliverySpeed: str = Field("standard", description="Delivery speed: standard or express")
    productId: Optional[int] = Field(None, description="Product ID", gt=0)
    
    @field_validator('deliverySpeed')
    @classmethod
    def validate_delivery_speed(cls, v):
        if v.lower() not in ['standard', 'express']:
            raise ValueError('Delivery speed must be either standard or express')
        return v.lower()


class ShippingChargeCalculateResponseSchema(BaseModel):
    """Response schema for shipping charge calculation"""
    shippingCharge: float = Field(..., description="Total shipping charge in Rs")
    nearestWarehouse: WarehouseResponseSchema
    distance_km: Optional[float] = Field(None, description="Distance in kilometers")
    transport_mode: Optional[str] = Field(None, description="Mode of transport used")
    delivery_speed: Optional[str] = Field(None, description="Delivery speed used")


class ErrorResponseSchema(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
