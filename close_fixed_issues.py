#!/usr/bin/env python3
"""
Close Fixed Security Issues

This script automatically closes GitHub issues that have been resolved.
It compares the current vulnerability scan with open security issues and closes
issues for vulnerabilities that have been fixed.

Features:
- Identifies fixed vulnerabilities by comparing current scan with open issues
- Closes issues with appropriate closing comment
- Supports dry-run mode to preview changes
- Works with security-Vulnerability labeled issues

Author: GitHub Copilot
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import csv
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from dotenv import load_dotenv
from github import Github, GithubException

class IssueCloser:
    """Handles closing of resolved security vulnerability issues."""
    
    def __init__(self, github_token: str, org_name: str, dry_run: bool = False):
        """
        Initialize the Issue Closer.
        
        Args:
            github_token: GitHub personal access token
            org_name: GitHub organization name
            dry_run: If True, only preview changes without closing issues
        """
        self.github_token = github_token
        self.org_name = org_name
        self.dry_run = dry_run
        
        # Initialize GitHub client
        if os.getenv('GITHUB_ENTERPRISE_URL'):
            base_url = f"{os.getenv('GITHUB_ENTERPRISE_URL')}/api/v3"
            self.github = Github(base_url=base_url, login_or_token=github_token)
        else:
            self.github = Github(github_token)
        
        self.org = self.github.get_organization(org_name)
        
        # Statistics
        self.stats = {
            'repos_checked': 0,
            'open_issues_found': 0,
            'issues_closed': 0,
            'issues_skipped': 0,
            'errors': 0
        }
    
    def get_current_vulnerabilities(self, report_file: Path) -> Dict[str, Set[str]]:
        """
        Load current vulnerabilities from the latest scan report.
        
        Args:
            report_file: Path to the detailed vulnerabilities CSV file
            
        Returns:
            Dictionary mapping repository names to sets of vulnerability identifiers
        """
        current_vulns = {}
        
        if not report_file.exists():
            print(f"⚠️  Report file not found: {report_file}")
            return current_vulns
        
        with open(report_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                repo_name = row.get('Repository', '').strip()
                package = row.get('Package', '').strip()
                severity = row.get('Severity', '').strip()
                status = row.get('Status', '').strip().lower()
                
                # Only track open vulnerabilities
                if status == 'open' and repo_name and package:
                    if repo_name not in current_vulns:
                        current_vulns[repo_name] = set()
                    
                    # Create unique identifier for vulnerability
                    vuln_id = f"{package}|{severity}"
                    current_vulns[repo_name].add(vuln_id)
        
        print(f"📊 Loaded current vulnerabilities from {report_file.name}")
        print(f"   Repositories with open vulnerabilities: {len(current_vulns)}")
        return current_vulns
    
    def extract_vulnerability_ids_from_issue(self, issue_body: str) -> Set[str]:
        """
        Extract vulnerability identifiers from issue body.
        
        Args:
            issue_body: The body text of the GitHub issue
            
        Returns:
            Set of vulnerability identifiers found in the issue
        """
        vuln_ids = set()
        
        if not issue_body:
            return vuln_ids
        
        # Parse the issue body to extract package names and severities
        # Expected format: | Package | Version | Severity | ... |
        lines = issue_body.split('\n')
        in_table = False
        
        for line in lines:
            if '|' in line and ('Package' in line or 'package' in line):
                in_table = True
                continue
            
            if in_table and '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:  # Should have empty, package, version, severity, ...
                    package = parts[1] if len(parts) > 1 else ''
                    severity = parts[3] if len(parts) > 3 else ''
                    
                    if package and severity and package not in ['Package', 'package', '-', '--']:
                        vuln_id = f"{package}|{severity}"
                        vuln_ids.add(vuln_id)
        
        return vuln_ids
    
    def close_fixed_issues(self, repo_name: str, current_vulns: Set[str]) -> None:
        """
        Close issues for a repository that have been fixed.
        
        Args:
            repo_name: Name of the repository
            current_vulns: Set of current open vulnerability identifiers
        """
        try:
            repo = self.org.get_repo(repo_name)
            
            # Get all open issues with security-Vulnerability label
            open_issues = list(repo.get_issues(
                state='open',
                labels=['security-Vulnerability']
            ))
            
            if not open_issues:
                return
            
            print(f"\n📋 Repository: {repo_name}")
            print(f"   Open security issues: {len(open_issues)}")
            self.stats['open_issues_found'] += len(open_issues)
            
            for issue in open_issues:
                # Extract vulnerabilities mentioned in the issue
                issue_vulns = self.extract_vulnerability_ids_from_issue(issue.body)
                
                if not issue_vulns:
                    print(f"   ⚠️  Issue #{issue.number}: Could not parse vulnerabilities, skipping")
                    self.stats['issues_skipped'] += 1
                    continue
                
                # Check if any vulnerabilities in the issue are still open
                still_open = issue_vulns.intersection(current_vulns)
                
                if not still_open:
                    # All vulnerabilities in this issue have been fixed
                    if self.dry_run:
                        print(f"   🔍 [DRY RUN] Would close issue #{issue.number}: {issue.title}")
                        print(f"      Fixed vulnerabilities: {len(issue_vulns)}")
                    else:
                        # Close the issue with a comment
                        closing_comment = (
                            f"🎉 **All vulnerabilities mentioned in this issue have been resolved!**\n\n"
                            f"✅ Fixed vulnerabilities: {len(issue_vulns)}\n"
                            f"📅 Verified on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            f"This issue is being automatically closed as all security vulnerabilities "
                            f"have been addressed. If you believe this was closed in error, please reopen it."
                        )
                        
                        issue.create_comment(closing_comment)
                        issue.edit(state='closed')
                        
                        print(f"   ✅ Closed issue #{issue.number}: {issue.title}")
                        print(f"      Fixed vulnerabilities: {len(issue_vulns)}")
                    
                    self.stats['issues_closed'] += 1
                else:
                    print(f"   ℹ️  Issue #{issue.number}: Still has {len(still_open)} open vulnerabilities")
                    self.stats['issues_skipped'] += 1
        
        except GithubException as e:
            print(f"   ❌ Error processing {repo_name}: {e}")
            self.stats['errors'] += 1
        except Exception as e:
            print(f"   ❌ Unexpected error for {repo_name}: {e}")
            self.stats['errors'] += 1
    
    def process_all_repositories(self, current_vulns: Dict[str, Set[str]]) -> None:
        """
        Process all repositories to close fixed issues.
        
        Args:
            current_vulns: Dictionary of current vulnerabilities by repository
        """
        # Get all repositories that had vulnerabilities (in current scan or had open issues)
        all_repo_names = set(current_vulns.keys())
        
        # Also check repositories that might have open issues but no current vulnerabilities
        try:
            for repo in self.org.get_repos():
                if repo.name not in all_repo_names:
                    # Check if it has open security issues
                    try:
                        issues = list(repo.get_issues(
                            state='open',
                            labels=['security-Vulnerability']
                        ))
                        if issues:
                            all_repo_names.add(repo.name)
                    except:
                        pass
        except Exception as e:
            print(f"⚠️  Could not enumerate all repositories: {e}")
        
        print(f"\n🔍 Checking {len(all_repo_names)} repositories for fixed issues...")
        
        for repo_name in sorted(all_repo_names):
            self.stats['repos_checked'] += 1
            current_repo_vulns = current_vulns.get(repo_name, set())
            self.close_fixed_issues(repo_name, current_repo_vulns)
    
    def print_summary(self) -> None:
        """Print summary statistics."""
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        print(f"Repositories checked:     {self.stats['repos_checked']}")
        print(f"Open issues found:        {self.stats['open_issues_found']}")
        
        if self.dry_run:
            print(f"Issues to close:          {self.stats['issues_closed']}")
        else:
            print(f"Issues closed:            {self.stats['issues_closed']}")
        
        print(f"Issues skipped:           {self.stats['issues_skipped']}")
        print(f"Errors encountered:       {self.stats['errors']}")
        print("="*60)


def find_latest_report() -> Optional[Path]:
    """Find the most recent vulnerability report."""
    reports_dir = Path(__file__).parent / 'reports'
    
    if not reports_dir.exists():
        return None
    
    # Find all report directories
    report_dirs = [d for d in reports_dir.iterdir() if d.is_dir() and 'security_reports' in d.name]
    
    if not report_dirs:
        return None
    
    # Sort by modification time and get the latest
    latest_dir = max(report_dirs, key=lambda d: d.stat().st_mtime)
    
    # Look for detailed vulnerabilities CSV
    csv_file = latest_dir / 'detailed_vulnerabilities.csv'
    
    if csv_file.exists():
        return csv_file
    
    return None


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Close GitHub issues for fixed security vulnerabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Close fixed issues using latest scan (preview only)
  python close_fixed_issues.py --dry-run
  
  # Actually close fixed issues using latest scan
  python close_fixed_issues.py
  
  # Use specific report file
  python close_fixed_issues.py --report reports/10R1_security_reports_20251108_101004/detailed_vulnerabilities.csv
  
  # Preview what would be closed for a specific report
  python close_fixed_issues.py --report path/to/report.csv --dry-run
        """
    )
    
    parser.add_argument(
        '--report',
        type=str,
        help='Path to the detailed vulnerabilities CSV report (default: auto-detect latest)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be closed without actually closing issues'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get GitHub credentials
    github_token = os.getenv('GITHUB_TOKEN')
    org_name = os.getenv('GITHUB_ORG')
    
    if not github_token or not org_name:
        print("❌ Error: GITHUB_TOKEN and GITHUB_ORG must be set in .env file")
        sys.exit(1)
    
    # Determine report file
    if args.report:
        report_file = Path(args.report)
    else:
        report_file = find_latest_report()
    
    if not report_file or not report_file.exists():
        print("❌ Error: No vulnerability report found")
        print("   Please run a scan first: python security_pipeline.py")
        sys.exit(1)
    
    print("🔧 Close Fixed Security Issues")
    print("="*60)
    print(f"Report file: {report_file}")
    print(f"Organization: {org_name}")
    print(f"Mode: {'DRY RUN (preview only)' if args.dry_run else 'LIVE (will close issues)'}")
    print("="*60)
    
    # Initialize closer
    closer = IssueCloser(github_token, org_name, dry_run=args.dry_run)
    
    # Load current vulnerabilities from report
    current_vulns = closer.get_current_vulnerabilities(report_file)
    
    # Process all repositories
    closer.process_all_repositories(current_vulns)
    
    # Print summary
    closer.print_summary()
    
    if args.dry_run:
        print("\n💡 This was a dry run. Use without --dry-run to actually close issues.")


if __name__ == "__main__":
    main()
