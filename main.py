#!/usr/bin/env python3
"""
Sovereign Whisper Reader — Main Entry Point
==========================================

Demonstrates the high-fidelity OCR-to-TTS pipeline.
Solves layout jumble and adds contextual intelligence.
"""

import sys
from whisper_reader.agent import WhisperAgent

def main():
    print("━" * 50)
    print("      SOVEREIGN WHISPER READER v1.0")
    print("      'Compiling Knowledge into Voice'")
    print("━" * 50)
    
    agent = WhisperAgent()
    
    # 1. Run the Pipeline
    print(f"\n[+] Input: academic_paper_multicol.pdf")
    agent.process_document("academic_paper_multicol.pdf")
    
    # 2. Demonstrate the 'Unthought-of' Feature: Contextual Interruption
    print("\n" + "━" * 50)
    print("  FEATURE DEMO: Contextual Interruption")
    print("━" * 50)
    
    questions = [
        "Cloud Agent, why is cloud computing a problem?",
        "What is the core conclusion of this paper?"
    ]
    
    for q in questions:
        response = agent.query(q)
        print(f"🤖 Agent: \"{response}\"")

    print("\n✅ MISSION COMPLETE: Reader fully manifested.")

if __name__ == "__main__":
    main()
