#!/usr/bin/env python3
"""
Configuration customization examples for GitHub Issue Creator.
This script shows how to easily modify issue settings via the config file.
"""

import json
from pathlib import Path
from config_manager import IssueConfig

def create_custom_config():
    """Create a custom configuration file with different settings."""
    
    print("🔧 Creating Custom Configuration Examples")
    print("=" * 50)
    
    # Example 1: Different project and labels
    custom_config = {
        "issue_settings": {
            "default_project": "Security Team",
            "project_number": 15,
            "labels": [
                {
                    "name": "security",
                    "color": "d73a4a",
                    "description": "Security-related issue"
                },
                {
                    "name": "critical",
                    "color": "ff0000", 
                    "description": "Critical priority issue"
                },
                {
                    "name": "dependabot",
                    "color": "0366d6",
                    "description": "Dependabot security alert"
                }
            ],
            "title_format": "[SECURITY] {repository} - {critical} Critical, {high} High, {medium} Medium, {low} Low vulnerabilities",
            "auto_assign_project": True,
            "include_timestamp": True,
            "force_update_existing": False
        },
        "github_settings": {
            "organization": "MyOrg",
            "base_url": "https://github.com"
        },
        "severity_settings": {
            "minimum_severity": "medium",
            "severity_order": ["critical", "high", "medium", "low"],
            "severity_colors": {
                "critical": "d73a4a",
                "high": "ff6b6b", 
                "medium": "fbca04",
                "low": "28a745"
            }
        }
    }
    
    # Save example config
    config_path = Path("custom_config_example.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(custom_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created: {config_path}")
    print("   - Project: Security Team")
    print("   - Labels: security, critical, dependabot")
    print("   - Includes timestamp in issues")
    
    # Example 2: Minimal config (just override project)
    minimal_config = {
        "issue_settings": {
            "default_project": "DevOps Team",
            "project_number": 8
        }
    }
    
    minimal_path = Path("minimal_config_example.json")
    with open(minimal_path, 'w', encoding='utf-8') as f:
        json.dump(minimal_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created: {minimal_path}")
    print("   - Only overrides project settings")
    print("   - Uses defaults for everything else")
    
    # Example 3: Color customization
    color_config = {
        "issue_settings": {
            "labels": [
                {
                    "name": "vulnerability",
                    "color": "e11d21",
                    "description": "Security vulnerability"
                },
                {
                    "name": "high-priority", 
                    "color": "ff6900",
                    "description": "High priority issue"
                }
            ]
        },
        "severity_settings": {
            "severity_colors": {
                "critical": "e11d21",
                "high": "ff6900",
                "medium": "fef2c0", 
                "low": "c2e0c6"
            }
        }
    }
    
    color_path = Path("color_config_example.json")
    with open(color_path, 'w', encoding='utf-8') as f:
        json.dump(color_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created: {color_path}")
    print("   - Custom label colors")
    print("   - Custom severity colors")

def show_usage_examples():
    """Show how to use different configurations."""
    print("\n📋 USAGE EXAMPLES")
    print("=" * 50)
    
    print("# Use default configuration:")
    print("python create_security_issues.py --auto")
    
    print("\n# Use custom configuration file:")
    print("python create_security_issues.py --auto --config custom_config_example.json")
    
    print("\n# Use minimal config (just different project):")
    print("python create_security_issues.py --auto --config minimal_config_example.json")
    
    print("\n# Use config but override project on command line:")
    print("python create_security_issues.py --auto --config color_config_example.json --project \"Emergency Response\"")
    
    print("\n# Use config but override labels:")
    print("python create_security_issues.py --auto --config custom_config_example.json --labels \"urgent,security\"")

def test_configurations():
    """Test loading different configurations."""
    print("\n🧪 TESTING CONFIGURATIONS")
    print("=" * 50)
    
    configs = [
        ("Default", "issue_config.json"),
        ("Custom", "custom_config_example.json"),
        ("Minimal", "minimal_config_example.json"),
        ("Colors", "color_config_example.json")
    ]
    
    for name, config_file in configs:
        if Path(config_file).exists():
            print(f"\n📄 {name} Configuration ({config_file}):")
            try:
                config = IssueConfig(config_file)
                print(f"   Project: {config.default_project}")
                print(f"   Labels: {', '.join(config.get_label_names())}")
                print(f"   Auto-assign: {config.auto_assign_project}")
                print(f"   Timestamp: {config.include_timestamp}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

def main():
    """Main function."""
    print("🎨 GitHub Issue Creator - Configuration Examples")
    print("=" * 60)
    
    create_custom_config()
    show_usage_examples()
    test_configurations()
    
    print("\n✅ Configuration examples created!")
    print("Edit issue_config.json or create your own config file to customize:")
    print("  - Project names and numbers")
    print("  - Labels and colors") 
    print("  - Title formats")
    print("  - Organization settings")
    print("  - And much more!")

if __name__ == "__main__":
    main()