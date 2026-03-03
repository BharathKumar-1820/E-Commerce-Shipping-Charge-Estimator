import React, { useState } from 'react'
import { apiService } from '../services/api'
import '../styles/WarehouseSelector.css'

function WarehouseSelector() {
  const [formData, setFormData] = useState({
    sellerId: '1',
    productId: '1',
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await apiService.getNearestWarehouse(
        parseInt(formData.sellerId),
        parseInt(formData.productId)
      )

      setResult(response.data)
    } catch (err) {
      setError(
        err.response?.data?.error || 'Failed to find nearest warehouse. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="warehouse-container">
      <div className="warehouse-form-section">
        <h2>Find Nearest Warehouse</h2>
        <p className="section-subtitle">Enter seller and product details to find the nearest warehouse</p>

        <form onSubmit={handleSubmit} className="warehouse-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="sellerId">Seller ID</label>
              <input
                type="number"
                id="sellerId"
                name="sellerId"
                value={formData.sellerId}
                onChange={handleInputChange}
                placeholder="Enter Seller ID"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="productId">Product ID</label>
              <input
                type="number"
                id="productId"
                name="productId"
                value={formData.productId}
                onChange={handleInputChange}
                placeholder="Enter Product ID"
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Finding Warehouse...' : 'Find Nearest Warehouse'}
          </button>
        </form>
      </div>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <div>
            <strong>Error</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>✅ Nearest Warehouse Found</h3>
          <div className="warehouse-card">
            <div className="warehouse-header">
              <h4>Warehouse Details</h4>
              <span className="warehouse-badge">ID: {result.warehouseId}</span>
            </div>

            <div className="warehouse-body">
              <div className="location-item">
                <span className="location-label">📍 Latitude:</span>
                <span className="location-value">{result.warehouseLocation.lat.toFixed(6)}</span>
              </div>
              <div className="location-item">
                <span className="location-label">📍 Longitude:</span>
                <span className="location-value">{result.warehouseLocation.lng.toFixed(6)}</span>
              </div>
            </div>

            <div className="warehouse-footer">
              <p className="warehouse-description">
                This is the nearest warehouse where the seller can drop off the product.
              </p>
            </div>
          </div>

          <div className="info-box">
            <h4>ℹ️ Warehouse Information</h4>
            <ul>
              <li>Warehouses are distribution centers located across India</li>
              <li>Sellers drop products at the nearest warehouse</li>
              <li>Products are then shipped from the warehouse to customers</li>
              <li>Distance calculation uses coordinates (latitude, longitude)</li>
              <li>Transport mode selection depends on distance to customer</li>
            </ul>
          </div>
        </div>
      )}

      <div className="sample-data-info">
        <h4>📋 Sample Data Available</h4>
        <div className="data-table">
          <div className="table-section">
            <h5>Sellers</h5>
            <ul>
              <li>ID: 1 - Nestle Seller (Chennai)</li>
              <li>ID: 2 - Rice Seller (Mumbai)</li>
              <li>ID: 3 - Sugar Seller (Hubli)</li>
            </ul>
          </div>
          <div className="table-section">
            <h5>Products</h5>
            <ul>
              <li>ID: 1 - Maggie 500g Packet (0.5 kg)</li>
              <li>ID: 2 - Rice Bag 10Kg (10 kg)</li>
              <li>ID: 3 - Sugar Bag 25kg (25 kg)</li>
            </ul>
          </div>
          <div className="table-section">
            <h5>Warehouses</h5>
            <ul>
              <li>ID: 1 - BLR_Warehouse (Bangalore)</li>
              <li>ID: 2 - MUMB_Warehouse (Mumbai)</li>
              <li>ID: 3 - DELHI_Warehouse (Delhi)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WarehouseSelector
