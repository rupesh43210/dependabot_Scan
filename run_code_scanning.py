#!/usr/bin/env python3
"""
Code Scanning Pipeline - Main Entry Point
Optimized entry point for running Code Scanning alert scans.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function from code_scanning_pipeline
if __name__ == "__main__":
    from code_scanning_pipeline import main
    sys.exit(main())
