#!/usr/bin/env python3
"""
Configuration and Utilities for MiDAS Security Pipeline

Contains configuration settings, constants, and utility functions
used across the security assessment pipeline.

Author: GitHub Copilot
Version: 2.0.0
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration settings for the security pipeline."""
    
    # GitHub Enterprise settings
    GITHUB_BASE_URL = "https://github.boschdevcloud.com"
    DEFAULT_ORG = "MiDAS"
    
    # API settings
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 1
    
    # Report settings
    REPORTS_DIR = "reports"
    MAX_DESCRIPTION_LENGTH = 10000
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Risk scoring weights
    SEVERITY_WEIGHTS = {
        'CRITICAL': 50,
        'HIGH': 20,
        'MEDIUM': 5,
        'LOW': 1
    }
    
    # Excel formatting colors
    SEVERITY_COLORS = {
        'CRITICAL': {'bg': 'FF0000', 'font': 'FFFFFF'},  # Red
        'HIGH': {'bg': 'FF8C00', 'font': 'FFFFFF'},      # Orange
        'MEDIUM': {'bg': 'FFD700', 'font': '000000'},    # Yellow
        'LOW': {'bg': '90EE90', 'font': '000000'}        # Light Green
    }
    
    # CVSS score defaults for missing values
    CVSS_DEFAULTS = {
        'critical': 9.0,
        'high': 7.0,
        'medium': 5.0,
        'low': 3.0
    }


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_environment() -> Dict[str, Any]:
    """
    Validate environment setup and return configuration.
    
    Returns:
        Dictionary with validated configuration
        
    Raises:
        ValidationError: If environment is not properly configured
    """
    config = {}
    
    # Check for required environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValidationError(
            "GITHUB_TOKEN environment variable not set. "
            "Please set your GitHub Enterprise token in the .env file"
        )
    
    config['github_token'] = github_token
    config['org_name'] = os.getenv('GITHUB_ORG', Config.DEFAULT_ORG)
    config['base_url'] = os.getenv('GITHUB_BASE_URL', Config.GITHUB_BASE_URL)
    
    # Validate token format (basic check)
    if len(github_token) < 20:
        raise ValidationError("GitHub token appears to be invalid (too short)")
    
    # Check Python version
    if sys.version_info < (3, 8):
        raise ValidationError("Python 3.8 or higher is required")
    
    # Check required packages
    required_packages = ['requests', 'pandas', 'github', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        raise ValidationError(
            f"Missing required packages: {', '.join(missing_packages)}. "
            "Please run: pip install -r requirements.txt"
        )
    
    return config


def setup_logging(level: str = "INFO") -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    import logging
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    log_file = logs_dir / f"midas_security_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for cross-platform compatibility.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove/replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
    filename = filename.strip('.')  # Remove leading/trailing dots
    
    # Ensure filename is not too long
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename


def create_directory_structure(base_dir: str) -> Dict[str, Path]:
    """
    Create standardized directory structure for reports.
    
    Args:
        base_dir: Base directory path
        
    Returns:
        Dictionary mapping directory names to Path objects
    """
    base_path = Path(base_dir)
    
    directories = {
        'reports': base_path / 'reports',
        'logs': base_path / 'logs',
        'temp': base_path / 'temp',
        'archives': base_path / 'archives'
    }
    
    # Create all directories
    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return directories


def cleanup_old_files(directory: Path, days_old: int = 30) -> int:
    """
    Clean up files older than specified days.
    
    Args:
        directory: Directory to clean
        days_old: Number of days after which files are considered old
        
    Returns:
        Number of files cleaned up
    """
    import time
    
    if not directory.exists():
        return 0
    
    current_time = time.time()
    cutoff_time = current_time - (days_old * 24 * 60 * 60)
    
    cleaned_count = 0
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                cleaned_count += 1
            except Exception:
                pass  # Skip files that can't be deleted
    
    return cleaned_count


def get_system_info() -> Dict[str, str]:
    """
    Get system information for debugging and logging.
    
    Returns:
        Dictionary with system information
    """
    import platform
    import pkg_resources
    
    info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'hostname': platform.node()
    }
    
    # Get package versions
    try:
        key_packages = ['pandas', 'requests', 'github', 'openpyxl']
        for package in key_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                info[f'{package}_version'] = version
            except:
                info[f'{package}_version'] = 'Not installed'
    except:
        pass
    
    return info


def check_disk_space(path: str, required_gb: float = 1.0) -> bool:
    """
    Check if there's enough disk space available.
    
    Args:
        path: Path to check
        required_gb: Required space in GB
        
    Returns:
        True if enough space is available
    """
    import shutil
    
    try:
        total, used, free = shutil.disk_usage(path)
        free_gb = free / (1024**3)  # Convert to GB
        return free_gb >= required_gb
    except:
        return True  # If we can't check, assume it's fine


def export_to_json(data: Any, filename: str, indent: int = 2) -> bool:
    """
    Export data to JSON file with error handling.
    
    Args:
        data: Data to export
        filename: Output filename
        indent: JSON indentation
        
    Returns:
        True if export successful
    """
    import json
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return False


def load_from_json(filename: str) -> Optional[Any]:
    """
    Load data from JSON file with error handling.
    
    Args:
        filename: Input filename
        
    Returns:
        Loaded data or None if error
    """
    import json
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading from JSON: {e}")
        return None


# Import datetime for use in logging setup
from datetime import datetime