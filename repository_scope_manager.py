#!/usr/bin/env python3
"""
Repository Scope Manager

Manages repository scoping configurations for targeted vulnerability scanning.
Allows defining different scopes of repositories for different scan scenarios.

Author: GitHub Copilot
Version: 1.0.0
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class RepositoryScopeManager:
    """
    Manages repository scoping configurations for selective scanning.
    
    Features:
    - Predefined scopes (critical, frontend, backend, etc.)
    - Custom scope definitions
    - Dynamic scope switching
    - Validation and error handling
    """
    
    def __init__(self, config_file: str = "repo_scopes.json"):
        """
        Initialize the scope manager.
        
        Args:
            config_file: Path to the scope configuration file
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load scope configuration from file."""
        if not self.config_file.exists():
            print(f"⚠️  Scope configuration file not found: {self.config_file}")
            print("   Creating default configuration...")
            self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"❌ Error loading scope configuration: {e}")
            print("   Creating default configuration...")
            self._create_default_config()
            return self._load_config()
    
    def _create_default_config(self):
        """Create a default scope configuration file."""
        default_config = {
            "scopes": {
                "critical": {
                    "description": "Critical production repositories",
                    "repositories": []
                },
                "frontend": {
                    "description": "Frontend applications",
                    "repositories": []
                },
                "backend": {
                    "description": "Backend services and APIs",
                    "repositories": []
                },
                "infrastructure": {
                    "description": "Infrastructure and DevOps repositories",
                    "repositories": []
                },
                "custom": {
                    "description": "Custom scope for specific releases",
                    "repositories": []
                }
            },
            "default_scope": "all",
            "active_scope": "all"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    def get_available_scopes(self) -> List[str]:
        """Get list of available scope names."""
        scopes = list(self.config.get("scopes", {}).keys())
        scopes.append("all")  # Always include 'all' scope
        return scopes
    
    def get_scope_description(self, scope_name: str) -> str:
        """Get description for a specific scope."""
        if scope_name == "all":
            return "All repositories in the organization"
        
        scopes = self.config.get("scopes", {})
        if scope_name in scopes:
            return scopes[scope_name].get("description", "No description available")
        
        return "Unknown scope"
    
    def get_repositories_for_scope(self, scope_name: str) -> Optional[List[str]]:
        """
        Get list of repositories for a specific scope.
        
        Args:
            scope_name: Name of the scope
            
        Returns:
            List of repository names, or None if scope should scan all repos
        """
        if scope_name == "all":
            return None  # None means scan all repositories
        
        scopes = self.config.get("scopes", {})
        if scope_name not in scopes:
            print(f"❌ Unknown scope: {scope_name}")
            print(f"   Available scopes: {', '.join(self.get_available_scopes())}")
            return None
        
        repositories = scopes[scope_name].get("repositories", [])
        if not repositories:
            print(f"⚠️  Scope '{scope_name}' has no repositories defined")
            return []
        
        return repositories
    
    def set_active_scope(self, scope_name: str) -> bool:
        """
        Set the active scope in the configuration.
        
        Args:
            scope_name: Name of the scope to activate
            
        Returns:
            True if scope was set successfully
        """
        available_scopes = self.get_available_scopes()
        if scope_name not in available_scopes:
            print(f"❌ Invalid scope: {scope_name}")
            print(f"   Available scopes: {', '.join(available_scopes)}")
            return False
        
        self.config["active_scope"] = scope_name
        self._save_config()
        return True
    
    def get_active_scope(self) -> str:
        """Get the currently active scope."""
        return self.config.get("active_scope", "all")
    
    def add_repository_to_scope(self, scope_name: str, repo_name: str) -> bool:
        """
        Add a repository to a specific scope.
        
        Args:
            scope_name: Name of the scope
            repo_name: Name of the repository to add
            
        Returns:
            True if repository was added successfully
        """
        if scope_name == "all":
            print("❌ Cannot add repositories to 'all' scope")
            return False
        
        scopes = self.config.get("scopes", {})
        if scope_name not in scopes:
            print(f"❌ Unknown scope: {scope_name}")
            return False
        
        repositories = scopes[scope_name].get("repositories", [])
        if repo_name not in repositories:
            repositories.append(repo_name)
            scopes[scope_name]["repositories"] = repositories
            self._save_config()
            print(f"✅ Added '{repo_name}' to scope '{scope_name}'")
            return True
        else:
            print(f"⚠️  Repository '{repo_name}' already in scope '{scope_name}'")
            return False
    
    def remove_repository_from_scope(self, scope_name: str, repo_name: str) -> bool:
        """
        Remove a repository from a specific scope.
        
        Args:
            scope_name: Name of the scope
            repo_name: Name of the repository to remove
            
        Returns:
            True if repository was removed successfully
        """
        if scope_name == "all":
            print("❌ Cannot remove repositories from 'all' scope")
            return False
        
        scopes = self.config.get("scopes", {})
        if scope_name not in scopes:
            print(f"❌ Unknown scope: {scope_name}")
            return False
        
        repositories = scopes[scope_name].get("repositories", [])
        if repo_name in repositories:
            repositories.remove(repo_name)
            scopes[scope_name]["repositories"] = repositories
            self._save_config()
            print(f"✅ Removed '{repo_name}' from scope '{scope_name}'")
            return True
        else:
            print(f"⚠️  Repository '{repo_name}' not found in scope '{scope_name}'")
            return False
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving scope configuration: {e}")
    
    def print_scope_info(self, scope_name: str = None):
        """Print information about scopes."""
        if scope_name:
            # Print specific scope info
            if scope_name == "all":
                print(f"📋 Scope: {scope_name}")
                print(f"   Description: {self.get_scope_description(scope_name)}")
                print(f"   Repositories: All repositories in the organization")
            else:
                repositories = self.get_repositories_for_scope(scope_name)
                print(f"📋 Scope: {scope_name}")
                print(f"   Description: {self.get_scope_description(scope_name)}")
                if repositories:
                    print(f"   Repositories ({len(repositories)}): {', '.join(repositories)}")
                else:
                    print(f"   Repositories: None defined")
        else:
            # Print all scopes
            print("📋 Available Repository Scopes:")
            print("=" * 50)
            
            active_scope = self.get_active_scope()
            
            for scope in self.get_available_scopes():
                status = " (ACTIVE)" if scope == active_scope else ""
                print(f"\n🎯 {scope}{status}")
                print(f"   Description: {self.get_scope_description(scope)}")
                
                if scope != "all":
                    repositories = self.get_repositories_for_scope(scope)
                    if repositories:
                        print(f"   Repositories ({len(repositories)}): {', '.join(repositories)}")
                    else:
                        print(f"   Repositories: None defined")
                else:
                    print(f"   Repositories: All repositories in the organization")