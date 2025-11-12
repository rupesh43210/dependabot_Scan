"""
Configuration loader and validator.
Handles loading and validating config.json settings.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary containing configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    # If relative path, make it relative to project root
    if not Path(config_path).is_absolute():
        # Get project root (2 levels up from utils/)
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / config_path
    else:
        config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\n"
            "Please create config/config.json from config/config.json.sample"
        )
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure and required fields.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Check required top-level keys
    required_keys = ['scan', 'scopes']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate scan configuration
    scan_config = config['scan']
    if 'output_dir' not in scan_config:
        raise ValueError("Missing 'output_dir' in scan configuration")
    
    # Validate scopes
    scopes = config['scopes']
    if not scopes:
        raise ValueError("No scopes defined in configuration")
    
    # Check if scopes is dict (new format) or list (legacy)
    if isinstance(scopes, dict):
        for scope_name, repos in scopes.items():
            if not isinstance(repos, list):
                raise ValueError(f"Scope '{scope_name}' must contain a list of repositories")
    elif not isinstance(scopes, list):
        raise ValueError("Scopes must be either a dictionary or list")
    
    return True


def get_scope_repositories(config: Dict[str, Any], scope_name: str) -> list:
    """
    Get list of repositories for a given scope.
    
    Args:
        config: Configuration dictionary
        scope_name: Name of scope to retrieve
        
    Returns:
        List of repository names
        
    Raises:
        ValueError: If scope not found
    """
    scopes = config['scopes']
    
    # Handle dict format (new)
    if isinstance(scopes, dict):
        if scope_name not in scopes:
            raise ValueError(f"Scope '{scope_name}' not found in configuration")
        return scopes[scope_name]
    
    # Handle list format (legacy)
    elif isinstance(scopes, list):
        for scope in scopes:
            if scope.get('name') == scope_name:
                return scope.get('repositories', [])
        raise ValueError(f"Scope '{scope_name}' not found in configuration")
    
    raise ValueError("Invalid scopes format in configuration")


def get_active_scope(config: Dict[str, Any]) -> Optional[str]:
    """
    Get the active scope name from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Active scope name or None
    """
    return config.get('scan', {}).get('active_scope')


def get_output_directory(config: Dict[str, Any], scanner_type: str = 'dependabot') -> str:
    """
    Get output directory for a specific scanner type.
    
    Args:
        config: Configuration dictionary
        scanner_type: Type of scanner ('dependabot' or 'codeql')
        
    Returns:
        Output directory path
    """
    scan_config = config.get('scan', {})
    
    if scanner_type == 'dependabot':
        return scan_config.get('dependabot_output_dir', './reports/dependabot_alerts')
    elif scanner_type == 'codeql':
        return scan_config.get('codeql_output_dir', './reports/codeql_alerts')
    else:
        return scan_config.get('output_dir', './reports')
