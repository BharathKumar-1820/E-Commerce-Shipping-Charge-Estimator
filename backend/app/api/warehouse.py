"""API endpoints - Warehouse operations"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Warehouse, Seller, Customer, Product
from app.schemas import WarehouseResponseSchema, LocationSchema, ErrorResponseSchema
from app.utils.distance import get_nearest_warehouse
from app.utils.cache import cache_warehouse_query

router = APIRouter(prefix="/api/v1/warehouse", tags=["warehouse"])


@router.get(
    "/nearest",
    response_model=WarehouseResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema},
        404: {"model": ErrorResponseSchema},
    },
)
async def get_nearest_warehouse_endpoint(
    sellerId: int = Query(..., description="Seller ID"),
    productId: int = Query(..., description="Product ID"),
    db: Session = Depends(get_db)
):
    """
    Get the nearest warehouse for a seller
    
    Given a seller and product, return the nearest warehouse where the seller can drop off the product.
    
    - **sellerId**: The ID of the seller
    - **productId**: The ID of the product
    
    Returns:
    - warehouseId: ID of the nearest warehouse
    - warehouseLocation: Location coordinates of the warehouse
    """
    
    # Validate inputs
    if not sellerId or not productId:
        raise HTTPException(
            status_code=400,
            detail="sellerId and productId are required parameters"
        )
    
    # Fetch seller details
    seller = db.query(Seller).filter(Seller.id == sellerId).first()
    if not seller:
        raise HTTPException(
            status_code=404,
            detail=f"Seller with ID {sellerId} not found"
        )
    
    # Fetch product details
    product = db.query(Product).filter(Product.id == productId).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {productId} not found"
        )
    
    # Fetch all warehouses
    warehouses = db.query(Warehouse).all()
    if not warehouses:
        raise HTTPException(
            status_code=404,
            detail="No warehouses available in the system"
        )
    
    # Get nearest warehouse
    nearest_warehouse, distance = get_nearest_warehouse(seller.location, warehouses)
    
    if not nearest_warehouse:
        raise HTTPException(
            status_code=404,
            detail="Could not calculate nearest warehouse"
        )
    
    return WarehouseResponseSchema(
        warehouseId=nearest_warehouse.id,
        warehouseLocation=LocationSchema(**nearest_warehouse.location)
    )
