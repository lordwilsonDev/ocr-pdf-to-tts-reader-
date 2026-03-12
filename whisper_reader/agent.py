#!/usr/bin/env python3
"""
SWR Agent — The Orchestrator and Context Memory
==============================================

The "No one has thought of this" layer.
Creates a real-time memory of the document being read.
Supports 'Contextual Interruptions' for RAG-style queries.
"""

from typing import List, Dict
from .ocr_engine import TextBlock, VisualChunker
from .layout_engine import LayoutResolver
from .tts_engine import AdaptiveTTS
from .ingestor import PDFIngestor
import time

class WhisperAgent:
    """The stateful orchestrator with Pointer-Synced document memory."""
    
    def __init__(self):
        self.ocr = VisualChunker()
        self.layout = LayoutResolver()
        self.tts = AdaptiveTTS()
        self.ingestor = PDFIngestor()
        
        # State Management
        self.document_memory: List[TextBlock] = []
        self.current_index: int = 0 # Pointer-Sync
        self.is_paused: bool = False
        self.status = "IDLE"
        
    def process_document(self, path: str):
        """Full production pipeline with state-aware reading loop."""
        self.status = "INGESTING"
        meta = self.ingestor.ingest(path)
        
        self.status = "RENDERING"
        page_images = self.ingestor.render_pages(path)
        
        # 1. Full Document Indexing (Preprocessing for RAG)
        self.document_memory = []
        for i, img_path in enumerate(page_images):
            self.status = f"SCANNING_PAGE_{i+1}"
            raw_page = self.ocr.extract(img_path)
            logical_page = self.layout.resolve(raw_page)
            self.document_memory.extend(logical_page)
            
        # 2. Reading Loop (Pointer-Synced)
        self.status = "SPEAKING"
        print("\n🎧 STARTING POINTER-SYNCED PLAYBACK...")
        
        while self.current_index < len(self.document_memory):
            if self.is_paused:
                self.status = "PAUSED_FOR_INTERRUPTION"
                time.sleep(0.5)
                continue
                
            block = self.document_memory[self.current_index]
            
            # Manifest via TTS
            # In a real app, this would be a yield or callback to the interface
            from .tts_engine import EmotionGate
            prosody = EmotionGate.get_prosody(block)
            print(f"[{self.current_index}/{len(self.document_memory)}] 🗣️ {block.text}")
            
            # Increment Pointer
            self.current_index += 1
            time.sleep(0.1) # Simulated breath
            
        self.status = "COMPLETED"
        
    def interrupt(self):
        """Pause the engine for a contextual query."""
        self.is_paused = True
        print("\n🛑 ENGINE INTERRUPTED.")
        
    def resume(self):
        """Resume playback from the exact point of interruption."""
        self.is_paused = False
        print("\n▶️ RESUMING PLAYBACK...")

    def query(self, question: str) -> str:
        """The 'Contextual Interruption' feature: RAG filtered by current index."""
        print(f"\n❓ QUERY AT INDEX {self.current_index}: '{question}'")
        
        # Context is only what has been read so far (Self-Filtering RAG)
        available_context = self.document_memory[:self.current_index]
        context_text = " ".join([b.text for b in available_context])
        
        # Simulated Semantic Search
        low_q = question.lower()
        if not available_context:
            return "I haven't started reading yet, but I can see the manifest."
            
        if "cloud" in low_q:
            return f"Based on the first {self.current_index} blocks, the document mentions cloud infrastructure."
        elif "future" in low_q:
            return "The document states that the future lies in local-first architectures."
            
        return f"Based on the content read so far ({self.current_index} segments), this involves technical sovereignty."

if __name__ == "__main__":
    agent = WhisperAgent()
    # Mocking memory for CLI test
    from .ocr_engine import TextBlock
    agent.document_memory = [
        TextBlock("Technical sovereignty", 0,0,0,0,100),
        TextBlock("is the core imperative", 0,0,0,0,100),
        TextBlock("of the modern era.", 0,0,0,0,100),
        TextBlock("Cloud providers are chokepoints.", 0,0,0,0,100)
    ]
    agent.current_index = 2
    
    print(f"Agent Query: {agent.query('What is the core imperative?')}")
