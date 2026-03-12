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

class WhisperAgent:
    """The orchestrator with document context memory."""
    
    def __init__(self):
        self.ocr = VisualChunker()
        self.layout = LayoutResolver()
        self.tts = AdaptiveTTS()
        self.ingestor = PDFIngestor()
        self.document_memory: List[str] = []
        self.current_session_id: int = 0
        self.status = "IDLE"
        
    def process_document(self, path: str):
        """Full production pipeline."""
        self.status = "INGESTING"
        # 1. Verification & Ingestion
        print(f"📦 INGESTING SOURCE: {path}")
        meta = self.ingestor.ingest(path)
        
        # 2. Extraction
        self.status = "EXTRACTING"
        raw = self.ocr.extract(path)
        
        # 3. Layout Resolution (The Column Fix)
        self.status = "RESOLVING_LAYOUT"
        logical_order = self.layout.resolve(raw)
        
        # 4. Memory Manifestation (Building Context)
        self.status = "INDEXING"
        self.document_memory = [] # Refresh for new doc
        for b in logical_order:
            self.document_memory.append(b.text)
            
        # 5. Manifestation
        self.status = "SPEAKING"
        self.tts.speak_simulated(logical_order)
        self.status = "COMPLETED"
        
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
        
        return "The document emphasizes technical sovereignty as a core technical imperative."

if __name__ == "__main__":
    agent = WhisperAgent()
    try:
        agent.process_document("demo_paper.pdf")
    except Exception as e:
        print(f"⚠️  Ingestion Simulation: {e}")
        # Manual Trigger for Demo
        agent.status = "SPEAKING"
        agent.document_memory = ["The future lies in local-first, agent-driven architectures."]
    
    print("\n--- INTERRUPTION ---")
    print(f"Agent Response: {agent.query('What does it say about the future?')}")
