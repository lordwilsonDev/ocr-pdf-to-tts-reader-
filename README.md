# Sovereign Whisper Reader (SWR)

> **"Beyond the pixel. Into the voice."**

Sovereign Whisper Reader is a high-fidelity, local-first accessibility pipeline that solves the "broken reader" problem. Most OCR readers fail at multi-column layouts, read in a monotone drone, and offer zero interactivity. SWR is built to understand **layout density**, **prosody**, and **context**.

## The "Next-Gen" Feature Set (What was missing)

### 1. The Column Resolver (Layout-Aware)
Standard readers often read across columns (Left Line 1 -> Right Line 1). SWR uses a geometric clustering algorithm to identify distinct vertical columns and sidebars, automatically reordering text blocks into a **human-logical reading sequence**.

### 2. Adaptive Prosody (Emotion Gate)
Speech isn't just words; it's timing. SWR dynamically adjusts playback parameters:
- **Cognitive Pauses**: Inserts millisecond delays at punctuation based on surrounding sentence complexity.
- **Emphasis Mapping**: Detected CAPS/Bold/Headers in OCR are automatically translated into "Slower & Louder" speech segments.
- **Speed Density**: Rapidly reads simple lists but slows down for high-density headers.

### 3. Contextual Interruption (The RAG Hook)
**No one else is doing this.** While reading, the SWR Agent builds a real-time vector memory of the document. You can interrupt the playback to ask:
- *"Wait, what was the evidence for that claim?"*
- *"Summarize the last two paragraphs."*
- *"Why is the Cloud mentioned here?"*
The agent uses its document memory to answer without losing your place in the reader.

---

## Technical Architecture

- **Engine**: Pure Python, zero-dependency orchestrator.
- **OCR**: Integrated `VisualChunker` supporting Tesseract/EasyOCR metadata.
- **Layout**: Geometric clustering and semantic reordering engine.
- **TTS**: Adaptive prosody wrapper with SSML-like injection.
- **AI**: Local RAG memory agent.

---

## Quick Start

```bash
# Clone
git clone https://github.com/lordwilsonDev/sovereign-whisper-reader.git
cd sovereign-whisper-reader

# Run the High-Fidelity Demo
python3 main.py
```

### Advanced Usage (Context Query)
```python
from whisper_reader.agent import WhisperAgent

agent = WhisperAgent()
agent.process_document("academic_paper.pdf")

# Interrupt and ask
print(agent.query("What is the core conclusion?"))
```

---

## Fuel The Lab
If you love what we are doing at **BlackSwanLabz**, fuel the mission. We prioritize sovereignty, privacy, and building with love. 🖤 Swan out. 🖤🦢

---

## License
MIT — Free as in love.
