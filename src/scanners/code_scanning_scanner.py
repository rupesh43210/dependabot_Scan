#!/usr/bin/env python3
"""
Code Scanning Scanner - Separate Module

A scanner for GitHub Code Scanning alerts (SAST - Static Application Security Testing)
that generates reports similar to Dependabot vulnerability reports.

GitHub Code Scanning detects:
- Security vulnerabilities
- Quality issues
- Code smells
- Best practice violations

Detected by tools like:
- CodeQL
- Third-party security scanners
- Custom scanning tools

Author: GitHub Copilot
Version: 1.0.0
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from github import Github
from dotenv import load_dotenv


class CodeScanningScanner:
    """
    Scanner for GitHub Code Scanning alerts across repositories.
    
    Features:
    - Complete Code Scanning alert extraction
    - Severity and rule tracking
    - Tool identification (CodeQL, etc.)
    - Comprehensive error handling
    - Rate limiting protection
    """
    
    # Severity mapping for consistency with Dependabot reports
    SEVERITY_WEIGHTS = {
        'critical': 50,
        'high': 20,
        'medium': 5,
        'low': 1,
        'warning': 3,
        'note': 1,
        'error': 20
    }
    
    def __init__(self, github_token: str, base_url: str = None):
        """
        Initialize the code scanning scanner.
        
        Args:
            github_token: GitHub personal access token
            base_url: GitHub base URL (auto-detected from environment)
        """
        # Get base URL from environment or use default
        if base_url is None:
            github_url = os.getenv('GITHUB_URL', '')
            if github_url and 'github.com' in github_url:
                base_url = 'https://github.com'
            else:
                base_url = os.getenv('GITHUB_ENTERPRISE_URL', 'https://github.com')
        
        self.base_url = base_url.rstrip('/').replace('/api/v3', '')
        self.api_base = f"{self.base_url}/api/v3"
        self.github_token = github_token
        
        # Initialize GitHub client
        if 'github.com' in self.base_url and self.base_url == 'https://github.com':
            self.github_client = Github(login_or_token=github_token)
        else:
            self.github_client = Github(base_url=f"{self.base_url}/api/v3", login_or_token=github_token)
        
        # Configure session for API calls
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Code-Scanning-Scanner/1.0'
        })
        
        self.stats = {
            'repositories_scanned': 0,
            'alerts_found': 0,
            'repositories_with_alerts': 0,
            'scan_errors': 0
        }
        
        # Store repository metadata
        self.repository_metadata = {}
    
    def get_organization_repositories(self, org_name: str) -> List[str]:
        """
        Fetch all repository names from the organization.
        
        Args:
            org_name: Organization name or username
            
        Returns:
            List of repository names
        """
        print(f"Fetching repositories from {org_name}...")
        
        try:
            # Try as organization first
            try:
                org = self.github_client.get_organization(org_name)
                repos = []
                page = 1
                
                while True:
                    try:
                        repo_page = list(org.get_repos(type='all').get_page(page - 1))
                        if not repo_page:
                            break
                        print(f"  Found {len(repo_page)} repositories on page {page}")
                        repos.extend([repo.name for repo in repo_page])
                        page += 1
                    except Exception:
                        if page == 1:
                            all_repos = list(org.get_repos(type='all'))
                            repos.extend([repo.name for repo in all_repos])
                            print(f"  Found {len(all_repos)} repositories")
                        break
                
                print(f"Total repositories found: {len(repos)} (organization)")
                return repos
                
            except Exception:
                # Try as user account
                print(f"  Not an organization, trying as user account...")
                user = self.github_client.get_user(org_name)
                all_repos = list(user.get_repos(type='all'))
                repos = [repo.name for repo in all_repos]
                print(f"  Found {len(repos)} repositories (user account)")
                print(f"Total repositories found: {len(repos)}")
                return repos
            
        except Exception as e:
            print(f"❌ Error fetching repositories: {e}")
            return []
    
    def get_repository_code_scanning_alerts(self, org_name: str, repo_name: str) -> List[Dict]:
        """
        Extract all Code Scanning alerts from a repository.
        
        Args:
            org_name: Organization name
            repo_name: Repository name
            
        Returns:
            List of alert dictionaries
        """
        url = f"{self.api_base}/repos/{org_name}/{repo_name}/code-scanning/alerts"
        alerts = []
        page = 1
        repo_obj = None
        default_branch = None
        
        while True:
            try:
                response = self.session.get(url, params={'page': page, 'per_page': 100})
                
                if response.status_code == 403:
                    print(f"  No access to Code Scanning alerts for {repo_name}")
                    break
                elif response.status_code == 404:
                    # Repository might not have Code Scanning enabled
                    try:
                        repo_obj = self.github_client.get_repo(f"{org_name}/{repo_name}")
                        if repo_obj.archived:
                            print(f"  Skipping archived repository: {repo_name}")
                        else:
                            print(f"  Code Scanning not enabled for {repo_name}")
                        break
                    except:
                        break
                elif response.status_code != 200:
                    print(f"  ⚠️  Error {response.status_code} for {repo_name}")
                    break
                
                page_alerts = response.json()
                
                # Get repository object for metadata
                if repo_obj is None:
                    try:
                        repo_obj = self.github_client.get_repo(f"{org_name}/{repo_name}")
                    except Exception as e:
                        print(f"  ⚠️  Could not access repository {repo_name}: {e}")
                
                # Get default branch
                if default_branch is None and repo_obj is not None:
                    try:
                        default_branch = repo_obj.default_branch
                        print(f"  📍 Default branch: {default_branch}")
                        self.repository_metadata[repo_name] = {
                            'default_branch': default_branch,
                            'has_alerts': len(page_alerts) > 0
                        }
                    except Exception as e:
                        print(f"  ⚠️  Could not get default branch: {e}")
                        default_branch = 'unknown'
                        self.repository_metadata[repo_name] = {
                            'default_branch': 'unknown',
                            'has_alerts': len(page_alerts) > 0
                        }
                
                if not page_alerts:
                    break
                
                # Process each alert
                for alert in page_alerts:
                    processed_alert = self._process_code_scanning_alert(
                        repo_name, alert, default_branch
                    )
                    if processed_alert:
                        alerts.append(processed_alert)
                
                page += 1
                
            except Exception as e:
                print(f"  ❌ Error processing {repo_name}: {e}")
                self.stats['scan_errors'] += 1
                break
        
        return alerts
    
    def _process_code_scanning_alert(self, repo_name: str, alert: Dict, default_branch: str) -> Optional[Dict]:
        """
        Process and normalize a Code Scanning alert.
        
        Args:
            repo_name: Repository name
            alert: Raw alert data from GitHub API
            default_branch: Default branch name
            
        Returns:
            Processed alert dictionary
        """
        try:
            rule = alert.get('rule', {})
            tool = alert.get('tool', {})
            most_recent_instance = alert.get('most_recent_instance', {})
            location = most_recent_instance.get('location', {})
            
            return {
                # Repository info
                'repository': repo_name,
                'scanned_branch': default_branch if default_branch else 'unknown',
                'alert_number': alert.get('number'),
                'alert_state': alert.get('state'),  # open, dismissed, fixed
                'alert_url': alert.get('html_url'),
                
                # Alert details
                'rule_id': rule.get('id'),
                'rule_name': rule.get('name'),
                'rule_description': rule.get('description'),
                'rule_severity': rule.get('severity'),  # error, warning, note
                'rule_security_severity_level': rule.get('security_severity_level'),  # critical, high, medium, low
                'rule_tags': ','.join(rule.get('tags', [])),
                
                # Tool information
                'tool_name': tool.get('name'),  # e.g., CodeQL
                'tool_version': tool.get('version'),
                
                # Location information
                'file_path': location.get('path'),
                'start_line': location.get('start_line'),
                'end_line': location.get('end_line'),
                'start_column': location.get('start_column'),
                'end_column': location.get('end_column'),
                
                # Timestamps
                'created_at': alert.get('created_at'),
                'updated_at': alert.get('updated_at'),
                'fixed_at': alert.get('fixed_at'),
                'dismissed_at': alert.get('dismissed_at'),
                
                # Dismissal information
                'dismissed_by': alert.get('dismissed_by', {}).get('login') if alert.get('dismissed_by') else None,
                'dismissed_reason': alert.get('dismissed_reason'),
                'dismissed_comment': alert.get('dismissed_comment'),
                
                # Instance details
                'instance_ref': most_recent_instance.get('ref'),
                'instance_commit_sha': most_recent_instance.get('commit_sha'),
                'instance_state': most_recent_instance.get('state'),
                'instance_message': most_recent_instance.get('message', {}).get('text'),
                
                # Calculate age
                'alert_age_days': self._calculate_age_days(alert.get('created_at')),
            }
        except Exception as e:
            print(f"  ⚠️  Error processing alert: {e}")
            return None
    
    def _calculate_age_days(self, created_at: Optional[str]) -> Optional[int]:
        """Calculate age of alert in days."""
        if not created_at:
            return None
        
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now(created.tzinfo)
            return (now - created).days
        except:
            return None
    
    def scan_organization(self, org_name: str, specific_repos: Optional[List[str]] = None) -> List[Dict]:
        """
        Scan entire organization for Code Scanning alerts.
        
        Args:
            org_name: Organization name or username to scan
            specific_repos: Optional list of specific repository names to scan
            
        Returns:
            List of all alerts found
        """
        print(f"🔍 Starting Code Scanning alert scan for {org_name}")
        print("=" * 70)
        
        # Get all repositories
        all_repositories = self.get_organization_repositories(org_name)
        if not all_repositories:
            print("❌ No repositories found or access denied")
            return []
        
        # Filter repositories if specific list provided
        if specific_repos:
            specific_repos = [repo.strip() for repo in specific_repos if repo.strip()]
            repositories = [repo for repo in all_repositories if repo in specific_repos]
            
            print(f"📋 Repository Filtering:")
            print(f"   Total repositories available: {len(all_repositories)}")
            print(f"   Specific repositories requested: {len(specific_repos)}")
            print(f"   Repositories to scan: {len(repositories)}")
            
            missing_repos = [repo for repo in specific_repos if repo not in all_repositories]
            if missing_repos:
                print(f"   ⚠️  Repositories not found: {', '.join(missing_repos)}")
            
            if not repositories:
                print("❌ None of the specified repositories were found")
                return []
            
            print(f"   ✅ Scanning repositories: {', '.join(repositories)}")
        else:
            repositories = all_repositories
            print(f"📋 Scanning all {len(repositories)} repositories")
        
        all_alerts = []
        
        # Scan each repository
        for i, repo_name in enumerate(repositories, 1):
            print(f"[{i}/{len(repositories)}] Processing {repo_name}...")
            self.stats['repositories_scanned'] += 1
            
            alerts = self.get_repository_code_scanning_alerts(org_name, repo_name)
            
            if alerts:
                print(f"  Found {len(alerts)} Code Scanning alerts")
                all_alerts.extend(alerts)
                self.stats['repositories_with_alerts'] += 1
                self.stats['alerts_found'] += len(alerts)
            else:
                print(f"  No Code Scanning alerts found")
        
        print(f"✅ Code Scanning scan completed: {len(all_alerts)} alerts found")
        return all_alerts
    
    def save_results(self, alerts: List[Dict], timestamp: str) -> Tuple[str, str, str]:
        """
        Save scan results to JSON and CSV files.
        
        Args:
            alerts: List of alert data
            timestamp: Timestamp string for file naming
            
        Returns:
            Tuple of (json_filename, csv_filename, metadata_filename)
        """
        # Create filenames
        json_filename = f"temp_code_scanning_{timestamp}.json"
        csv_filename = f"temp_code_scanning_{timestamp}.csv"
        metadata_filename = f"temp_code_scanning_metadata_{timestamp}.json"
        
        # Save JSON
        with open(json_filename, 'w') as f:
            json.dump(alerts, f, indent=2, default=str)
        
        # Save CSV
        if alerts:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=alerts[0].keys())
                writer.writeheader()
                writer.writerows(alerts)
        
        # Save repository metadata
        with open(metadata_filename, 'w') as f:
            json.dump(self.repository_metadata, f, indent=2, default=str)
        
        return json_filename, csv_filename, metadata_filename
    
    def print_statistics(self):
        """Print scan statistics."""
        print(f"\n📊 Scan Statistics:")
        print(f"   Repositories scanned: {self.stats['repositories_scanned']}")
        print(f"   Repositories with alerts: {self.stats['repositories_with_alerts']}")
        print(f"   Total alerts found: {self.stats['alerts_found']}")
        print(f"   Scan errors: {self.stats['scan_errors']}")


def main():
    """Main execution function."""
    load_dotenv()
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        return
    
    scanner = CodeScanningScanner(github_token)
    org_name = os.getenv('GITHUB_ORG', 'your-organization')
    
    alerts = scanner.scan_organization(org_name)
    
    if alerts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file, csv_file, metadata_file = scanner.save_results(alerts, timestamp)
        
        print(f"\n📁 Results saved:")
        print(f"   JSON: {json_file}")
        print(f"   CSV: {csv_file}")
        print(f"   Metadata: {metadata_file}")
    
    scanner.print_statistics()


if __name__ == "__main__":
    main()
