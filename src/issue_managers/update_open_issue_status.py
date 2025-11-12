"""
Script to update GitHub Projects status for open security issues.
Changes status from "Done" to "In Progress" for all open issues with security-Vulnerability label.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv()


def update_project_status_to_in_progress(issue_node_id: str, github_token: str, org_name: str, github_enterprise_url: str) -> bool:
    """
    Update the GitHub Projects status to "In Progress" for an open issue.
    
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
    updated = False
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
                updated = True
    
    return updated


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Update project status for open security issues')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    args = parser.parse_args()
    
    # Get credentials
    github_token = os.getenv('GITHUB_TOKEN')
    github_org = os.getenv('GITHUB_ORG', 'MiDAS')
    github_enterprise_url = os.getenv('GITHUB_ENTERPRISE_URL')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not found in environment variables")
        sys.exit(1)
    
    print("=" * 70)
    print("Update Project Status for Open Security Issues")
    print("=" * 70)
    print(f"Organization: {github_org}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE MODE'}")
    print("=" * 70)
    print()
    
    # Initialize GitHub client
    if github_enterprise_url:
        base_url = f"{github_enterprise_url}/api/v3"
        github = Github(base_url=base_url, login_or_token=github_token)
    else:
        github = Github(github_token)
    
    org = github.get_organization(github_org)
    
    # Statistics
    stats = {
        'repos_checked': 0,
        'issues_found': 0,
        'status_updated': 0,
        'errors': 0
    }
    
    print("Scanning repositories for open security issues...\n")
    
    # Get all repositories
    try:
        for repo in org.get_repos():
            try:
                stats['repos_checked'] += 1
                
                # Get open issues with security-Vulnerability label
                issues = repo.get_issues(
                    state='open',
                    labels=['security-Vulnerability']
                )
                
                for issue in issues:
                    stats['issues_found'] += 1
                    
                    # Check if it's our automated issue format
                    if "fix all dependabot issues" not in issue.title.lower():
                        continue
                    
                    print(f"Found: {repo.name} #{issue.number}")
                    print(f"  Title: {issue.title}")
                    
                    if not args.dry_run:
                        # Update project status
                        updated = update_project_status_to_in_progress(
                            issue.node_id,
                            github_token,
                            github_org,
                            github_enterprise_url
                        )
                        
                        if updated:
                            print(f"  -> Status updated to 'In Progress'\n")
                            stats['status_updated'] += 1
                        else:
                            print(f"  -> No status update needed or not in project\n")
                    else:
                        print(f"  -> Would update status (dry-run)\n")
                        stats['status_updated'] += 1
                        
            except Exception as e:
                print(f"ERROR processing {repo.name}: {e}")
                stats['errors'] += 1
                
    except Exception as e:
        print(f"ERROR scanning repositories: {e}")
        stats['errors'] += 1
    
    # Print summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Repositories checked:   {stats['repos_checked']}")
    print(f"Open issues found:      {stats['issues_found']}")
    print(f"Status updated:         {stats['status_updated']}")
    print(f"Errors:                 {stats['errors']}")
    print("=" * 70)
    
    if args.dry_run:
        print("\nThis was a dry run. Use without --dry-run to actually update status.")


if __name__ == "__main__":
    main()
