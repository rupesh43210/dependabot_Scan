#!/usr/bin/env python3
"""
Setup and Test Script for MiDAS Security Pipeline

This script sets up the environment and tests the security pipeline components.

Author: GitHub Copilot
Version: 2.0.0
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def print_header(title: str):
    """Print formatted header."""
    print(f"\n{'=' * 60}")
    print(f"🔧 {title}")
    print(f"{'=' * 60}")


def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print("   Python 3.8+ is required for this pipeline")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True


def check_required_packages():
    """Check if required packages are installed."""
    print("\n📦 Checking required packages...")
    
    required_packages = {
        'requests': '2.32.0',
        'pandas': '2.3.0',
        'github': '2.8.0', 
        'python-dotenv': '1.2.0',
        'openpyxl': '3.1.0'
    }
    
    missing_packages = []
    installed_packages = {}
    
    for package, min_version in required_packages.items():
        try:
            if package == 'github':
                import github
                version = getattr(github, '__version__', 'installed')
                module_name = 'PyGithub'
            elif package == 'python-dotenv':
                import dotenv
                version = getattr(dotenv, '__version__', 'installed')
                module_name = 'python-dotenv'
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'installed')
                module_name = package
            
            installed_packages[module_name] = version
            print(f"   ✅ {module_name}: {version}")
            
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}: Not installed")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements_optimized.txt")
        return False
    
    return True


def check_environment_variables():
    """Check environment variables."""
    print("\n🔑 Checking environment variables...")
    
    # Load .env file
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv()
        print("   ✅ .env file found and loaded")
    else:
        print("   ⚠️  .env file not found")
    
    # Check GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        token_preview = f"{github_token[:8]}..." if len(github_token) > 8 else "***"
        print(f"   ✅ GITHUB_TOKEN: {token_preview}")
        
        if len(github_token) < 20:
            print("   ⚠️  Token seems too short - please verify")
            return False
    else:
        print("   ❌ GITHUB_TOKEN: Not set")
        print("      Please add GITHUB_TOKEN=your_token_here to .env file")
        return False
    
    # Check organization
    org_name = os.getenv('GITHUB_ORG', 'MiDAS')
    print(f"   ✅ Organization: {org_name}")
    
    return True


def test_github_connectivity():
    """Test GitHub Enterprise connectivity."""
    print("\n🌐 Testing GitHub Enterprise connectivity...")
    
    try:
        from config_utils import validate_environment
        config = validate_environment()
        
        from vulnerability_scanner import VulnerabilityScanner
        scanner = VulnerabilityScanner(config['github_token'])
        
        # Try to get organization info
        org = scanner.github_client.get_organization(config['org_name'])
        print(f"   ✅ Connected to organization: {org.name}")
        print(f"   📊 Organization has {org.public_repos + org.total_private_repos} repositories")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False


def test_pipeline_components():
    """Test individual pipeline components."""
    print("\n🧪 Testing pipeline components...")
    
    try:
        # Test scanner import
        from vulnerability_scanner import VulnerabilityScanner
        print("   ✅ VulnerabilityScanner: Import successful")
        
        # Test report generator import
        from security_report_generator import SecurityReportGenerator
        print("   ✅ SecurityReportGenerator: Import successful")
        
        # Test main pipeline import
        from midas_security_pipeline import MiDASSecurityPipeline
        print("   ✅ MiDASSecurityPipeline: Import successful")
        
        # Test config utilities
        from config_utils import Config, validate_environment
        print("   ✅ Config utilities: Import successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Component test failed: {e}")
        return False


def create_sample_env_file():
    """Create a sample .env file if it doesn't exist."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("\n📝 Creating sample .env file...")
        
        sample_content = """# MiDAS Security Pipeline Configuration
# Copy this file to .env and fill in your values

# GitHub Enterprise Token (required)
# Get from: https://github.boschdevcloud.com/settings/tokens
GITHUB_TOKEN=your_github_enterprise_token_here

# Organization to scan (optional, defaults to MiDAS)
GITHUB_ORG=MiDAS

# GitHub Enterprise base URL (optional)
GITHUB_BASE_URL=https://github.boschdevcloud.com
"""
        
        with open(env_file, 'w') as f:
            f.write(sample_content)
        
        print(f"   ✅ Sample .env file created")
        print(f"   ⚠️  Please edit .env and add your GitHub token")
        return False
    
    return True


def run_quick_test():
    """Run a quick functionality test."""
    print("\n⚡ Running quick functionality test...")
    
    try:
        # Create test data
        test_data = [
            {
                'repository': 'test-repo',
                'severity': 'HIGH',
                'cvss_score': 7.5,
                'alert_state': 'open',
                'summary': 'Test vulnerability',
                'package_name': 'test-package'
            }
        ]
        
        # Test report generation
        from security_report_generator import SecurityReportGenerator
        import pandas as pd
        
        generator = SecurityReportGenerator()
        generator.data = pd.DataFrame(test_data)
        generator._calculate_statistics()
        
        executive_df = generator.generate_executive_summary()
        detailed_df = generator.generate_detailed_report()
        
        if not executive_df.empty and not detailed_df.empty:
            print("   ✅ Report generation: Working")
        else:
            print("   ⚠️  Report generation: Empty results")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Quick test failed: {e}")
        return False


def main():
    """Main setup and test function."""
    print("🚀 MiDAS Security Pipeline Setup & Test")
    print("Version 2.0.0")
    
    all_checks_passed = True
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Environment Setup", lambda: create_sample_env_file() and check_environment_variables()),
        ("Pipeline Components", test_pipeline_components),
        ("GitHub Connectivity", test_github_connectivity),
        ("Quick Functionality Test", run_quick_test)
    ]
    
    for check_name, check_func in checks:
        print_header(check_name)
        try:
            if not check_func():
                all_checks_passed = False
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            all_checks_passed = False
    
    # Final summary
    print_header("Setup Summary")
    
    if all_checks_passed:
        print("🎉 All checks passed! The pipeline is ready to use.")
        print("\n📋 Quick Start:")
        print("   1. Ensure your .env file has the correct GITHUB_TOKEN")
        print("   2. Run: python midas_security_pipeline.py")
        print("\n📚 Available Commands:")
        print("   • Full pipeline: python midas_security_pipeline.py")
        print("   • Scan only: python vulnerability_scanner.py")
        print("   • Reports only: python security_report_generator.py <data_file>")
    else:
        print("❌ Some checks failed. Please address the issues above.")
        print("\n🔧 Common Solutions:")
        print("   • Install packages: pip install -r requirements_optimized.txt")
        print("   • Set GitHub token in .env file")
        print("   • Check network connectivity to GitHub Enterprise")
    
    return all_checks_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)