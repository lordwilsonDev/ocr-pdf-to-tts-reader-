import React from 'react';
import { useSwr } from './context/SwrContext';
import { UploadNode } from './components/UploadNode';
import { CognitiveTerminal } from './components/CognitiveTerminal';
import { RAGQueryInterface } from './components/RAGQueryInterface';
import { CircuitBoard } from 'lucide-react';

function App() {
  const { status } = useSwr();

  return (
    <div className="min-h-screen text-swr-text relative overflow-x-hidden">
      
      {/* HUD Header */}
      <header className="p-6 flex items-center justify-between border-b border-swr-border bg-swr-surface/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-swr-glow rounded-lg relative overflow-hidden">
            <CircuitBoard className="w-6 h-6 text-swr-accent animate-pulse-slow relative z-10" />
            <div className="absolute inset-0 bg-swr-accent/20 blur-xl"></div>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">Sovereign Whisper</h1>
            <p className="text-xs text-swr-accent font-mono">Phase 5: HUD Orchestrator</p>
          </div>
        </div>
        <div className="flex items-center gap-2 font-mono text-sm">
          <span className="text-swr-muted">Global State:</span>
          <span className={`px-2 py-1 rounded-md bg-opacity-20 uppercase tracking-widest text-[10px] sm:text-xs font-bold ${
            status === 'idle' ? 'text-gray-400 bg-gray-500' :
            status === 'uploading' ? 'text-blue-400 bg-blue-500' :
            status === 'processing' ? 'text-yellow-400 bg-yellow-500 animate-pulse' :
            'text-green-400 bg-green-500'
          }`}>
            {status}
          </span>
        </div>
      </header>

      {/* Main Grid Layout */}
      <main className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Ingestion & Chat */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <UploadNode />
          <RAGQueryInterface />
        </div>

        {/* Right Column: Terminal & Extraction Visualization */}
        <div className="lg:col-span-7 flex flex-col">
          <CognitiveTerminal />
        </div>

      </main>
    </div>
  );
}

export default App;
