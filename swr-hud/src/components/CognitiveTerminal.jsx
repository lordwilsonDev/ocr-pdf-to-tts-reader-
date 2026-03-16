import React, { useEffect, useState, useRef } from 'react';
import { Terminal, Activity, ChevronRight } from 'lucide-react';
import { useSwr } from '../context/SwrContext';

export function CognitiveTerminal() {
  const { status, documentId } = useSwr();
  const [logs, setLogs] = useState([
    { id: 1, text: "SWR Neural Engine Initialized", type: "system" },
    { id: 2, text: "Awaiting intel payload...", type: "info" }
  ]);
  const endRef = useRef(null);

  useEffect(() => {
    if (status === 'processing') {
      const msgs = [
        "Analyzing high-DPI artifact layers...",
        "Executing Gutter-Void resolution protocol...",
        "Bypassing adversarial layout noise...",
        "Extracting textual telemetry..."
      ];
      let i = 0;
      const t = setInterval(() => {
        if (i < msgs.length) {
          setLogs(prev => [...prev, { id: Date.now(), text: msgs[i], type: "processing" }]);
          i++;
        }
      }, 1500);
      return () => clearInterval(t);
    }
    
    if (status === 'ready') {
      setLogs(prev => [...prev, { id: Date.now(), text: "Assimilation Complete. RAG Nodes Armed.", type: "success" }]);
    }
  }, [status]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="glass-panel flex flex-col h-[500px] lg:h-full relative overflow-hidden group">
      
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-swr-border/50 bg-black/20">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-swr-muted" />
          <h2 className="text-sm font-semibold tracking-wider uppercase text-swr-muted">Cognitive Feed</h2>
        </div>
        <div className="flex items-center gap-2">
          {status === 'processing' && (
            <Activity className="w-4 h-4 text-yellow-500 animate-pulse" />
          )}
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
          </div>
        </div>
      </div>

      {/* Terminal Output */}
      <div className="flex-1 p-4 font-mono text-xs sm:text-sm overflow-y-auto space-y-2">
        {logs.map((log) => (
          <div key={log.id} className="flex items-start gap-2 animate-fade-in opacity-90 hover:opacity-100">
            <span className="text-swr-muted shrink-0 mt-0.5"><ChevronRight className="w-4 h-4" /></span>
            <span className={`
              ${log.type === 'system' ? 'text-gray-400' : ''}
              ${log.type === 'info' ? 'text-blue-400' : ''}
              ${log.type === 'processing' ? 'text-yellow-400' : ''}
              ${log.type === 'success' ? 'text-green-400 font-bold' : ''}
            `}>
              {log.text}
            </span>
          </div>
        ))}
        {status === 'processing' && (
          <div className="flex items-center gap-2 text-swr-muted animate-pulse">
            <ChevronRight className="w-4 h-4" />
            <span className="w-2 h-4 bg-swr-accent animate-ping rounded-sm"></span>
          </div>
        )}
        <div ref={endRef} />
      </div>
      
      {/* Subtle Terminal Scanline Overlay */}
      <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(255,255,255,0)_50%,rgba(0,0,0,0.1)_50%)] bg-[length:100%_4px] opacity-20"></div>
    </div>
  );
}
