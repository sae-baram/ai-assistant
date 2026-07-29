import React from 'react'
import ReactDOM from 'react-dom/client'
import MinimalChat from './components/MinimalChat'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MinimalChat apiUrl={import.meta.env.VITE_API_URL || 'http://localhost:8000/ask'} />
  </React.StrictMode>
)
