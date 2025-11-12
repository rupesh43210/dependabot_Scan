#!/usr/bin/env python3
"""
Code Scanning Pipeline

Orchestrates end-to-end code scanning workflow including scanning,
report generation, and cleanup.

Author: GitHub Copilot
Version: 1.1.0 (Optimized)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# Add parent directory to path for module imports
sys.path.insert(0, str(Path(__file__).parent))

# Import modular components
from scanners.code_scanning_scanner import CodeScanningScanner
from reporters.code_scanning_report_generator import CodeScanningReportGenerator
from utils.config_loader import load_config, validate_config, get_active_scope, get_scope_repositories
from utils.logger import setup_logger

# Load environment variables from .env file (in project root)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path if env_path.exists() else None)


class CodeScanningPipeline:
    """
    Main pipeline orchestrating the code scanning workflow.
    
    Features:
    - Repository scope management
    - Automated scanning
    - Report generation
    - Temporary file cleanup
    """
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize the code scanning pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        # If relative path, make it relative to project root (parent of src/)
        if not os.path.isabs(config_path):
            project_root = os.path.dirname(os.path.dirname(__file__))
            self.config_path = os.path.join(project_root, config_path)
        else:
            self.config_path = config_path
        self.config = self._load_config()
        self.scanner = None
        self.report_generator = None
        self.temp_files = []
        self.reports_directory = None
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from: {self.config_path}")
            return config
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _validate_config(self) -> bool:
        """Validate required configuration parameters."""
        # Check for environment variables (primary method)
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("❌ Error: GITHUB_TOKEN environment variable not set")
            print("💡 Please set it in your .env file or environment")
            return False
        
        # Validate scopes exist
        if 'scopes' not in self.config or not self.config['scopes']:
            print("⚠️  No scopes defined in configuration")
            return False
        
        return True
    
    def _get_scope_info(self, scope_name: str) -> Optional[Dict]:
        """Get scope configuration by name."""
        # Support both dict format {"scope_name": [...]} and array format [{"name": "...", "repositories": [...]}]
        if isinstance(self.config['scopes'], dict):
            if scope_name in self.config['scopes']:
                return {'name': scope_name, 'repositories': self.config['scopes'][scope_name]}
            return None
        else:
            for scope in self.config['scopes']:
                if scope['name'] == scope_name:
                    return scope
            return None
    
    def _display_available_scopes(self):
        """Display all available scopes."""
        print("\n📋 Available Scopes:")
        print("-" * 60)
        
        # Support both dict format and array format
        if isinstance(self.config['scopes'], dict):
            for idx, (scope_name, repos) in enumerate(self.config['scopes'].items(), 1):
                print(f"{idx}. {scope_name}")
                print(f"   Repositories: {len(repos)}")
                print()
        else:
            for idx, scope in enumerate(self.config['scopes'], 1):
                print(f"{idx}. {scope['name']}")
                print(f"   Description: {scope.get('description', 'N/A')}")
            print(f"   Repositories: {len(scope['repositories'])}")
            print()
    
    def select_scope(self, scope_name: Optional[str] = None) -> Tuple[str, List[str]]:
        """
        Select a scope for scanning.
        
        Args:
            scope_name: Optional scope name. If not provided, will prompt user.
                       Use "scoped" to automatically use the active_scope from config.
            
        Returns:
            Tuple of (scope_name, list of repositories)
        """
        # If "scoped" is provided, use active_scope from config
        if scope_name and scope_name.lower() == "scoped":
            if 'scan' in self.config and 'active_scope' in self.config['scan']:
                scope_name = self.config['scan']['active_scope']
                print(f"ℹ️  Using active scope from config: {scope_name}")
            else:
                print("❌ No active_scope defined in config.json")
                self._display_available_scopes()
                sys.exit(1)
        
        if scope_name:
            scope = self._get_scope_info(scope_name)
            if not scope:
                print(f"❌ Scope '{scope_name}' not found in configuration")
                self._display_available_scopes()
                sys.exit(1)
        else:
            self._display_available_scopes()
            print("Enter scope name to scan (or 'all' for all repositories):")
            scope_name = input("Scope: ").strip()
            
            if scope_name.lower() == 'all':
                all_repos = []
                if isinstance(self.config['scopes'], dict):
                    for repos in self.config['scopes'].values():
                        all_repos.extend(repos)
                else:
                    for scope in self.config['scopes']:
                        all_repos.extend(scope['repositories'])
                return "All Repositories", list(set(all_repos))
            
            scope = self._get_scope_info(scope_name)
            if not scope:
                print(f"❌ Invalid scope: {scope_name}")
                sys.exit(1)
        
        return scope_name, scope['repositories']
    
    def run_scan(self, scope_name: str, repositories: List[str]) -> Tuple[str, str, str]:
        """
        Execute code scanning for specified repositories.
        
        Args:
            scope_name: Name of the scope being scanned
            repositories: List of repository names to scan
            
        Returns:
            Tuple of (json_file, csv_file, metadata_file) paths
        """
        print(f"\n{'='*60}")
        print(f"🔍 CODE SCANNING SCAN")
        print(f"Scope: {scope_name}")
        print(f"Repositories: {len(repositories)}")
        print(f"{'='*60}\n")
        
        # Initialize scanner using environment variables
        github_token = os.getenv('GITHUB_TOKEN')
        base_url = os.getenv('GITHUB_ENTERPRISE_URL', 'https://github.boschdevcloud.com')
        org_name = os.getenv('GITHUB_ORG', 'BGSW')
        
        self.scanner = CodeScanningScanner(
            github_token=github_token,
            base_url=base_url
        )
        
        # Scan repositories
        all_alerts = []
        
        for i, repo in enumerate(repositories, 1):
            print(f"[{i}/{len(repositories)}] Processing {repo}...")
            alerts = self.scanner.get_repository_code_scanning_alerts(org_name, repo)
            
            if alerts:
                print(f"✅ Found {len(alerts)} Code Scanning alert(s)")
            else:
                print(f"⚠️  No Code Scanning alerts found")
            
            all_alerts.extend(alerts)
        
        # Print scan summary
        print(f"\n{'='*60}")
        print(f"📊 SCAN SUMMARY")
        print(f"{'='*60}")
        print(f"Total repositories scanned: {len(repositories)}")
        print(f"Total Code Scanning alerts found: {len(all_alerts)}")
        
        # Count by state
        open_count = sum(1 for a in all_alerts if a.get('alert_state') == 'open')
        fixed_count = sum(1 for a in all_alerts if a.get('alert_state') == 'fixed')
        dismissed_count = sum(1 for a in all_alerts if a.get('alert_state') == 'dismissed')
        
        print(f"  • Open alerts: {open_count}")
        print(f"  • Fixed alerts: {fixed_count}")
        print(f"  • Dismissed alerts: {dismissed_count}")
        print(f"{'='*60}\n")
        
        # Save results with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file, csv_file, metadata_file = self.scanner.save_results(all_alerts, timestamp=timestamp)
        
        # Track temp files for cleanup
        self.temp_files.extend([json_file, csv_file, metadata_file])
        
        return json_file, csv_file, metadata_file
    
    def generate_reports(self, data_file: str, metadata_file: str, scope_name: str, repositories: List[str]):
        """
        Generate comprehensive reports.
        
        Args:
            data_file: Path to data file (JSON or CSV)
            metadata_file: Path to repository metadata file
            scope_name: Name of the scope
            repositories: List of scoped repositories
        """
        print(f"\n{'='*60}")
        print(f"📊 GENERATING REPORTS")
        print(f"{'='*60}\n")
        
        # Initialize report generator
        self.report_generator = CodeScanningReportGenerator(
            scoped_repositories=repositories,
            active_scope=scope_name
        )
        
        # Load metadata
        self.report_generator.load_repository_metadata(metadata_file)
        
        # Load data
        if not self.report_generator.load_alert_data(data_file):
            print("❌ Failed to load alert data")
            return
        
        # Generate reports
        repo_summary = self.report_generator.generate_repository_executive_summary()
        detailed = self.report_generator.generate_detailed_report()
        
        # Save reports
        self.reports_directory = self.report_generator.save_reports(repo_summary, detailed)
        
        if self.reports_directory:
            print(f"\n✅ Reports saved to: {self.reports_directory}")
    
    def cleanup_temp_files(self):
        """Remove temporary files."""
        if not self.temp_files:
            return
        
        print(f"\n🧹 Cleaning up {len(self.temp_files)} temporary files...")
        
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"✅ Removed: {temp_file}")
            except Exception as e:
                print(f"⚠️  Could not remove {temp_file}: {e}")
        
        self.temp_files = []
        print("✅ Cleanup complete")
    
    def run(self, scope_name: Optional[str] = None, skip_cleanup: bool = False):
        """
        Execute the complete code scanning pipeline.
        
        Args:
            scope_name: Optional scope name. If not provided, will prompt user.
            skip_cleanup: If True, keep temporary files
        """
        start_time = datetime.now()
        
        print("\n" + "="*60)
        print("🛡️  CODE SCANNING SECURITY PIPELINE")
        print("="*60)
        
        # Validate configuration
        if not self._validate_config():
            print("❌ Configuration validation failed")
            sys.exit(1)
        
        # Select scope
        scope_name, repositories = self.select_scope(scope_name)
        
        if not repositories:
            print("❌ No repositories found in scope")
            sys.exit(1)
        
        try:
            # Run scan
            json_file, csv_file, metadata_file = self.run_scan(scope_name, repositories)
            
            # Generate reports
            self.generate_reports(json_file, metadata_file, scope_name, repositories)
            
            # Cleanup
            if not skip_cleanup:
                self.cleanup_temp_files()
            else:
                print(f"\nℹ️  Temporary files kept: {self.temp_files}")
            
            # Summary
            duration = datetime.now() - start_time
            print(f"\n{'='*60}")
            print(f"✅ PIPELINE COMPLETED SUCCESSFULLY")
            print(f"Duration: {duration}")
            if self.reports_directory:
                print(f"Reports: {self.reports_directory}")
            print(f"{'='*60}\n")
            
        except KeyboardInterrupt:
            print("\n⚠️  Pipeline interrupted by user")
            if not skip_cleanup:
                self.cleanup_temp_files()
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            if not skip_cleanup:
                self.cleanup_temp_files()
            sys.exit(1)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Code Scanning Security Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--scope',
        type=str,
        help='Name of the scope to scan (if not provided, will prompt)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file (default: config/config.json)'
    )
    
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary files (do not cleanup)'
    )
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = CodeScanningPipeline(config_path=args.config)
    pipeline.run(scope_name=args.scope, skip_cleanup=args.keep_temp)


if __name__ == "__main__":
    main()
