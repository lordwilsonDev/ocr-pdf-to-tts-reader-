import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, File as FileIcon, Loader2, CheckCircle2 } from 'lucide-react';
import { useSwr } from '../context/SwrContext';

export function UploadNode() {
  const { status, setStatus, setDocumentId } = useSwr();

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    setStatus('uploading');
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await resp.json();
      
      setDocumentId(data.id);
      
      // Trigger reading
      setStatus('processing');
      await fetch(`http://localhost:8000/read/${data.id}`);
      
    } catch (error) {
      console.error('Core ingestion failure:', error);
      setStatus('idle');
    }
  }, [setStatus, setDocumentId]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'text/plain': ['.txt'] },
    disabled: status !== 'idle'
  });

  return (
    <div className="glass-panel p-6 flex flex-col relative overflow-hidden">
      {/* Decorative Glow */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-swr-glow blur-[80px] rounded-full pointer-events-none" />
      
      <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <span className="text-swr-accent">01.</span> Precision Ingestion
      </h2>
      
      <div 
        {...getRootProps()} 
        className={`relative flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-8 transition-all duration-300
          ${isDragActive ? 'border-swr-accent bg-swr-accent/5' : 'border-swr-border/50 hover:border-swr-border hover:bg-white/5'}
          ${status !== 'idle' ? 'opacity-50 cursor-not-allowed pointer-events-none' : 'cursor-pointer'}
        `}
      >
        <input {...getInputProps()} />
        
        <AnimatePresence mode="wait">
          {status === 'idle' ? (
            <motion.div 
              key="idle"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center text-center"
            >
              <div className="w-16 h-16 rounded-full bg-swr-surface border border-swr-border flex items-center justify-center mb-4 shadow-xl shadow-swr-glow/10 text-swr-muted">
                <UploadCloud className="w-8 h-8" />
              </div>
              <p className="text-sm font-medium">Drag & Drop Intel Payload</p>
              <p className="text-xs text-swr-muted mt-2">Supports high-DPI PDF & TXT</p>
            </motion.div>
          ) : status === 'uploading' ? (
            <motion.div 
              key="uploading"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center text-center"
            >
              <Loader2 className="w-10 h-10 text-blue-500 animate-spin mb-3" />
              <p className="text-sm font-mono text-blue-400">Transmitting to core...</p>
            </motion.div>
          ) : status === 'processing' ? (
            <motion.div 
              key="processing"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center text-center"
            >
              <div className="relative mb-3">
                <FileIcon className="w-10 h-10 text-yellow-500" />
                <div className="absolute inset-0 bg-yellow-500 blur-xl opacity-30 animate-pulse"></div>
              </div>
              <p className="text-sm font-mono text-yellow-400">Extracting intelligence...</p>
            </motion.div>
          ) : (
             <motion.div 
              key="ready"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center text-center"
            >
              <CheckCircle2 className="w-10 h-10 text-green-500 mb-3" />
              <p className="text-sm font-mono text-green-400">Document Assimilated</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
