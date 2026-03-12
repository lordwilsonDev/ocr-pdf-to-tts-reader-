import os
from pypdf import PdfReader
from typing import List
from .ocr_engine import TextBlock

class PDFIngestor:
    """Handles real PDF parsing and extraction."""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        
    def ingest(self, file_path: str) -> Dict:
        """Parses PDF and returns metadata."""
        reader = PdfReader(file_path)
        return {
            "filename": os.path.basename(file_path),
            "pages": len(reader.pages),
            "metadata": reader.metadata
        }
        
    def get_page_text(self, file_path: str, page_num: int) -> str:
        """Extracts native text if available, fallback for OCR soon."""
        reader = PdfReader(file_path)
        if page_num < len(reader.pages):
            return reader.pages[page_num].extract_text()
        return ""
