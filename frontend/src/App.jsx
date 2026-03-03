import React, { useState } from 'react'
import './App.css'
import ShippingCalculator from './components/ShippingCalculator'
import WarehouseSelector from './components/WarehouseSelector'

function App() {
  const [activeTab, setActiveTab] = useState('shipping')

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>📦 Shipping Charge Estimator</h1>
          <p>B2B E-Commerce Marketplace Solution</p>
        </div>
      </header>

      <main className="app-main">
        <div className="tabs-container">
          <div className="tabs">
            <button
              className={`tab-button ${activeTab === 'shipping' ? 'active' : ''}`}
              onClick={() => setActiveTab('shipping')}
            >
              Calculate Shipping
            </button>
            <button
              className={`tab-button ${activeTab === 'warehouse' ? 'active' : ''}`}
              onClick={() => setActiveTab('warehouse')}
            >
              Find Warehouse
            </button>
          </div>
        </div>

        <div className="content-container">
          {activeTab === 'shipping' && <ShippingCalculator />}
          {activeTab === 'warehouse' && <WarehouseSelector />}
        </div>
      </main>

      <footer className="app-footer">
        <p>© 2024 E-Commerce Shipping Charge Estimator. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
