"""
Quick Test Script - Verify New Structure
Tests that the new modular structure works correctly.
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing Module Imports...\n")
    
    try:
        print("├── Testing scanners...")
        from scanners.vulnerability_scanner import VulnerabilityScanner
        from scanners.code_scanning_scanner import CodeScanningScanner
        print("│   ✅ Scanners imported successfully")
        
        print("├── Testing reporters...")
        from reporters.security_report_generator import SecurityReportGenerator
        from reporters.code_scanning_report_generator import CodeScanningReportGenerator
        print("│   ✅ Reporters imported successfully")
        
        print("├── Testing issue managers...")
        from issue_managers.github_issue_manager import GitHubIssueManager
        print("│   ✅ Issue managers imported successfully")
        
        print("├── Testing utilities...")
        from utils.config_loader import load_config, validate_config
        from utils.logger import setup_logger
        print("│   ✅ Utilities imported successfully")
        
        print("└── Testing pipelines...")
        from security_pipeline import SecurityPipeline
        from code_scanning_pipeline import CodeScanningPipeline
        print("    ✅ Pipelines imported successfully")
        
        print("\n✅ All modules imported successfully!")
        print("🎉 New structure is working correctly!\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        print("⚠️  Some modules may need adjustment\n")
        return False

def test_config():
    """Test configuration loading."""
    print("🧪 Testing Configuration Loading...\n")
    
    try:
        from utils.config_loader import load_config, validate_config
        
        config_file = Path(__file__).parent / "config.json"
        if not config_file.exists():
            print("⚠️  config.json not found - skipping config test")
            return True
        
        print("├── Loading config.json...")
        config = load_config()
        print("│   ✅ Configuration loaded")
        
        print("├── Validating configuration...")
        validate_config(config)
        print("│   ✅ Configuration valid")
        
        print("└── Configuration test complete")
        print("\n✅ Configuration system working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("🔧 New Project Structure Verification")
    print("="*60)
    print()
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test configuration
    results.append(test_config())
    
    # Summary
    print("="*60)
    if all(results):
        print("✅ ALL TESTS PASSED - Structure is ready to use!")
    else:
        print("⚠️  SOME TESTS FAILED - Check errors above")
    print("="*60)
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
