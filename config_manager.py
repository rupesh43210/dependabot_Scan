#!/usr/bin/env python3
"""
Configuration manager for GitHub Issue Creator.
Handles loading and validation of issue creation settings from JSON config file.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

class IssueConfig:
    """Configuration manager for GitHub issue creation settings."""
    
    DEFAULT_CONFIG_FILE = "issue_config.json"
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (optional)
        """
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config_path = Path(__file__).parent / self.config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            if not self.config_path.exists():
                print(f"⚠️  Configuration file {self.config_file} not found, using defaults")
                return self._get_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate and merge with defaults
            return self._validate_config(config)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing configuration file: {e}")
            print("Using default configuration")
            return self._get_default_config()
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "issue_settings": {
                "default_project": "OPL Management",
                "project_number": 23,
                "labels": [
                    {
                        "name": "security-Vulnerability",
                        "color": "fbca04",
                        "description": "Security vulnerability that needs to be addressed"
                    }
                ],
                "title_format": "{repository} - Fix all dependabot issues Critical - {critical:02d}, High - {high:02d}, Medium - {medium:02d}, Low - {low:02d}",
                "auto_assign_project": True,
                "include_timestamp": False,
                "force_update_existing": False
            },
            "github_settings": {
                "organization": "MiDAS",
                "base_url": "https://github.boschdevcloud.com"
            },
            "severity_settings": {
                "minimum_severity": "low",
                "severity_order": ["critical", "high", "medium", "low"],
                "severity_colors": {
                    "critical": "d73a4a",
                    "high": "ff6b6b", 
                    "medium": "fbca04",
                    "low": "28a745"
                }
            },
            "report_settings": {
                "default_reports_directory": "reports",
                "supported_formats": ["csv", "json"],
                "auto_detect_latest": True
            },
            "advanced_settings": {
                "batch_size": 10,
                "api_timeout": 30,
                "retry_attempts": 3,
                "enable_debug_logging": False
            }
        }
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration and merge with defaults."""
        default_config = self._get_default_config()
        
        # Deep merge configuration
        merged_config = self._deep_merge(default_config, config)
        
        # Validate specific settings
        if "issue_settings" in merged_config:
            issue_settings = merged_config["issue_settings"]
            
            # Validate labels
            if "labels" in issue_settings:
                for label in issue_settings["labels"]:
                    if not isinstance(label, dict) or "name" not in label:
                        print("⚠️  Invalid label configuration, using defaults")
                        issue_settings["labels"] = default_config["issue_settings"]["labels"]
                        break
                    
                    # Ensure color doesn't have # prefix
                    if "color" in label and label["color"].startswith("#"):
                        label["color"] = label["color"][1:]
            
            # Validate project number
            if "project_number" in issue_settings:
                try:
                    issue_settings["project_number"] = int(issue_settings["project_number"])
                except (ValueError, TypeError):
                    print("⚠️  Invalid project_number, using default")
                    issue_settings["project_number"] = 23
        
        return merged_config
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    # Property accessors for easy access to configuration values
    
    @property
    def default_project(self) -> str:
        """Get default project name."""
        return self.config.get("issue_settings", {}).get("default_project", "OPL Management")
    
    @property
    def project_number(self) -> int:
        """Get project number."""
        return self.config.get("issue_settings", {}).get("project_number", 23)
    
    @property
    def labels(self) -> List[Dict[str, str]]:
        """Get label configurations."""
        return self.config.get("issue_settings", {}).get("labels", [])
    
    @property
    def title_format(self) -> str:
        """Get issue title format."""
        return self.config.get("issue_settings", {}).get("title_format", 
            "{repository} - Fix all dependabot issues Critical - {critical:02d}, High - {high:02d}, Medium - {medium:02d}, Low - {low:02d}")
    
    @property
    def auto_assign_project(self) -> bool:
        """Get auto assign project setting."""
        return self.config.get("issue_settings", {}).get("auto_assign_project", True)
    
    @property
    def include_timestamp(self) -> bool:
        """Get include timestamp setting."""
        return self.config.get("issue_settings", {}).get("include_timestamp", False)
    
    @property
    def organization(self) -> str:
        """Get GitHub organization."""
        return self.config.get("github_settings", {}).get("organization", "MiDAS")
    
    @property
    def base_url(self) -> str:
        """Get GitHub base URL."""
        return self.config.get("github_settings", {}).get("base_url", "https://github.boschdevcloud.com")
    
    @property
    def severity_order(self) -> List[str]:
        """Get severity order."""
        return self.config.get("severity_settings", {}).get("severity_order", ["critical", "high", "medium", "low"])
    
    @property
    def severity_colors(self) -> Dict[str, str]:
        """Get severity colors."""
        return self.config.get("severity_settings", {}).get("severity_colors", {})
    
    @property
    def reports_directory(self) -> str:
        """Get default reports directory."""
        return self.config.get("report_settings", {}).get("default_reports_directory", "reports")
    
    @property
    def api_timeout(self) -> int:
        """Get API timeout."""
        return self.config.get("advanced_settings", {}).get("api_timeout", 30)
    
    @property
    def enable_debug_logging(self) -> bool:
        """Get debug logging setting."""
        return self.config.get("advanced_settings", {}).get("enable_debug_logging", False)
    
    def get_label_names(self) -> List[str]:
        """Get list of label names."""
        return [label["name"] for label in self.labels]
    
    def get_label_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """Get label configuration by name."""
        for label in self.labels:
            if label["name"] == name:
                return label
        return None
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def update_setting(self, section: str, key: str, value: Any) -> bool:
        """
        Update a configuration setting.
        
        Args:
            section: Configuration section (e.g., 'issue_settings')
            key: Setting key
            value: New value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section][key] = value
            return True
        except Exception as e:
            print(f"❌ Error updating setting {section}.{key}: {e}")
            return False
    
    def print_config_summary(self):
        """Print a summary of current configuration."""
        print("🔧 Current Issue Configuration")
        print("=" * 50)
        print(f"📋 Default Project: {self.default_project}")
        print(f"🔢 Project Number: {self.project_number}")
        print(f"🏢 Organization: {self.organization}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🏷️  Labels:")
        for label in self.labels:
            print(f"   - {label['name']} (#{label['color']})")
        print(f"🎯 Auto-assign Project: {self.auto_assign_project}")
        print(f"⏰ Include Timestamp: {self.include_timestamp}")
        print(f"📁 Reports Directory: {self.reports_directory}")
        print("=" * 50)

def main():
    """Test configuration loading."""
    config = IssueConfig()
    config.print_config_summary()

if __name__ == "__main__":
    main()