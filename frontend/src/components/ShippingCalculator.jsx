import React, { useState } from 'react'
import { apiService } from '../services/api'
import '../styles/ShippingCalculator.css'

function ShippingCalculator() {
  const [formData, setFormData] = useState({
    sellerId: '1',
    customerId: '1',
    deliverySpeed: 'standard',
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
      const response = await apiService.calculateShippingCharge(
        parseInt(formData.sellerId),
        parseInt(formData.customerId),
        formData.deliverySpeed,
        formData.productId ? parseInt(formData.productId) : null
      )

      setResult(response.data)
    } catch (err) {
      setError(
        err.response?.data?.error || 'Failed to calculate shipping charge. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="calculator-container">
      <div className="calculator-form-section">
        <h2>Calculate Shipping Charge</h2>
        <p className="section-subtitle">Enter seller and customer details to calculate the shipping charge</p>

        <form onSubmit={handleSubmit} className="calculator-form">
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
              <label htmlFor="customerId">Customer ID</label>
              <input
                type="number"
                id="customerId"
                name="customerId"
                value={formData.customerId}
                onChange={handleInputChange}
                placeholder="Enter Customer ID"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="deliverySpeed">Delivery Speed</label>
              <select
                id="deliverySpeed"
                name="deliverySpeed"
                value={formData.deliverySpeed}
                onChange={handleInputChange}
              >
                <option value="standard">Standard (Rs 10 + base charge)</option>
                <option value="express">Express (Rs 10 + Rs 1.2/kg + base charge)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="productId">Product ID (Optional)</label>
              <input
                type="number"
                id="productId"
                name="productId"
                value={formData.productId}
                onChange={handleInputChange}
                placeholder="Enter Product ID"
              />
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Calculating...' : 'Calculate Shipping Charge'}
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
          <h3>📊 Shipping Charge Result</h3>
          <div className="result-grid">
            <div className="result-card highlight">
              <div className="result-label">Total Shipping Charge</div>
              <div className="result-value">₹ {result.shippingCharge.toFixed(2)}</div>
            </div>

            <div className="result-card">
              <div className="result-label">Distance</div>
              <div className="result-value">{result.distance_km} km</div>
            </div>

            <div className="result-card">
              <div className="result-label">Transport Mode</div>
              <div className="result-value">{result.transport_mode}</div>
            </div>

            <div className="result-card">
              <div className="result-label">Delivery Speed</div>
              <div className="result-value">{result.delivery_speed}</div>
            </div>
          </div>

          <div className="warehouse-info">
            <h4>📍 Nearest Warehouse</h4>
            <div className="warehouse-details">
              <p><strong>Warehouse ID:</strong> {result.nearestWarehouse.warehouseId}</p>
              <p>
                <strong>Location:</strong> Lat {result.nearestWarehouse.warehouseLocation.lat.toFixed(4)}, 
                Lng {result.nearestWarehouse.warehouseLocation.lng.toFixed(4)}
              </p>
            </div>
          </div>

          <div className="rate-info">
            <h4>💰 Rate Information</h4>
            <ul>
              <li><strong>Standard Courier Charge:</strong> Rs 10</li>
              <li><strong>Express Extra Charge:</strong> Rs 1.2 per kg (if applicable)</li>
              <li><strong>Transport Rates:</strong></li>
              <ul>
                <li>Aeroplane (500km+): Rs 1 per km per kg</li>
                <li>Truck (100km+): Rs 2 per km per kg</li>
                <li>Mini Van (0-100km): Rs 3 per km per kg</li>
              </ul>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default ShippingCalculator
