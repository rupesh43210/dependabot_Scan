#!/usr/bin/env python3
"""
GitHub Issue Creator for Security Vulnerabilities

A standalone tool for creating GitHub issues based on vulnerability scan results.
This tool can be run independently after a vulnerability scan to create issues
for repositories with security vulnerabilities.

Features:
- Standalone operation (separate from security pipeline)
- Duplicate issue detection and prevention
- Flexible label management with automatic label creation
- Customizable project assignment
- Detailed vulnerability reporting in issues

Author: GitHub Copilot
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Check if virtual environment is activated, if not create and activate it
def ensure_venv():
    """Ensure virtual environment is activated, create if it doesn't exist."""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Not in virtual environment
        venv_path = Path(__file__).parent / "venv"
        
        if not venv_path.exists():
            print("📦 Virtual environment not found. Creating new venv...")
            try:
                # Create virtual environment
                subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
                print("✅ Virtual environment created successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create virtual environment: {e}")
                print("   Please ensure Python venv module is available")
                return False
        
        # Activate virtual environment
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux
            activate_script = venv_path / "bin" / "python"
            
        if activate_script.exists():
            print("🔄 Activating virtual environment...")
            
            # Check if requirements need to be installed
            requirements_file = Path(__file__).parent / "requirements.txt"
            if requirements_file.exists():
                # Check if dependencies are already installed
                try:
                    result = subprocess.run([
                        str(activate_script), "-c", 
                        "import requests, pandas, github, openpyxl; print('Dependencies OK')"
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode != 0:
                        print("📋 Installing/updating dependencies...")
                        subprocess.run([
                            str(activate_script), "-m", "pip", "install", "-r", str(requirements_file)
                        ], check=True, capture_output=True, text=True)
                        print("✅ Dependencies installed successfully")
                    else:
                        print("✅ Dependencies already satisfied")
                        
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                    print("📋 Installing/updating dependencies...")
                    try:
                        subprocess.run([
                            str(activate_script), "-m", "pip", "install", "-r", str(requirements_file)
                        ], check=True, capture_output=True, text=True)
                        print("✅ Dependencies installed successfully")
                    except subprocess.CalledProcessError as install_error:
                        print(f"❌ Failed to install dependencies: {install_error}")
                        print("   You may need to install them manually")
            
            # Restart script with virtual environment
            print("🚀 Restarting script with virtual environment...")
            subprocess.run([str(activate_script), __file__] + sys.argv[1:])
            sys.exit(0)
        else:
            print("❌ Failed to find Python executable in virtual environment")
            return False
    
    return True

# Ensure venv is activated
ensure_venv()

import pandas as pd

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from github_issue_manager import GitHubIssueManager


class StandaloneIssueCreator:
    """
    Standalone tool for creating GitHub issues from vulnerability scan results.
    """
    
    def __init__(self, github_token: str, config: dict = None):
        """
        Initialize the standalone issue creator.
        
        Args:
            github_token: GitHub personal access token
            config: Configuration dictionary (optional)
        """
        self.config = config or {}
        self.github_token = github_token
        
        # Get org and base URL from environment if not in config
        org_name = self.config.get('organization', os.getenv('GITHUB_ORG', 'MiDAS'))
        base_url = self.config.get('base_url', os.getenv('GITHUB_ENTERPRISE_URL'))
        
        # Initialize GitHub Issue Manager with config values
        self.issue_manager = GitHubIssueManager(
            github_token=github_token,
            org_name=org_name,
            base_url=base_url
        )
        
        self.org_name = org_name
        
        self.stats = {
            'scan_files_processed': 0,
            'repositories_analyzed': 0,
            'issues_created': 0,
            'issues_updated': 0,
            'issues_skipped': 0,
            'labels_created': 0,
            'errors': 0
        }
    
    def find_latest_scan_file(self, reports_dir: str = "reports") -> Optional[str]:
        """
        Find the latest vulnerability scan file.
        
        Args:
            reports_dir: Directory to search for reports
            
        Returns:
            Path to the latest vulnerability file or None
        """
        reports_path = Path(reports_dir)
        if not reports_path.exists():
            return None
        
        # Look for the most recent report directory
        report_dirs = [d for d in reports_path.iterdir() if d.is_dir() and d.name.startswith('security_reports_')]
        
        if not report_dirs:
            return None
        
        # Sort by creation time (newest first)
        report_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        latest_dir = report_dirs[0]
        
        # Look for vulnerability files in the latest directory
        vuln_files = list(latest_dir.glob('detailed_vulnerabilities.csv'))
        if vuln_files:
            return str(vuln_files[0])
        
        # Fallback: look for any CSV files with vulnerability data
        csv_files = list(latest_dir.glob('*.csv'))
        for csv_file in csv_files:
            if 'vulnerabilities' in csv_file.name.lower():
                return str(csv_file)
        
        return None
    
    def load_vulnerability_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Load vulnerability data from file.
        
        Args:
            file_path: Path to vulnerability data file (CSV or JSON)
            
        Returns:
            DataFrame with vulnerability data or None if failed
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                return None
            
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                print(f"❌ Unsupported file format: {file_path.suffix}")
                return None
            
            if df.empty:
                print("⚠️  No data found in file")
                return None
            
            # Normalize column names for compatibility
            column_mapping = {
                'Repository Name': 'repository',
                'Status': 'alert_state', 
                'Severity': 'severity',
                'Component': 'package_name',
                'Vulnerability Title': 'advisory_summary',
                'CVSS Score': 'cvss_score',
                'CVE ID': 'cve_id',
                'Description': 'description'
            }
            
            # Rename columns if they exist
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # Convert status values to lowercase for consistency  
            if 'alert_state' in df.columns:
                df['alert_state'] = df['alert_state'].str.lower()
                # Map CSV status values to expected values
                status_mapping = {
                    'open': 'open',
                    'fixed': 'fixed', 
                    'dismissed': 'dismissed',
                    'resolved - fixed': 'fixed',
                    'resolved - dismissed': 'dismissed'
                }
                df['alert_state'] = df['alert_state'].map(lambda x: status_mapping.get(x, x))
            
            print(f"✅ Loaded {len(df)} vulnerability records from {file_path.name}")
            self.stats['scan_files_processed'] += 1
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading file {file_path}: {e}")
            self.stats['errors'] += 1
            return None
    
    def ensure_label_exists(self, repo: Any, label_name: str, color: str = None) -> bool:
        """
        Ensure a label exists in the repository, create if it doesn't.
        
        Args:
            repo: GitHub repository object
            label_name: Name of the label
            color: Color for the label (without #)
            
        Returns:
            True if label exists or was created successfully
        """
        try:
            # Try to get the label (will raise exception if not found)
            repo.get_label(label_name)
            return True
            
        except Exception:
            # Label doesn't exist, create it
            try:
                if color is None:
                    color = 'fbca04'  # Default yellow/orange color for security labels
                else:
                    color = color.lstrip('#')
                
                repo.create_label(
                    name=label_name,
                    color=color,
                    description=f"Security vulnerability tracking"
                )
                
                print(f"  ✅ Created label '{label_name}' with color #{color}")
                self.stats['labels_created'] += 1
                return True
                
            except Exception as e:
                print(f"  ⚠️  Could not create label '{label_name}': {e}")
                return False
    
    def create_issues_for_repositories(self, vulnerability_data: pd.DataFrame,
                                     project_name: str = "OPL Management",
                                     labels: List[str] = None,
                                     label_color: str = None,
                                     force_update: bool = False) -> Dict[str, Any]:
        """
        Create GitHub issues for repositories with vulnerabilities.
        
        Args:
            vulnerability_data: DataFrame with vulnerability data
            project_name: Project to assign issues to
            labels: List of labels to apply to issues
            label_color: Color for custom labels
            force_update: Whether to update existing issues
            
        Returns:
            Dictionary with creation statistics
        """
        print("🔧 Creating GitHub issues for repositories with vulnerabilities...")
        
        # Default labels
        if labels is None:
            labels = ['security', 'vulnerability', 'dependabot', f'project:{project_name}']
        
        # Get repositories with open vulnerabilities
        repos_with_vulns = vulnerability_data[
            vulnerability_data['alert_state'] == 'open'
        ]['repository'].unique()
        
        print(f"   📋 Found {len(repos_with_vulns)} repositories with open vulnerabilities")
        
        if len(repos_with_vulns) == 0:
            print("   ✅ No repositories with open vulnerabilities found")
            return self.stats
        
        # Process each repository
        for repo_name in repos_with_vulns:
            print(f"\n   🔧 Processing {repo_name}...")
            
            try:
                # Get repository object
                repo = self.issue_manager.github_client.get_repo(f"{self.org_name}/{repo_name}")
                
                # Ensure all labels exist
                for label in labels:
                    self.ensure_label_exists(repo, label, label_color)
                
                # Check for existing issues
                existing_issue = self.check_existing_vulnerability_issue(repo_name)
                
                if existing_issue and not force_update:
                    print(f"     ⚠️  Issue already exists: #{existing_issue.number} - {existing_issue.title}")
                    print(f"     ℹ️  Use --force-update to update existing issues")
                    self.stats['issues_skipped'] += 1
                    continue
                
                # Analyze vulnerabilities for this repository
                severity_counts = self.issue_manager.analyze_repository_vulnerabilities(
                    vulnerability_data, repo_name
                )
                
                if severity_counts['total'] == 0:
                    print(f"     ℹ️  No open vulnerabilities found for {repo_name}")
                    continue
                
                # Create or update issue
                if existing_issue and force_update:
                    success = self.update_existing_issue(
                        existing_issue, repo_name, severity_counts, vulnerability_data, labels
                    )
                    if success:
                        self.stats['issues_updated'] += 1
                else:
                    success = self.create_new_issue(
                        repo, repo_name, severity_counts, vulnerability_data, labels, project_name
                    )
                    if success:
                        self.stats['issues_created'] += 1
                
                if success:
                    self.stats['repositories_analyzed'] += 1
                    
            except Exception as e:
                print(f"     ❌ Error processing {repo_name}: {e}")
                self.stats['errors'] += 1
        
        return self.stats
    
    def check_existing_vulnerability_issue(self, repository_name: str) -> Optional[Any]:
        """
        Check if a vulnerability issue already exists for the repository.
        
        Args:
            repository_name: Name of the repository
            
        Returns:
            Existing issue object or None
        """
        try:
            repo = self.issue_manager.github_client.get_repo(f"{self.org_name}/{repository_name}")
            
            # Search for existing vulnerability issues - try both label formats
            # First try the combined label 'security-Vulnerability'
            try:
                issues = list(repo.get_issues(state='open', labels=['security-Vulnerability']))
            except:
                # Fall back to separate labels if combined label doesn't exist
                issues = list(repo.get_issues(state='open', labels=['security', 'vulnerability']))
            
            for issue in issues:
                # Check if this is a vulnerability issue for this repo
                if (repository_name in issue.title and 
                    any(keyword in issue.title.lower() for keyword in ['dependabot', 'fix all', 'vulnerability', 'security'])):
                    return issue
            
            return None
            
        except Exception as e:
            print(f"     ❌ Error checking existing issues for {repository_name}: {e}")
            return None
    
    def create_new_issue(self, repo: Any, repository_name: str, severity_counts: Dict[str, int],
                        vulnerability_data: pd.DataFrame, labels: List[str], project_name: str) -> bool:
        """
        Create a new GitHub issue for repository vulnerabilities.
        """
        try:
            title = self.issue_manager.format_issue_title(repository_name, severity_counts)
            body = self.issue_manager.format_issue_body(repository_name, severity_counts, vulnerability_data)
            
            # Create the issue
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            
            print(f"     ✅ Created issue #{issue.number}: {title}")
            return True
            
        except Exception as e:
            import traceback
            print(f"     ❌ Error creating issue for {repository_name}")
            print(f"        Error type: {type(e).__name__}")
            print(f"        Error message: {str(e)}")
            traceback.print_exc()
            self.stats['errors'] += 1
            return False
    
    def update_existing_issue(self, issue: Any, repository_name: str, severity_counts: Dict[str, int],
                            vulnerability_data: pd.DataFrame, labels: List[str]) -> bool:
        """
        Update an existing GitHub issue with new vulnerability information.
        """
        try:
            new_title = self.issue_manager.format_issue_title(repository_name, severity_counts)
            new_body = self.issue_manager.format_issue_body(repository_name, severity_counts, vulnerability_data)
            
            # Update the issue
            issue.edit(title=new_title, body=new_body)
            
            # Update labels (add new ones, keep existing ones)
            existing_labels = [label.name for label in issue.labels]
            all_labels = list(set(existing_labels + labels))
            issue.edit(labels=all_labels)
            
            print(f"     ✅ Updated issue #{issue.number}: {new_title}")
            return True
            
        except Exception as e:
            print(f"     ❌ Error updating issue for {repository_name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def print_summary(self):
        """Print a summary of issue creation results."""
        print("\n" + "=" * 70)
        print("📊 GITHUB ISSUE CREATION SUMMARY")
        print("=" * 70)
        print(f"📁 Scan Files Processed: {self.stats['scan_files_processed']}")
        print(f"📄 Repositories Analyzed: {self.stats['repositories_analyzed']}")
        print(f"✅ Issues Created: {self.stats['issues_created']}")
        print(f"📝 Issues Updated: {self.stats['issues_updated']}")
        print(f"⏭️  Issues Skipped: {self.stats['issues_skipped']}")
        print(f"🏷️  Labels Created: {self.stats['labels_created']}")
        
        if self.stats['errors'] > 0:
            print(f"❌ Errors Encountered: {self.stats['errors']}")
        else:
            print("✅ All operations completed successfully")
        
        print("=" * 70)


def main():
    """Main execution function for standalone issue creator."""
    parser = argparse.ArgumentParser(
        description="Standalone GitHub Issue Creator for Security Vulnerabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create issues from latest scan with default settings
  python create_security_issues.py --auto

  # Create issues with custom configuration file
  python create_security_issues.py --auto --config my_config.json

  # Create issues from specific file
  python create_security_issues.py --file reports/latest/detailed_vulnerabilities.csv

  # Override project setting from config
  python create_security_issues.py --auto --project "Custom Project"

  # Override labels from config
  python create_security_issues.py --auto --labels "bug,security,critical"

  # Update existing issues
  python create_security_issues.py --auto --force-update

  # Create issues with custom label color override
  python create_security_issues.py --auto --label-color "#ff0000"
"""
    )
    
    parser.add_argument(
        '--file',
        help='Path to vulnerability data file (CSV or JSON)'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatically find and use the latest scan results'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (default: issue_config.json)'
    )
    
    parser.add_argument(
        '--project',
        help='Project to assign created issues to (overrides config file)'
    )
    
    parser.add_argument(
        '--labels',
        help='Comma-separated list of labels to apply to issues (overrides config file)'
    )
    
    parser.add_argument(
        '--label-color',
        help='Color for custom labels in hex format (overrides config file)'
    )
    
    parser.add_argument(
        '--force-update',
        action='store_true',
        help='Update existing issues instead of skipping them'
    )
    
    parser.add_argument(
        '--reports-dir',
        default='reports',
        help='Directory to search for scan reports (default: reports)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.file and not args.auto:
        print("❌ Error: Must specify either --file or --auto")
        print("Use --help for usage examples")
        sys.exit(1)
    
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub token in the .env file")
        sys.exit(1)
    
    # Load configuration (optional, not required for basic operation)
    config = {}
    
    print("GitHub Issue Creator for Security Vulnerabilities")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Organization: {os.getenv('GITHUB_ORG', 'MiDAS')}")
    
    # Override config with command line arguments where provided
    project_name = args.project or config.get('default_project', 'Security')
    reports_dir = args.reports_dir or config.get('reports_directory', 'reports')
    
    print(f"Project: {project_name}")
    print("=" * 70)
    
    # Initialize issue creator with configuration
    creator = StandaloneIssueCreator(github_token, config)
    
    # Determine input file
    if args.auto:
        print("🔍 Searching for latest scan results...")
        input_file = creator.find_latest_scan_file(reports_dir)
        if not input_file:
            print(f"❌ No scan results found in {reports_dir}")
            print("Please run a vulnerability scan first or specify a file with --file")
            sys.exit(1)
        print(f"📄 Using latest scan: {input_file}")
    else:
        input_file = args.file
        print(f"📄 Using specified file: {input_file}")
    
    # Load vulnerability data
    vulnerability_data = creator.load_vulnerability_data(input_file)
    if vulnerability_data is None:
        print("❌ Failed to load vulnerability data")
        sys.exit(1)
    
    # Determine labels to use
    if args.labels:
        labels = [label.strip() for label in args.labels.split(',') if label.strip()]
    else:
        labels = config.get('labels', ['security-Vulnerability'])
    
    # Determine label color
    label_color = args.label_color
    
    print(f"Labels to apply: {', '.join(labels)}")
    if label_color:
        print(f"Label color: {label_color}")
    
    if args.force_update:
        print("🔄 Force update mode: Will update existing issues")
    
    # Create issues
    try:
        stats = creator.create_issues_for_repositories(
            vulnerability_data=vulnerability_data,
            project_name=project_name,
            labels=labels,
            label_color=label_color,
            force_update=args.force_update
        )
        
        # Print summary
        creator.print_summary()
        
        # Exit with appropriate code
        if stats['errors'] > 0:
            sys.exit(1)
        else:
            print("\n🎉 Issue creation completed successfully!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Issue creation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Issue creation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()