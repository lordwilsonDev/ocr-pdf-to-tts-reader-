import React, { useState } from 'react';
import { Send, Sparkles, AlertCircle } from 'lucide-react';
import { useSwr } from '../context/SwrContext';

export function RAGQueryInterface() {
  const { status } = useSwr();
  const [query, setQuery] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query.trim() || status === 'idle' || status === 'uploading') return;

    const userQ = query;
    setQuery('');
    setChat(prev => [...prev, { role: 'user', text: userQ }]);
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:8000/query?q=${encodeURIComponent(userQ)}`);
      const data = await res.json();
      setChat(prev => [...prev, { role: 'agent', text: data.answer }]);
    } catch (error) {
      setChat(prev => [...prev, { role: 'agent', text: "Comms Link Severed. Unable to reach Sovereign Swarm." }]);
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = status === 'idle' || status === 'uploading';

  return (
    <div className="glass-panel flex flex-col h-[400px] relative">
      <div className="p-4 border-b border-swr-border/50 flex justify-between items-center">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <span className="text-swr-accent">02.</span> Sovereign Extraction
        </h2>
        {isDisabled && (
          <div className="flex items-center gap-1.5 text-xs text-yellow-500 bg-yellow-500/10 px-2 py-1 rounded border border-yellow-500/20">
            <AlertCircle className="w-3 h-3" /> Awaiting Payload
          </div>
        )}
      </div>

      {/* Chat Area */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {chat.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-swr-muted text-sm space-y-2 opacity-50">
            <Sparkles className="w-8 h-8" />
            <p>Awaiting Queries against Ingested Data</p>
          </div>
        ) : (
          chat.map((msg, i) => (
            <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[85%] p-3 rounded-2xl ${
                msg.role === 'user' 
                  ? 'bg-swr-accent text-white rounded-tr-sm' 
                  : 'bg-white/5 border border-swr-border/50 text-swr-text rounded-tl-sm'
              }`}>
                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.text}</p>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex items-start">
            <div className="max-w-[85%] p-3 rounded-2xl bg-white/5 border border-swr-border/50 rounded-tl-sm flex items-center gap-2">
               <div className="w-2 h-2 rounded-full bg-swr-accent animate-bounce"></div>
               <div className="w-2 h-2 rounded-full bg-swr-accent animate-bounce delay-75"></div>
               <div className="w-2 h-2 rounded-full bg-swr-accent animate-bounce delay-150"></div>
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="p-4 border-t border-swr-border/50 bg-black/20">
        <form onSubmit={handleQuery} className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isDisabled || loading}
            placeholder={isDisabled ? "Insert payload first..." : "Query the Sovereign Subconscious..."}
            className="w-full bg-black/40 border border-swr-border rounded-xl pl-4 pr-12 py-3 text-sm text-swr-text placeholder:text-swr-muted focus:outline-none focus:border-swr-accent transition-colors disabled:opacity-50"
          />
          <button 
            type="submit"
            disabled={isDisabled || loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-swr-muted hover:text-swr-accent transition-colors disabled:opacity-50 disabled:hover:text-swr-muted"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
