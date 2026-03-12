#!/usr/bin/env python3
"""
Layout Engine — Multi-Column Resolution and Semantic Reordering
==============================================================

The 'Brains' of SWR. Resolves jumbled OCR blocks into logical reading order.
Uses geometric clustering to identify columns and sidebars.
"""

from typing import List, Dict, Any
from .ocr_engine import TextBlock

class LayoutResolver:
    """Resolves spatial coordinates into logical reading sequences."""
    
    def __init__(self, gutter_threshold: int = 50):
        self.gutter_threshold = gutter_threshold

    def resolve(self, blocks: List[TextBlock]) -> List[TextBlock]:
        """
        Sorts blocks semantically:
        1. Identify distinct columns based on 'x' alignment.
        2. Group blocks into columns.
        3. Sort columns by 'x' (left to right).
        4. Sort blocks within columns by 'y' (top to bottom).
        """
        if not blocks:
            return []

        # 1. Identify Column Centers using simple clustering
        columns_map: Dict[int, List[TextBlock]] = {}
        
        # Sort by x first to make clustering easier
        sorted_x = sorted(blocks, key=lambda b: b.x)
        
        current_col_x = sorted_x[0].x
        columns_map[current_col_x] = []
        
        for b in sorted_x:
            # If this block is significantly further right than the current col x, start new col
            if abs(b.x - current_col_x) > self.gutter_threshold:
                current_col_x = b.x
                columns_map[current_col_x] = []
            
            columns_map[current_col_x].append(b)
            
        # 2. Sort columns by horizontal position (Header vs Main vs Sidebar)
        col_keys = sorted(columns_map.keys())
        
        resolved_sequence = []
        
        # 3. Flatten into reading order:
        # NOTE: We handle 'Headers' (full-width) separately if they span multiple columns
        # In this simple logic, they'll just be in their own col if aligned left
        
        for col_x in col_keys:
            # Sort blocks within the column by Y (top to bottom)
            col_blocks = sorted(columns_map[col_x], key=lambda b: b.y)
            resolved_sequence.extend(col_blocks)
            
        return resolved_sequence

if __name__ == "__main__":
    from .ocr_engine import VisualChunker
    engine = VisualChunker()
    raw_blocks = engine.extract("demo.pdf")
    
    resolver = LayoutResolver()
    logical_blocks = resolver.resolve(raw_blocks)
    
    print("--- RAW ORDER (Detection Order) ---")
    for b in raw_blocks[:3]: print(f"[{b.x}] {b.text[:30]}")
    
    print("\n--- LOGICAL ORDER (Reading Order) ---")
    for b in logical_blocks:
        print(f"[{b.x}, {b.y}] {b.text}")
