from typing import List, Dict
from .ocr_engine import TextBlock
import time

class EmotionGate:
    """Maps visual metadata to acoustic prosody parameters."""
    
    @staticmethod
    def get_prosody(block: TextBlock) -> Dict[str, Any]:
        params = {
            "rate": 1.0,      # 1.0 = normal
            "pitch": 0,      # 0 = normal
            "volume": 0.8,   # 0.8 = normal
            "pause": 0.2     # seconds
        }
        
        # 1. Header Logic
        if block.is_header:
            params["rate"] = 0.85
            params["pitch"] = 5
            params["volume"] = 1.0
            params["pause"] = 0.8
            
        # 2. All CAPS (Urgency/Emphasis)
        elif block.text.isupper() and len(block.text) > 3:
            params["rate"] = 1.1
            params["pitch"] = 2
            params["volume"] = 0.95
            
        # 3. Punctuation Damping
        if block.text.endswith((".", "!", "?")):
            params["pause"] = 0.6
        elif block.text.endswith(","):
            params["pause"] = 0.3
            
        return params

class AdaptiveTTS:
    """TTS Engine with Adaptive Prosody implementation."""
    
    def __init__(self):
        self.gate = EmotionGate()
        
    def speak_simulated(self, blocks: List[TextBlock]):
        """Runs the manifestation pipeline with prosody injection."""
        print("\n🎧 STARTING ADAPTIVE PLAYBACK...")
        
        for b in blocks:
            prosody = self.gate.get_prosody(b)
            
            # Simulated manifestation
            meta = f"[R:{prosody['rate']} P:{prosody['pitch']} V:{prosody['volume']}]"
            
            if b.is_header:
                print(f"📣 {meta} >> {b.text.upper()}")
            elif b.text.isupper():
                print(f"🔊 {meta} >> {b.text}")
            else:
                print(f"🗣️ {meta} >> {b.text}")
                
            # Simulate real-time pause
            time.sleep(0.1) # Accelerated for demo, but logic is there
