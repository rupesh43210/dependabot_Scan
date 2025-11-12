#!/usr/bin/env python3
"""
Dependabot Security Pipeline - Main Entry Point
Optimized entry point for running Dependabot vulnerability scans.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function from security_pipeline
if __name__ == "__main__":
    from security_pipeline import main
    sys.exit(main())
