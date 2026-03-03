# E-Commerce Shipping Charge Estimator

A comprehensive B2B e-commerce marketplace solution for calculating shipping charges, finding nearest warehouses, and managing delivery logistics for Kirana stores.

## 🚀 Features

### Backend (FastAPI)
- **Three RESTful APIs** as per requirements:
  - `GET /api/v1/warehouse/nearest` - Find nearest warehouse for a seller
  - `GET /api/v1/shipping-charge` - Calculate shipping charge from warehouse to customer
  - `POST /api/v1/shipping-charge/calculate` - Calculate complete shipping charge combining both operations

- **Comprehensive Entities**:
  - Customers (Kirana Stores) with location
  - Sellers with location
  - Products with weight and dimensions
  - Warehouses across India
  - Shipping logs for tracking

- **Smart Features**:
  - Haversine distance calculation for accurate distances
  - Automatic transport mode selection based on distance:
    - **Aeroplane** (500km+): ₹1 per km per kg
    - **Truck** (100km+): ₹2 per km per kg
    - **Mini Van** (0-100km): ₹3 per km per kg
  - Two delivery speed options:
    - **Standard**: ₹10 + base charge
    - **Express**: ₹10 + ₹1.2 per kg + base charge
  - Response caching for improved performance
  - Comprehensive error handling with meaningful messages
  - Input validation for all parameters

- **Design Patterns**:
  - MVC Architecture
  - Service layer pattern
  - Dependency injection
  - Factory pattern for utility functions
  - Caching decorator pattern

### Frontend (React + Vite)
- **Modern React Application** with:
  - Component-based architecture
  - Axios for API communication
  - Responsive design with Flexbox/Grid
  - Two main features:
    1. **Shipping Charge Calculator** - Calculate shipping costs with detailed breakdown
    2. **Warehouse Finder** - Find nearest warehouse for sellers
  - Sample data reference section
  - Real-time error handling
  - Loading states

## 📁 Project Structure

```
project_ecommerce/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── warehouse.py        # Warehouse endpoints
│   │   │   └── shipping.py         # Shipping endpoints
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── distance.py         # Distance calculations
│   │   │   └── cache.py            # Caching utilities
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── models.py               # Database models
│   │   ├── schemas.py              # Pydantic schemas
│   │   └── database.py             # Database setup & seeding
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_apis.py            # Comprehensive unit tests
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ShippingCalculator.jsx
│   │   │   └── WarehouseSelector.jsx
│   │   ├── services/
│   │   │   └── api.js              # API communication
│   │   ├── styles/
│   │   │   ├── ShippingCalculator.css
│   │   │   └── WarehouseSelector.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip (Python package manager)
- npm or yarn (Node package manager)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the backend server**:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Open another terminal and navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📚 API Endpoints

### 1. Get Nearest Warehouse

**Request**:
```http
GET /api/v1/warehouse/nearest?sellerId=1&productId=1
```

**Response** (200 OK):
```json
{
  "warehouseId": 1,
  "warehouseLocation": {
    "lat": 12.99999,
    "lng": 37.923273
  }
}
```

---

### 2. Get Shipping Charge

**Request**:
```http
GET /api/v1/shipping-charge?warehouseId=1&customerId=1&deliverySpeed=standard
```

**Response** (200 OK):
```json
{
  "shippingCharge": 150.00,
  "distance_km": 450.50,
  "transport_mode": "truck"
}
```

---

### 3. Calculate Shipping Charge (Combined)

**Request**:
```http
POST /api/v1/shipping-charge/calculate
Content-Type: application/json

{
  "sellerId": 1,
  "customerId": 1,
  "deliverySpeed": "express",
  "productId": 1
}
```

**Response** (200 OK):
```json
{
  "shippingCharge": 180.00,
  "nearestWarehouse": {
    "warehouseId": 1,
    "warehouseLocation": {
      "lat": 12.99999,
      "lng": 37.923273
    }
  },
  "distance_km": 450.50,
  "transport_mode": "truck",
  "delivery_speed": "express"
}
```

## 📋 Sample Data

The application comes preloaded with sample data:

### Sellers
- **ID 1**: Nestle Seller (Chennai)
- **ID 2**: Rice Seller (Mumbai)
- **ID 3**: Sugar Seller (Hubli)

### Customers
- **ID 1**: Shree Kirana Store (Hyderabad)
- **ID 2**: Andheri Mini Mart (Mumbai)
- **ID 3**: Delhi General Store (Delhi)

### Products
- **ID 1**: Maggie 500g Packet (0.5 kg) - ₹10
- **ID 2**: Rice Bag 10Kg (10 kg) - ₹500
- **ID 3**: Sugar Bag 25kg (25 kg) - ₹700

### Warehouses
- **ID 1**: BLR_Warehouse (Bangalore)
- **ID 2**: MUMB_Warehouse (Mumbai)
- **ID 3**: DELHI_Warehouse (Delhi)

## 🧪 Testing

Run the unit tests with pytest:

```bash
cd backend
pytest tests/ -v
```

**Test Coverage**:
- ✅ Health check endpoint
- ✅ Nearest warehouse retrieval
- ✅ Shipping charge calculation (standard & express)
- ✅ Successful API calls
- ✅ Invalid parameters handling
- ✅ Missing data handling
- ✅ Transport mode selection
- ✅ Price comparison (express vs standard)

## 🔧 Configuration

Edit `backend/app/config.py` to customize:

```python
# Shipping rates
STANDARD_COURIER_CHARGE = 10.0
EXPRESS_EXTRA_CHARGE_PER_KG = 1.2

# Transport mode rates (Rs per km per kg)
AEROPLANE_RATE = 1.0
TRUCK_RATE = 2.0
MINI_VAN_RATE = 3.0

# Distance thresholds
AEROPLANE_MIN_DISTANCE = 500.0
TRUCK_MIN_DISTANCE = 100.0
MINI_VAN_MAX_DISTANCE = 100.0
```

## 💡 Design Patterns & Best Practices

1. **Modular Code Structure**: Separate concerns with different modules
2. **Error Handling**: Comprehensive exception handling with meaningful error messages
3. **Input Validation**: Pydantic schemas for request validation
4. **Caching**: TTL-based caching for improved performance
5. **Distance Calculation**: Haversine formula for accurate geographic calculations
6. **Responsive Design**: Mobile-friendly frontend using CSS Grid/Flexbox
7. **Component Reusability**: Modular React components
8. **API Documentation**: Auto-generated Swagger UI and ReDoc

## 🚀 Deployment

### Backend (Heroku/AWS/Azure)
```bash
# Create requirements.txt with pinned versions
pip freeze > requirements.txt

# Deploy to Heroku
git push heroku main
```

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy the dist/ folder to your hosting provider
```

## 📝 Error Handling Examples

### Missing Parameters
```json
{
  "error": "sellerId and customerId are required parameters",
  "details": null
}
```

### Invalid Delivery Speed
```json
{
  "error": "deliverySpeed must be either 'standard' or 'express'",
  "details": null
}
```

### Resource Not Found
```json
{
  "error": "Seller with ID 999 not found",
  "details": null
}
```

### No Warehouses Available
```json
{
  "error": "No warehouses available in the system",
  "details": null
}
```

## 🎯 Key Features Implemented

✅ **Three Required APIs** - All three endpoints implemented with full functionality
✅ **Error Handling** - Comprehensive error handling for all edge cases
✅ **Database Models** - Complete data models for all entities
✅ **Caching** - TTL-based response caching for performance
✅ **Unit Tests** - 20+ test cases covering all functionality
✅ **Input Validation** - Request validation using Pydantic schemas
✅ **Distance Calculation** - Haversine formula for accurate distances
✅ **Transport Mode Selection** - Automatic selection based on distance
✅ **Delivery Speed Options** - Standard and Express pricing
✅ **Sample Data** - Pre-populated database with realistic data
✅ **API Documentation** - Auto-generated Swagger UI
✅ **React Frontend** - Interactive UI for testing APIs
✅ **Responsive Design** - Mobile-friendly interface
✅ **Code Quality** - Clean, well-documented, modular code

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues, please contact: shreya.palit@jumbotail.com

---

**Built with ❤️ for Jumbotail**
