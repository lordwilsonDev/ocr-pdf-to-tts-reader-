import React, { createContext, useContext, useState, useEffect } from 'react';

const SwrContext = createContext({});

export function SwrProvider({ children }) {
  const [documentId, setDocumentId] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, uploading, processing, ready, completed
  const [extractedData, setExtractedData] = useState([]);
  
  // Simulated Polling or Websocket connection
  useEffect(() => {
    let interval;
    if (status === 'processing') {
      interval = setInterval(async () => {
        try {
          const res = await fetch('http://localhost:8000/status');
          const data = await res.json();
          if (data.status === 'idle' && documentId) {
            setStatus('ready');
          }
        } catch (err) {
          console.error("Failed to fetch status", err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [status, documentId]);

  return (
    <SwrContext.Provider value={{
      documentId, setDocumentId,
      status, setStatus,
      extractedData, setExtractedData
    }}>
      {children}
    </SwrContext.Provider>
  );
}

export const useSwr = () => useContext(SwrContext);
