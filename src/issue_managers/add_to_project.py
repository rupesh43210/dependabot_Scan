"""
Script to add issues to GitHub Project 23 (OPL Management)
"""

import os
import sys
import requests
from dotenv import load_dotenv
from github import Github

load_dotenv()


def add_issue_to_project(issue_node_id: str, project_number: int, github_token: str, org_name: str, github_enterprise_url: str) -> bool:
    """
    Add an issue to a GitHub Project.
    
    Args:
        issue_node_id: The global node ID of the issue
        project_number: Project number (e.g., 23)
        github_token: GitHub authentication token
        org_name: Organization name
        github_enterprise_url: GitHub Enterprise URL
        
    Returns:
        True if added successfully, False otherwise
    """
    graphql_url = f"{github_enterprise_url}/api/graphql"
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json'
    }
    
    # First, get the project ID
    project_query = """
    query($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          id
        }
      }
    }
    """
    
    response = requests.post(
        graphql_url,
        headers=headers,
        json={
            'query': project_query,
            'variables': {
                'org': org_name,
                'number': project_number
            }
        }
    )
    
    if response.status_code != 200:
        print(f"  Error getting project: {response.status_code}")
        return False
    
    data = response.json()
    if 'errors' in data:
        print(f"  GraphQL errors: {data['errors']}")
        return False
    
    project_id = data.get('data', {}).get('organization', {}).get('projectV2', {}).get('id')
    
    if not project_id:
        print(f"  Project {project_number} not found")
        return False
    
    # Add the issue to the project
    add_mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {
        projectId: $projectId
        contentId: $contentId
      }) {
        item {
          id
        }
      }
    }
    """
    
    add_response = requests.post(
        graphql_url,
        headers=headers,
        json={
            'query': add_mutation,
            'variables': {
                'projectId': project_id,
                'contentId': issue_node_id
            }
        }
    )
    
    if add_response.status_code == 200:
        add_data = add_response.json()
        if 'errors' not in add_data:
            return True
        else:
            print(f"  Error adding to project: {add_data['errors']}")
    
    return False


def main():
    # Get credentials
    github_token = os.getenv('GITHUB_TOKEN')
    github_org = os.getenv('GITHUB_ORG', 'MiDAS')
    github_enterprise_url = os.getenv('GITHUB_ENTERPRISE_URL')
    
    if not github_token:
        print("ERROR: GITHUB_TOKEN not found in environment variables")
        sys.exit(1)
    
    print("=" * 70)
    print("Add Issues to GitHub Project")
    print("=" * 70)
    print(f"Organization: {github_org}")
    print(f"Project: #23 (OPL Management)")
    print("=" * 70)
    print()
    
    # Initialize GitHub client
    base_url = f"{github_enterprise_url}/api/v3"
    github = Github(base_url=base_url, login_or_token=github_token)
    org = github.get_organization(github_org)
    
    # Issues to add
    repos_and_issues = [
        ('uc-dar-api', 185),
        ('uc-ditto-api', 58)
    ]
    
    stats = {'added': 0, 'errors': 0}
    
    for repo_name, issue_num in repos_and_issues:
        try:
            repo = org.get_repo(repo_name)
            issue = repo.get_issue(issue_num)
            
            print(f"Processing: {repo_name} #{issue_num}")
            print(f"  Title: {issue.title}")
            
            # Add to project
            success = add_issue_to_project(
                issue.node_id,
                23,  # OPL Management project number
                github_token,
                github_org,
                github_enterprise_url
            )
            
            if success:
                print(f"  -> Added to Project #23\n")
                stats['added'] += 1
            else:
                print(f"  -> Failed to add to project\n")
                stats['errors'] += 1
                
        except Exception as e:
            print(f"ERROR processing {repo_name} #{issue_num}: {e}\n")
            stats['errors'] += 1
    
    # Print summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Issues added to project: {stats['added']}")
    print(f"Errors:                  {stats['errors']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
