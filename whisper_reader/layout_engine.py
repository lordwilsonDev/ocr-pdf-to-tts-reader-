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
        Resolves spatial coordinates into logical reading sequences using
        Gutter-Aware clustering.
        """
        if not blocks:
            return []

        # 1. Coordinate Normalization & Header Separation
        # Blocks with W > 70% of max width are treated as potential headers (full width)
        max_w = max(b.w for b in blocks)
        headers = [b for b in blocks if b.w > max_w * 0.7]
        others = [b for b in blocks if b not in headers]

        # 2. Identify Column Voids
        # Sort by x and scan for gaps larger than gutter_threshold
        sorted_others = sorted(others, key=lambda b: b.x)
        
        column_groups = []
        if sorted_others:
            current_group = [sorted_others[0]]
            for i in range(1, len(sorted_others)):
                if sorted_others[i].x - (current_group[-1].x + current_group[-1].w) > self.gutter_threshold:
                    column_groups.append(current_group)
                    current_group = [sorted_others[i]]
                else:
                    current_group.append(sorted_others[i])
            column_groups.append(current_group)
            
        # 3. Assemble Logical Sequence
        resolved_sequence = sorted(headers, key=lambda b: b.y)
        
        # Sort column groups by their leftmost block's X
        column_groups.sort(key=lambda g: min(b.x for b in g))
        
        for group in column_groups:
            # Sort blocks within column by Y
            resolved_sequence.extend(sorted(group, key=lambda b: b.y))
            
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
