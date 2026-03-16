import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { SwrProvider } from './context/SwrContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SwrProvider>
      <App />
    </SwrProvider>
  </StrictMode>,
)
