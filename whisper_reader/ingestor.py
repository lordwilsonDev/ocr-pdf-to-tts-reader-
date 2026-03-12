import os
from pypdf import PdfReader
from pdf2image import convert_from_path
from typing import List, Dict
from PIL import Image

class PDFIngestor:
    """Handles real PDF parsing and high-resolution rendering."""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        self.render_dir = os.path.join(upload_dir, "renders")
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.render_dir, exist_ok=True)
        
    def ingest(self, file_path: str) -> Dict:
        """Parses PDF and returns metadata."""
        reader = PdfReader(file_path)
        return {
            "filename": os.path.basename(file_path),
            "pages": len(reader.pages),
            "metadata": reader.metadata
        }
        
    def render_pages(self, file_path: str) -> List[str]:
        """Converts PDF pages to high-DPI images for OCR."""
        file_id = os.path.basename(file_path).replace(".", "_")
        target_dir = os.path.join(self.render_dir, file_id)
        os.makedirs(target_dir, exist_ok=True)
        
        # Check if already rendered
        existing = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith(".png")]
        if existing:
            return sorted(existing)
            
        print(f"🎨 RENDERING PDF: {file_path}")
        images = convert_from_path(file_path, dpi=300)
        paths = []
        for i, img in enumerate(images):
            p = os.path.join(target_dir, f"page_{i}.png")
            img.save(p, "PNG")
            paths.append(p)
            
        return paths

    def get_page_text(self, file_path: str, page_num: int) -> str:
        """Extracts native text if available."""
        reader = PdfReader(file_path)
        if page_num < len(reader.pages):
            return reader.pages[page_num].extract_text()
        return ""
