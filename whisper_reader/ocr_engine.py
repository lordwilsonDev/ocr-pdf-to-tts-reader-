import pytesseract
from PIL import Image
from dataclasses import dataclass
from typing import List
import os

@dataclass
class TextBlock:
    text: str
    x: int
    y: int
    w: int
    h: int
    confidence: float
    font_size: int = 12
    is_header: bool = False

class OCREngine:
    """The Tesseract-based Precision Ingestion Engine."""
    
    def __init__(self):
        # Tesseract usually found automatically on path via Homebrew
        pass

    def extract_from_image(self, image_path: str) -> List[TextBlock]:
        """Extracts text with raw geometric coordinates."""
        print(f"🔍 OCR SCANNING: {os.path.basename(image_path)}")
        img = Image.open(image_path)
        
        # Get raw data (TSV format logically)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        blocks = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if not text:
                continue
                
            conf = float(data['conf'][i])
            if conf < 10: # Filter noise
                continue
                
            # Create block
            # For simplicity in this v1, we group by word or line?
            # Tesseract gives data at level 5 (word).
            # We will return words and let the Layout engine group them.
            block = TextBlock(
                text=text,
                x=data['left'][i],
                y=data['top'][i],
                w=data['width'][i],
                h=data['height'][i],
                confidence=conf,
                is_header=data['height'][i] > 25 # Simple header heuristic
            )
            blocks.append(block)
            
        return blocks

class VisualChunker: 
    """Compatibility wrapper for the Agent."""
    def __init__(self):
        self.engine = OCREngine()
        
    def extract(self, image_path: str) -> List[TextBlock]:
        return self.engine.extract_from_image(image_path)
