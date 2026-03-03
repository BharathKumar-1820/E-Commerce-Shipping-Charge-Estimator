import axios from 'axios'

// Use relative URLs to leverage Vite proxy configuration
// Or directly use backend URL if running in production
const API_BASE_URL = import.meta.env.PROD ? 'http://localhost:8000' : ''

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // Warehouse endpoints
  getNearestWarehouse: (sellerId, productId) =>
    api.get('/api/v1/warehouse/nearest', {
      params: { sellerId, productId },
    }),

  // Shipping charge endpoints
  getShippingCharge: (warehouseId, customerId, deliverySpeed = 'standard', weight_kg = 5.0) =>
    api.get('/api/v1/shipping-charge', {
      params: { warehouseId, customerId, deliverySpeed, weight_kg },
    }),

  calculateShippingCharge: (sellerId, customerId, deliverySpeed = 'standard', productId = null) =>
    api.post('/api/v1/shipping-charge/calculate', {
      sellerId,
      customerId,
      deliverySpeed,
      productId,
    }),

  // Health check
  healthCheck: () =>
    api.get('/health'),
}

export default api
