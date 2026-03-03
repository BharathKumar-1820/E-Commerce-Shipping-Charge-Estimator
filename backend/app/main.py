"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db, seed_sample_data
from app.api import warehouse, shipping

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="E-Commerce Shipping Charge Estimator API for B2B marketplace",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with custom response"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "details": None
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle generic exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc) if settings.debug else None
        },
    )


# Initialize database and seed data on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    seed_sample_data()
    print("✓ Database initialized")
    print("✓ Sample data seeded")


# Include routers
app.include_router(warehouse.router)
app.include_router(shipping.router)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API documentation"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "nearest_warehouse": "/api/v1/warehouse/nearest?sellerId=1&productId=1",
            "shipping_charge": "/api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=standard",
            "calculate_shipping": "/api/v1/shipping-charge/calculate"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
