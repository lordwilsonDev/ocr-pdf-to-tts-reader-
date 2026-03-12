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

class WhisperAgent:
    """The orchestrator with document context memory."""
    
    def __init__(self):
        self.ocr = VisualChunker()
        self.layout = LayoutResolver()
        self.tts = AdaptiveTTS()
        self.document_memory: List[str] = []
        
    def process_document(self, path: str):
        """Full pipeline: Extract -> Resolve -> Ingest -> Speak."""
        # 1. Extraction
        raw = self.ocr.extract(path)
        
        # 2. Layout Resolution (The Column Fix)
        logical_order = self.layout.resolve(raw)
        
        # 3. Memory Ingestion (The RAG Prep)
        print(f"🧠 Indexing document context in local memory...")
        for b in logical_order:
            self.document_memory.append(b.text)
            
        # 4. Manifestation (The Adaptive TTS)
        self.tts.speak_simulated(logical_order)
        
    def query(self, question: str) -> str:
        """The 'Contextual Interruption' feature."""
        # Simple local search (simulated RAG)
        context = " ".join(self.document_memory)
        print(f"\n❓ QUERY: '{question}'")
        
        # Basic keyword match simulation
        if "cloud" in question.lower():
            return "Based on the text, cloud computing is described as a systemic chokepoint due to vendor lock-in."
        elif "future" in question.lower():
            return "The document states that the future lies in local-first, agent-driven architectures."
        
        return "The document doesn't explicitly mention that, but emphasizes technical sovereignty."

if __name__ == "__main__":
    agent = WhisperAgent()
    agent.process_document("demo_paper.pdf")
    print("\n--- INTERRUPTION ---")
    print(f"Agent Response: {agent.query('What does it say about the future?')}")
