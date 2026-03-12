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
    
    def __init__(self, gutter_threshold: int = 50, sidebar_threshold: float = 0.75):
        self.gutter_threshold = gutter_threshold
        self.sidebar_threshold = sidebar_threshold # x > 75% of page width is a sidebar

    def resolve(self, blocks: List[TextBlock]) -> List[TextBlock]:
        """
        Resolves spatial coordinates into logical reading sequences using
        Gutter-Aware clustering and Sidebar Sequestration.
        """
        if not blocks:
            return []

        # 1. Normalize based on Page Dimensions
        max_x = max(b.x + b.w for b in blocks)
        max_w = max(b.w for b in blocks)
        
        # 2. Separate Headers and Sidebars
        headers = [b for b in blocks if b.w > max_w * 0.65 or b.is_header]
        sidebars = [b for b in blocks if b.x > max_x * self.sidebar_threshold and b not in headers]
        main_content = [b for b in blocks if b not in headers and b not in sidebars]

        # 3. Identify Columns in Main Content
        # Sort by x and scan for gaps larger than gutter_threshold
        sorted_main = sorted(main_content, key=lambda b: b.x)
        
        column_groups = []
        if sorted_main:
            current_group = [sorted_main[0]]
            for i in range(1, len(sorted_main)):
                # If the gap between current word and previous word's right edge is large
                # Or if the current word's X is significantly different
                if sorted_main[i].x - (current_group[-1].x + current_group[-1].w) > self.gutter_threshold:
                    column_groups.append(current_group)
                    current_group = [sorted_main[i]]
                else:
                    current_group.append(sorted_main[i])
            column_groups.append(current_group)
            
        # 4. Assemble Logical Sequence
        # Headers First (Title, etc.)
        resolved_sequence = sorted(headers, key=lambda b: b.y)
        
        # Sort column groups by their leftmost block's X
        column_groups.sort(key=lambda g: min(b.x for b in g))
        
        # Main Columns
        for group in column_groups:
            # Sort blocks within column by Y
            resolved_sequence.extend(sorted(group, key=lambda b: b.y))
            
        # Sidebars Last (Footnotes, Marginalia)
        resolved_sequence.extend(sorted(sidebars, key=lambda b: b.y))
            
        return resolved_sequence

if __name__ == "__main__":
    from .ocr_engine import VisualChunker
    engine = VisualChunker()
    # Mocking blocks for testing
    b1 = TextBlock("Header", 0, 0, 800, 50, 100, is_header=True)
    b2 = TextBlock("Col 1 Line 1", 50, 100, 300, 20, 100)
    b3 = TextBlock("Col 2 Line 1", 450, 100, 300, 20, 100)
    b4 = TextBlock("Col 1 Line 2", 50, 130, 300, 20, 100)
    b5 = TextBlock("Sidebar Note", 760, 200, 40, 500, 100)
    
    resolver = LayoutResolver()
    logical_blocks = resolver.resolve([b1, b2, b3, b4, b5])
    
    print("\n--- LOGICAL ORDER (Reading Order) ---")
    for b in logical_blocks:
        print(f"[{b.x}, {b.y}] {b.text}")
