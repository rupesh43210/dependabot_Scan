"""
Simple script to reopen GitHub issues that were incorrectly closed.
Reopens any closed security-Vulnerability issues that still have open vulnerabilities.
Also updates GitHub Projects status from "Done" back to "In Progress".
"""

import os
import sys
import csv
import re
import requests
from pathlib import Path
from typing import Dict, Set
from datetime import datetime
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv()


def get_current_vulnerabilities(report_file: Path) -> Dict[str, Set[str]]:
    """Load current open vulnerabilities from the scan report."""
    current_vulns = {}
    
    if not report_file.exists():
        print(f"ERROR: Report file not found: {report_file}")
        return current_vulns
    
    with open(report_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            repo_name = row.get('Repository Name', '').strip()
            package = row.get('Component', '').strip()
            severity = row.get('Severity', '').strip()
            status = row.get('Status', '').strip().upper()
            
            # Only track open vulnerabilities
            if status == 'OPEN' and repo_name and package:
                if repo_name not in current_vulns:
                    current_vulns[repo_name] = set()
                
                # Create unique identifier for vulnerability
                vuln_id = f"{package}|{severity}"
                current_vulns[repo_name].add(vuln_id)
    
    print(f"Loaded {len(current_vulns)} repositories with open vulnerabilities")
    return current_vulns


def extract_vulnerability_ids_from_issue(issue_body: str) -> Set[str]:
    """Extract vulnerability identifiers from issue body table."""
    vuln_ids = set()
    
    lines = issue_body.split('\n')
    in_table = False
    
    for line in lines:
        # Detect table start
        if '| Package |' in line or '| Component |' in line:
            in_table = True
            continue
        
        # Skip separator line
        if in_table and line.strip().startswith('|---'):
            continue
        
        # Parse table rows
        if in_table and line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                package = parts[1]
                severity = parts[2]
                
                # Skip header/empty rows
                if not package or package.lower() in ['package', 'component', '']:
                    continue
                
                vuln_id = f"{package}|{severity}"
                vuln_ids.add(vuln_id)
        
        # Stop at end of table
        elif in_table and not line.strip():
            break
    
    return vuln_ids


def update_project_status_to_in_progress(issue_node_id: str, github_token: str, org_name: str, github_enterprise_url: str) -> bool:
    """
    Update the GitHub Projects status from "Done" back to "In Progress" for a reopened issue.
    
    Args:
        issue_node_id: The global node ID of the issue
        github_token: GitHub authentication token
        org_name: Organization name
        github_enterprise_url: GitHub Enterprise URL
        
    Returns:
        True if status was updated, False otherwise
    """
    graphql_url = f"{github_enterprise_url}/api/graphql"
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json'
    }
    
    # Query to get project items for this issue
    query = """
    query($nodeId: ID!) {
      node(id: $nodeId) {
        ... on Issue {
          projectItems(first: 10) {
            nodes {
              id
              project {
                id
                number
              }
            }
          }
        }
      }
    }
    """
    
    response = requests.post(
        graphql_url,
        headers=headers,
        json={'query': query, 'variables': {'nodeId': issue_node_id}}
    )
    
    if response.status_code != 200:
        return False
    
    data = response.json()
    if 'errors' in data:
        return False
    
    project_items = data.get('data', {}).get('node', {}).get('projectItems', {}).get('nodes', [])
    
    if not project_items:
        return False
    
    # For each project the issue is in, update status to "In Progress"
    for item in project_items:
        project_item_id = item.get('id')
        project_info = item.get('project', {})
        
        if not project_item_id:
            continue
        
        # Get the project status field
        project_query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              id
              field(name: "Status") {
                ... on ProjectV2SingleSelectField {
                  id
                  options {
                    id
                    name
                  }
                }
              }
            }
          }
        }
        """
        
        proj_response = requests.post(
            graphql_url,
            headers=headers,
            json={
                'query': project_query,
                'variables': {
                    'org': org_name,
                    'number': project_info.get('number')
                }
            }
        )
        
        if proj_response.status_code != 200:
            continue
        
        proj_data = proj_response.json()
        if 'errors' in proj_data:
            continue
        
        project_data = proj_data.get('data', {}).get('organization', {}).get('projectV2', {})
        status_field = project_data.get('field', {})
        field_id = status_field.get('id')
        
        # Find "In Progress" or "To Do" option ID
        target_option_id = None
        for option in status_field.get('options', []):
            option_name = option.get('name', '').lower()
            # Prefer "In Progress", but accept "To Do" or similar as fallback
            if option_name in ['in progress', 'in-progress', 'inprogress']:
                target_option_id = option.get('id')
                break
            elif option_name in ['todo', 'to do', 'to-do', 'open']:
                target_option_id = option.get('id')
        
        if not field_id or not target_option_id:
            continue
        
        # Update the status
        update_mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $valueId: String!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $projectId
            itemId: $itemId
            fieldId: $fieldId
            value: {singleSelectOptionId: $valueId}
          }) {
            projectV2Item {
              id
            }
          }
        }
        """
        
        update_response = requests.post(
            graphql_url,
            headers=headers,
            json={
                'query': update_mutation,
                'variables': {
                    'projectId': project_data.get('id'),
                    'itemId': project_item_id,
                    'fieldId': field_id,
                    'valueId': target_option_id
                }
            }
        )
        
        if update_response.status_code == 200:
            update_data = update_response.json()
            if 'errors' not in update_data:
                return True
    
    return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Reopen incorrectly closed security issues')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--report', type=str, help='Path to specific report CSV file')
    args = parser.parse_args()
    
    # Get credentials
    github_token = os.getenv('GITHUB_TOKEN')
    github_org = os.getenv('GITHUB_ORG', 'MiDAS')
    github_enterprise_url = os.getenv('GITHUB_ENTERPRISE_URL')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not found in environment variables")
        sys.exit(1)
    
    print("=" * 70)
    print("Reopen Incorrectly Closed Security Issues")
    print("=" * 70)
    print(f"Organization: {github_org}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE MODE'}")
    print("=" * 70)
    
    # Find report file
    if args.report:
        report_file = Path(args.report)
    else:
        reports_dir = Path("../reports")
        if not reports_dir.exists():
            reports_dir = Path("reports")
        
        if not reports_dir.exists():
            print("ERROR: Could not find reports directory")
            sys.exit(1)
        
        # Find most recent report
        report_dirs = [d for d in reports_dir.iterdir() if d.is_dir() and 'security_reports' in d.name]
        if not report_dirs:
            print("ERROR: No security report directories found")
            sys.exit(1)
        
        latest_dir = max(report_dirs, key=lambda d: d.stat().st_mtime)
        report_file = latest_dir / "detailed_vulnerabilities.csv"
    
    print(f"Report: {report_file}")
    print()
    
    # Load current vulnerabilities
    current_vulns = get_current_vulnerabilities(report_file)
    
    if not current_vulns:
        print("No open vulnerabilities found. Nothing to reopen.")
        return
    
    # Initialize GitHub client
    if github_enterprise_url:
        base_url = f"{github_enterprise_url}/api/v3"
        github = Github(base_url=base_url, login_or_token=github_token)
    else:
        github = Github(github_token)
    
    org = github.get_organization(github_org)
    
    # Check each repository
    stats = {'checked': 0, 'reopened': 0, 'skipped': 0, 'errors': 0, 'project_updated': 0}
    
    print(f"Checking {len(current_vulns)} repositories...\n")
    
    for repo_name in current_vulns.keys():
        try:
            repo = org.get_repo(repo_name)
            
            # Get closed issues with security-Vulnerability label
            issues = repo.get_issues(state='closed', labels=['security-Vulnerability'])
            
            for issue in issues:
                stats['checked'] += 1
                
                # Skip if not an automated issue
                if "fix all dependabot issues" not in issue.title.lower():
                    continue
                
                # Extract vulnerabilities from issue
                issue_vulns = extract_vulnerability_ids_from_issue(issue.body or "")
                
                if not issue_vulns:
                    continue
                
                # Check if any are still open
                repo_current_vulns = current_vulns.get(repo_name, set())
                still_open = issue_vulns.intersection(repo_current_vulns)
                
                if still_open:
                    print(f"Found: {repo_name} #{issue.number}")
                    print(f"  Title: {issue.title}")
                    print(f"  Still open: {len(still_open)} vulnerabilities")
                    
                    if not args.dry_run:
                        try:
                            # Reopen the issue
                            issue.edit(state='open')
                            
                            # Update project status
                            project_updated = update_project_status_to_in_progress(
                                issue.node_id,
                                github_token,
                                github_org,
                                github_enterprise_url
                            )
                            if project_updated:
                                stats['project_updated'] += 1
                            
                            # Add comment
                            comment = f"""## Issue Reopened - Automation Error

This issue was incorrectly closed due to a bug in the closure script.

**Bug Details:**
The script was looking for wrong CSV column names ('Repository'/'Package' instead of 'Repository Name'/'Component'), causing it to never detect open vulnerabilities.

**Current Status:**
- **{len(still_open)} vulnerabilities are still open**
- The bug has been fixed
- This issue will remain open until all vulnerabilities are resolved
- Project status updated back to "In Progress"

---
*Reopened by reopen_fixed.py on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
                            
                            issue.create_comment(comment)
                            print(f"  -> REOPENED (Project status: {'updated' if project_updated else 'unchanged'})\n")
                            stats['reopened'] += 1
                        except Exception as e:
                            print(f"  -> ERROR: {e}\n")
                            stats['errors'] += 1
                    else:
                        print(f"  -> Would reopen (dry-run)\n")
                        stats['reopened'] += 1
                else:
                    stats['skipped'] += 1
                    
        except Exception as e:
            print(f"ERROR checking {repo_name}: {e}")
            stats['errors'] += 1
    
    # Print summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Issues checked:         {stats['checked']}")
    print(f"Issues reopened:        {stats['reopened']}")
    print(f"Project status updated: {stats['project_updated']}")
    print(f"Issues skipped:         {stats['skipped']}")
    print(f"Errors:                 {stats['errors']}")
    print("=" * 70)
    
    if args.dry_run:
        print("\nThis was a dry run. Use without --dry-run to actually reopen issues.")


if __name__ == "__main__":
    main()
