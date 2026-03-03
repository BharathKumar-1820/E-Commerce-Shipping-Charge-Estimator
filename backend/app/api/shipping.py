"""API endpoints - Shipping charge operations"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import (
    Warehouse, Seller, Customer, Product, ShippingLog
)
from app.schemas import (
    ShippingChargeResponseSchema,
    ShippingChargeCalculateRequestSchema,
    ShippingChargeCalculateResponseSchema,
    LocationSchema,
    ErrorResponseSchema,
)
from app.config import settings
from app.utils.distance import haversine_distance, get_nearest_warehouse
from app.utils.cache import cache_shipping_query
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["shipping"])


def calculate_shipping_charge(
    distance_km: float,
    weight_kg: float,
    delivery_speed: str
) -> tuple:
    """
    Calculate shipping charge based on distance, weight, and delivery speed
    
    Returns:
        Tuple of (shipping_charge, transport_mode)
    """
    
    # Determine transport mode based on distance
    if distance_km >= settings.AEROPLANE_MIN_DISTANCE:
        transport_mode = "aeroplane"
        rate = settings.AEROPLANE_RATE
    elif distance_km >= settings.TRUCK_MIN_DISTANCE:
        transport_mode = "truck"
        rate = settings.TRUCK_RATE
    else:
        transport_mode = "mini_van"
        rate = settings.MINI_VAN_RATE
    
    # Calculate base shipping charge
    charge = distance_km * weight_kg * rate
    
    # Add standard courier charge
    total_charge = charge + settings.STANDARD_COURIER_CHARGE
    
    # Add express surcharge if applicable
    if delivery_speed.lower() == "express":
        total_charge += weight_kg * settings.EXPRESS_EXTRA_CHARGE_PER_KG
    
    return total_charge, transport_mode


@router.get(
    "/shipping-charge",
    response_model=ShippingChargeResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema},
        404: {"model": ErrorResponseSchema},
    },
)
async def get_shipping_charge(
    warehouseId: int = Query(..., description="Warehouse ID"),
    customerId: int = Query(..., description="Customer ID"),
    deliverySpeed: str = Query("standard", description="Delivery speed: standard or express"),
    weight_kg: float = Query(5.0, description="Weight of product in kg", ge=0.1),
    db: Session = Depends(get_db)
):
    """
    Get shipping charge from warehouse to customer
    
    Given the warehouse ID and customer ID, return the shipping charge based on the distance and transport mode.
    
    - **warehouseId**: The ID of the warehouse
    - **customerId**: The ID of the customer
    - **deliverySpeed**: Delivery speed preference (standard or express)
    - **weight_kg**: Weight of the product in kilograms (default: 5.0 kg, minimum: 0.1 kg)
    
    Returns:
    - shippingCharge: Total shipping charge in Rs
    - distance_km: Distance between warehouse and customer
    - transport_mode: Mode of transport used
    """
    
    # Validate inputs
    if not warehouseId or not customerId:
        raise HTTPException(
            status_code=400,
            detail="warehouseId and customerId are required parameters"
        )
    
    # Validate delivery speed
    if deliverySpeed.lower() not in ["standard", "express"]:
        raise HTTPException(
            status_code=400,
            detail="deliverySpeed must be either 'standard' or 'express'"
        )
    
    # Fetch warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouseId).first()
    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail=f"Warehouse with ID {warehouseId} not found"
        )
    
    # Fetch customer
    customer = db.query(Customer).filter(Customer.id == customerId).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {customerId} not found"
        )
    
    # Calculate distance
    distance_km = haversine_distance(
        warehouse.location['lat'],
        warehouse.location['lng'],
        customer.location['lat'],
        customer.location['lng']
    )
    
    # Calculate shipping charge using provided weight
    shipping_charge, transport_mode = calculate_shipping_charge(
        distance_km,
        weight_kg,
        deliverySpeed
    )
    
    return ShippingChargeResponseSchema(
        shippingCharge=round(shipping_charge, 2),
        distance_km=round(distance_km, 2),
        transport_mode=transport_mode
    )


@router.post(
    "/shipping-charge/calculate",
    response_model=ShippingChargeCalculateResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema},
        404: {"model": ErrorResponseSchema},
    },
)
async def calculate_shipping_charge_endpoint(
    request: ShippingChargeCalculateRequestSchema,
    db: Session = Depends(get_db)
):
    """
    Calculate shipping charge for a seller and customer
    
    Given a seller and customer ID, calculate the shipping charges by combining 
    the nearest warehouse retrieval and shipping charge calculation.
    
    Request body:
    - sellerId: The ID of the seller
    - customerId: The ID of the customer
    - deliverySpeed: Delivery speed preference (standard or express)
    - productId: Optional - The ID of the product
    
    Returns:
    - shippingCharge: Total shipping charge in Rs
    - nearestWarehouse: Details of the nearest warehouse
    - distance_km: Distance between warehouse and customer
    - transport_mode: Mode of transport used
    - delivery_speed: The delivery speed used for calculation
    """
    
    # Validate inputs
    if not request.sellerId or not request.customerId:
        raise HTTPException(
            status_code=400,
            detail="sellerId and customerId are required"
        )
    
    # Validate delivery speed
    if request.deliverySpeed.lower() not in ["standard", "express"]:
        raise HTTPException(
            status_code=400,
            detail="deliverySpeed must be either 'standard' or 'express'"
        )
    
    # Fetch seller
    seller = db.query(Seller).filter(Seller.id == request.sellerId).first()
    if not seller:
        raise HTTPException(
            status_code=404,
            detail=f"Seller with ID {request.sellerId} not found"
        )
    
    # Fetch customer
    customer = db.query(Customer).filter(Customer.id == request.customerId).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with ID {request.customerId} not found"
        )
    
    # Fetch all warehouses
    warehouses = db.query(Warehouse).all()
    if not warehouses:
        raise HTTPException(
            status_code=404,
            detail="No warehouses available in the system"
        )
    
    # Get nearest warehouse
    nearest_warehouse, warehouse_distance = get_nearest_warehouse(seller.location, warehouses)
    if not nearest_warehouse:
        raise HTTPException(
            status_code=404,
            detail="Could not calculate nearest warehouse"
        )
    
    # Calculate distance from warehouse to customer
    customer_distance_km = haversine_distance(
        nearest_warehouse.location['lat'],
        nearest_warehouse.location['lng'],
        customer.location['lat'],
        customer.location['lng']
    )
    
    # Get product weight if provided, otherwise use default
    product_weight = 5.0
    if request.productId:
        product = db.query(Product).filter(Product.id == request.productId).first()
        if product:
            product_weight = product.weight_kg
    
    # Calculate shipping charge
    shipping_charge, transport_mode = calculate_shipping_charge(
        customer_distance_km,
        product_weight,
        request.deliverySpeed
    )
    
    # Log the shipping calculation
    shipping_log = ShippingLog(
        seller_id=request.sellerId,
        customer_id=request.customerId,
        warehouse_id=nearest_warehouse.id,
        product_id=request.productId or 0,
        shipping_charge=shipping_charge,
        delivery_speed=request.deliverySpeed,
        distance_km=customer_distance_km,
        transport_mode=transport_mode
    )
    db.add(shipping_log)
    db.commit()
    
    return ShippingChargeCalculateResponseSchema(
        shippingCharge=round(shipping_charge, 2),
        nearestWarehouse={
            "warehouseId": nearest_warehouse.id,
            "warehouseLocation": LocationSchema(**nearest_warehouse.location)
        },
        distance_km=round(customer_distance_km, 2),
        transport_mode=transport_mode,
        delivery_speed=request.deliverySpeed
    )
