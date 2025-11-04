#!/usr/bin/env python3
"""
GitHub Issue Manager

Automatically creates GitHub issues for repositories with security vulnerabilities
based on vulnerability scan results.

Author: GitHub Copilot
Version: 1.0.0
"""

import os
from typing import Dict, List, Optional, Any
from github import Github
from github.GithubException import GithubException
import pandas as pd


class GitHubIssueManager:
    """
    Manages creation of GitHub issues for vulnerability remediation.
    
    Features:
    - Automatic issue creation for repositories with vulnerabilities
    - Severity-based issue formatting
    - Project assignment support
    - Duplicate issue prevention
    """
    
    def __init__(self, github_token: str, org_name: str, base_url: str = None):
        """
        Initialize the GitHub Issue Manager.
        
        Args:
            github_token: GitHub personal access token
            org_name: Organization name
            base_url: GitHub base URL (auto-detected from environment)
        """
        self.org_name = org_name
        
        # Get base URL from environment or use default
        if base_url is None:
            github_url = os.getenv('GITHUB_URL', '')
            if github_url and 'github.com' in github_url:
                base_url = 'https://github.com'
            else:
                base_url = os.getenv('GITHUB_ENTERPRISE_URL', 'https://github.com')
        
        # Remove /api/v3 suffix if present and ensure proper format
        self.base_url = base_url.rstrip('/').replace('/api/v3', '')
        
        # Initialize GitHub client
        if 'github.com' in self.base_url and self.base_url == 'https://github.com':
            self.github_client = Github(login_or_token=github_token)
        else:
            self.github_client = Github(base_url=f"{self.base_url}/api/v3", login_or_token=github_token)
        
        self.stats = {
            'issues_created': 0,
            'issues_updated': 0,
            'repositories_processed': 0,
            'errors': 0
        }
    
    def analyze_repository_vulnerabilities(self, vulnerability_data: pd.DataFrame, 
                                         repository_name: str) -> Dict[str, int]:
        """
        Analyze vulnerabilities for a specific repository.
        
        Args:
            vulnerability_data: DataFrame with vulnerability data
            repository_name: Name of the repository to analyze
            
        Returns:
            Dictionary with severity counts
        """
        # Filter data for the specific repository
        repo_data = vulnerability_data[
            (vulnerability_data['repository'] == repository_name) & 
            (vulnerability_data['alert_state'] == 'open')
        ]
        
        if repo_data.empty:
            return {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'total': 0}
        
        # Count vulnerabilities by severity (handle both upper and lower case)
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for _, row in repo_data.iterrows():
            severity = row['severity'].lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        severity_counts['total'] = sum(severity_counts.values())
        return severity_counts
    
    def format_issue_title(self, repository_name: str, severity_counts: Dict[str, int]) -> str:
        """
        Format the issue title according to specifications.
        
        Args:
            repository_name: Name of the repository
            severity_counts: Dictionary with severity counts
            
        Returns:
            Formatted issue title
        """
        title = f"{repository_name} - Fix all dependabot issues "
        title += f"Critical - {severity_counts['critical']:02d}, "
        title += f"High - {severity_counts['high']:02d}, "
        title += f"Medium - {severity_counts['medium']:02d}, "
        title += f"Low - {severity_counts['low']:02d}"
    def assign_issue_to_project(self, repo, issue, project_name: str) -> bool:
        """
        Assign an issue to a project using GitHub GraphQL API.
        
        Args:
            repo: Repository object
            issue: Issue object
            project_name: Name of the project to assign to
            
        Returns:
            True if assignment was successful, False otherwise
        """
        try:
            # For OPL Management project (ID: 23)
            if project_name == "OPL Management":
                import requests
                import json
                
                # GitHub GraphQL API endpoint
                if 'github.com' in self.base_url:
                    graphql_url = "https://api.github.com/graphql"
                else:
                    graphql_url = f"{self.base_url}/api/graphql"
                
                headers = {
                    'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}',
                    'Content-Type': 'application/json',
                }
                
                # First get project ID
                project_query = """
                query($org: String!, $number: Int!) {
                  organization(login: $org) {
                    projectV2(number: $number) {
                      id
                    }
                  }
                }
                """
                
                project_variables = {
                    'org': self.org_name,
                    'number': 23
                }
                
                project_response = requests.post(
                    graphql_url,
                    headers=headers,
                    json={'query': project_query, 'variables': project_variables},
                    timeout=30
                )
                
                if project_response.status_code != 200:
                    print(f"  ⚠️  Could not get project ID")
                    return False
                
                project_data = project_response.json()
                if not project_data.get('data', {}).get('organization', {}).get('projectV2'):
                    print(f"  ⚠️  Project '{project_name}' not found")
                    return False
                
                project_id = project_data['data']['organization']['projectV2']['id']
                
                # Now add issue to project
                add_mutation = """
                mutation($projectId: ID!, $contentId: ID!) {
                  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                    item {
                      id
                    }
                  }
                }
                """
                
                add_variables = {
                    'projectId': project_id,
                    'contentId': issue.node_id
                }
                
                add_response = requests.post(
                    graphql_url,
                    headers=headers,
                    json={'query': add_mutation, 'variables': add_variables},
                    timeout=30
                )
                
                if add_response.status_code == 200:
                    add_data = add_response.json()
                    if add_data.get('data', {}).get('addProjectV2ItemById'):
                        print(f"  ✅ Assigned to project '{project_name}'")
                        return True
                
                print(f"  ⚠️  Could not assign to project '{project_name}'")
                return False
            else:
                print(f"  ⚠️  Project '{project_name}' assignment not configured")
                return False
            
        except Exception as e:
            print(f"  ⚠️  Could not assign to project '{project_name}': {e}")
            return False
    
    def format_issue_body(self, repository_name: str, severity_counts: Dict[str, int], 
                         vulnerability_data: pd.DataFrame) -> str:
        """
        Format the issue body with detailed vulnerability information.
        
        Args:
            repository_name: Name of the repository
            severity_counts: Dictionary with severity counts
            vulnerability_data: DataFrame with vulnerability data
            
        Returns:
            Formatted issue body
        """
        # Filter data for the specific repository
        repo_data = vulnerability_data[
            (vulnerability_data['repository'] == repository_name) & 
            (vulnerability_data['alert_state'] == 'open')
        ]
        
        body = f"""# Security Vulnerability Report for {repository_name}

## 📊 Vulnerability Summary
- **Total Open Vulnerabilities**: {severity_counts['total']}
- **Critical**: {severity_counts['critical']}
- **High**: {severity_counts['high']}
- **Medium**: {severity_counts['medium']}
- **Low**: {severity_counts['low']}

## 🚨 Priority Actions Required

### Critical & High Priority Issues
"""
        
        # Add critical and high severity details
        critical_high = repo_data[repo_data['severity'].str.upper().isin(['CRITICAL', 'HIGH'])]
        if not critical_high.empty:
            for _, vuln in critical_high.iterrows():
                body += f"""
**{vuln['severity'].upper()}**: {vuln.get('package_name', 'Unknown Package')}
- **Advisory**: {vuln.get('advisory_summary', 'No summary available')}
- **CVSS Score**: {vuln.get('cvss_score', 'N/A')}
- **CWE**: {vuln.get('cwe_id', 'N/A')}
"""
        else:
            body += "\nNo critical or high severity vulnerabilities found.\n"
        
        body += f"""
## 📋 All Vulnerabilities Details

| Package | Severity | CVSS | Advisory | Status |
|---------|----------|------|----------|--------|
"""
        
        # Add table with all vulnerabilities
        for _, vuln in repo_data.iterrows():
            package_name = vuln.get('package_name', 'Unknown')
            severity = vuln.get('severity', 'Unknown').upper()
            cvss_score = vuln.get('cvss_score', 'N/A')
            advisory = vuln.get('advisory_summary', 'No summary')[:50] + "..." if len(str(vuln.get('advisory_summary', ''))) > 50 else vuln.get('advisory_summary', 'No summary')
            status = vuln.get('alert_state', 'Unknown').title()
            
            body += f"| {package_name} | {severity} | {cvss_score} | {advisory} | {status} |\n"
        
        body += f"""
## 🔧 Recommended Actions

1. **Immediate**: Address all Critical and High severity vulnerabilities
2. **Short-term**: Update vulnerable packages to secure versions
3. **Long-term**: Implement automated dependency scanning in CI/CD pipeline

## 📅 Timeline
- **Critical**: Fix within 24-48 hours
- **High**: Fix within 1 week
- **Medium**: Fix within 2 weeks
- **Low**: Address during regular maintenance
"""
        
        return body
    
    def check_existing_issue(self, repository_name: str) -> Optional[Any]:
        """
        Check if a vulnerability issue already exists for the repository.
        
        Args:
            repository_name: Name of the repository
            
        Returns:
            Existing issue object or None
        """
        try:
            repo = self.github_client.get_repo(f"{self.org_name}/{repository_name}")
            
            # Search for existing vulnerability issues
            issues = repo.get_issues(state='open')
            for issue in issues:
                if ("Fix all dependabot issues" in issue.title and 
                    repository_name in issue.title):
                    return issue
            
            return None
            
        except GithubException as e:
            print(f"  ❌ Error checking existing issues for {repository_name}: {e}")
            return None
    
    def assign_to_project(self, issue: Any, project_name: str = "OPL Management") -> bool:
        """
        Assign issue to a project (Note: GitHub API v3 has limited project support).
        
        Args:
            issue: GitHub issue object
            project_name: Name of the project to assign to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Note: Full project assignment requires GitHub API v4 (GraphQL)
            # For now, we'll add a label to indicate project assignment
            issue.add_to_labels(f"project:{project_name}")
            return True
        except GithubException as e:
            print(f"  ⚠️  Warning: Could not assign to project '{project_name}': {e}")
            return False
    
    def create_vulnerability_issue(self, repository_name: str, severity_counts: Dict[str, int],
                                 vulnerability_data: pd.DataFrame, project_name: str = "OPL Management") -> bool:
        """
        Create a GitHub issue for repository vulnerabilities.
        
        Args:
            repository_name: Name of the repository
            severity_counts: Dictionary with severity counts
            vulnerability_data: DataFrame with vulnerability data
            project_name: Project to assign the issue to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if issue already exists
            existing_issue = self.check_existing_issue(repository_name)
            
            if existing_issue:
                print(f"  ⚠️  Issue already exists for {repository_name}: #{existing_issue.number}")
                
                # Update existing issue with new information
                new_title = self.format_issue_title(repository_name, severity_counts)
                new_body = self.format_issue_body(repository_name, severity_counts, vulnerability_data)
                
                existing_issue.edit(title=new_title, body=new_body)
                print(f"  ✅ Updated existing issue #{existing_issue.number}")
                self.stats['issues_updated'] += 1
                return True
            
            # Create new issue
            repo = self.github_client.get_repo(f"{self.org_name}/{repository_name}")
            
            title = self.format_issue_title(repository_name, severity_counts)
            body = self.format_issue_body(repository_name, severity_counts, vulnerability_data)
            
            # Create the issue
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels if labels else ['security-Vulnerability']
            )
            
            print(f"  ✅ Created issue #{issue.number}: {title}")
            
            # Try to assign to project
            if project_name:
                self.assign_issue_to_project(repo, issue, project_name)
            
            self.stats['issues_created'] += 1
            return True
            
        except GithubException as e:
            print(f"  ❌ Error creating issue for {repository_name}: {e}")
            self.stats['errors'] += 1
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error creating issue for {repository_name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def process_vulnerability_data(self, vulnerability_data: pd.DataFrame, 
                                 scoped_repositories: Optional[List[str]] = None,
                                 project_name: str = "OPL Management") -> Dict[str, Any]:
        """
        Process vulnerability data and create issues for affected repositories.
        
        Args:
            vulnerability_data: DataFrame with vulnerability data
            scoped_repositories: Optional list of repositories to process (None for all)
            project_name: Project to assign issues to
            
        Returns:
            Dictionary with processing statistics
        """
        print("🔧 Creating GitHub issues for repositories with vulnerabilities...")
        
        # Get unique repositories with open vulnerabilities
        repos_with_vulns = vulnerability_data[
            vulnerability_data['alert_state'] == 'open'
        ]['repository'].unique()
        
        if scoped_repositories:
            # Filter to only scoped repositories that have vulnerabilities
            repos_to_process = [repo for repo in repos_with_vulns if repo in scoped_repositories]
            print(f"   📋 Processing {len(repos_to_process)} scoped repositories with vulnerabilities")
        else:
            repos_to_process = repos_with_vulns
            print(f"   📋 Processing {len(repos_to_process)} repositories with vulnerabilities")
        
        if not repos_to_process:
            print("   ✅ No repositories with vulnerabilities found. No issues to create.")
            return self.stats
        
        # Process each repository
        for repo_name in repos_to_process:
            print(f"   [🔧 Processing {repo_name}...")
            
            # Analyze vulnerabilities for this repository
            severity_counts = self.analyze_repository_vulnerabilities(vulnerability_data, repo_name)
            
            if severity_counts['total'] > 0:
                # Create issue for this repository
                success = self.create_vulnerability_issue(
                    repo_name, severity_counts, vulnerability_data, project_name
                )
                
                if success:
                    self.stats['repositories_processed'] += 1
            else:
                print(f"     ℹ️  No open vulnerabilities found for {repo_name}")
        
        return self.stats
    
    def print_summary(self):
        """Print a summary of issue creation results."""
        print("\n📊 GitHub Issue Creation Summary:")
        print(f"   📄 Issues Created: {self.stats['issues_created']}")
        print(f"   📝 Issues Updated: {self.stats['issues_updated']}")
        print(f"   📁 Repositories Processed: {self.stats['repositories_processed']}")
        
        if self.stats['errors'] > 0:
            print(f"   ❌ Errors Encountered: {self.stats['errors']}")
        else:
            print("   ✅ All operations completed successfully")