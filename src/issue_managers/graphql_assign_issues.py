#!/usr/bin/env python3
"""
Automatically assign existing GitHub security issues to OPL Management project.
Uses GitHub GraphQL API with the token from .env file.
"""

import os
import sys
import json
import requests
from pathlib import Path

class GraphQLProjectAssigner:
    def __init__(self):
        """Initialize the GraphQL Project Assigner."""
        self.load_env_vars()
        
        self.org_name = "MiDAS"
        self.project_number = 23
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = os.getenv('GITHUB_ENTERPRISE_URL', 'https://github.boschdevcloud.com')
        
        # GitHub GraphQL API endpoint
        if 'github.com' in self.base_url:
            self.graphql_url = "https://api.github.com/graphql"
        else:
            self.graphql_url = f"{self.base_url}/api/graphql"
        
        self.headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Content-Type': 'application/json',
        }

    def load_env_vars(self):
        """Load environment variables from .env file."""
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value

    def execute_graphql_query(self, query: str, variables: dict = None) -> dict:
        """Execute a GraphQL query against GitHub API."""
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ GraphQL request failed: {e}")
            return None

    def get_project_id(self) -> str:
        """Get the project ID for OPL Management project."""
        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              id
              title
            }
          }
        }
        """
        
        variables = {
            'org': self.org_name,
            'number': self.project_number
        }
        
        result = self.execute_graphql_query(query, variables)
        
        if result and 'data' in result and result['data']['organization']['projectV2']:
            project_id = result['data']['organization']['projectV2']['id']
            project_title = result['data']['organization']['projectV2']['title']
            print(f"  ✅ Found project: {project_title} (ID: {project_id})")
            return project_id
        else:
            print(f"  ❌ Could not find project #{self.project_number} in organization {self.org_name}")
            if result and 'errors' in result:
                for error in result['errors']:
                    print(f"     Error: {error['message']}")
            return None

    def get_issue_node_id(self, repo_name: str, issue_number: str) -> str:
        """Get the node ID for a specific issue."""
        query = """
        query($owner: String!, $repo: String!, $number: Int!) {
          repository(owner: $owner, name: $repo) {
            issue(number: $number) {
              id
              title
            }
          }
        }
        """
        
        variables = {
            'owner': self.org_name,
            'repo': repo_name,
            'number': int(issue_number)
        }
        
        result = self.execute_graphql_query(query, variables)
        
        if result and 'data' in result and result['data']['repository']['issue']:
            issue_id = result['data']['repository']['issue']['id']
            issue_title = result['data']['repository']['issue']['title']
            print(f"  ✅ Found issue: #{issue_number} - {issue_title}")
            return issue_id
        else:
            print(f"  ❌ Could not find issue #{issue_number} in {repo_name}")
            if result and 'errors' in result:
                for error in result['errors']:
                    print(f"     Error: {error['message']}")
            return None

    def add_issue_to_project(self, project_id: str, issue_node_id: str) -> bool:
        """Add an issue to the project."""
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item {
              id
            }
          }
        }
        """
        
        variables = {
            'projectId': project_id,
            'contentId': issue_node_id
        }
        
        result = self.execute_graphql_query(mutation, variables)
        
        if result and 'data' in result and result['data']['addProjectV2ItemById']:
            print(f"  ✅ Successfully added to project")
            return True
        else:
            print(f"  ❌ Failed to add to project")
            if result and 'errors' in result:
                for error in result['errors']:
                    print(f"     Error: {error['message']}")
            return False

    def get_issues_to_assign(self):
        """Get the list of issues that need to be assigned."""
        return [
            ("uc-mbd-remote-ui", "70"),
            ("uc-tda-remote-ui", "23"), 
            ("MiDAS-Platform", "2909"),
            ("uc-misra-assist-api", "360"),
            ("uc-duta-api", "219"),
            ("uc-code-review-api", "260"),
            ("uc-aoob", "148"),
            ("uc-aspireai-api", "186"),
            ("uc-esperant-ai-api", "57"),
            ("uc-cia-api", "149"),
            ("uc-swrs-ai-api", "74"),
            ("ss9-midas-ui", "780"),
            ("aoob-ui", "57"),
            ("RSA_SS6_Backend", "506")
        ]

    def assign_all_issues(self):
        """Assign all existing security issues to OPL Management project."""
        print("🔧 Automatic GitHub Project Assignment via GraphQL")
        print(f"📅 Started: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') if 'pd' in globals() else 'Now'}")
        print(f"🏢 Organization: {self.org_name}")
        print(f"📋 Project: OPL Management (#{self.project_number})")
        print(f"🌐 GraphQL Endpoint: {self.graphql_url}")
        print("=" * 70)
        
        if not self.github_token:
            print("❌ Error: GITHUB_TOKEN not found in environment")
            print("Please check your .env file")
            return False

        # Get project ID first
        print("🔍 Getting project information...")
        project_id = self.get_project_id()
        if not project_id:
            return False

        issues_to_assign = self.get_issues_to_assign()
        total_assigned = 0
        total_failed = 0

        print(f"\n🔧 Assigning {len(issues_to_assign)} issues to project...")

        for repo_name, issue_number in issues_to_assign:
            print(f"\n📋 Processing {repo_name} issue #{issue_number}...")
            
            # Get issue node ID
            issue_node_id = self.get_issue_node_id(repo_name, issue_number)
            if not issue_node_id:
                total_failed += 1
                continue
            
            # Add issue to project
            success = self.add_issue_to_project(project_id, issue_node_id)
            if success:
                total_assigned += 1
            else:
                total_failed += 1

        print("\n" + "=" * 70)
        print("📊 ASSIGNMENT SUMMARY")
        print("=" * 70)
        print(f"📁 Issues Processed: {len(issues_to_assign)}")
        print(f"✅ Issues Assigned: {total_assigned}")
        print(f"❌ Assignment Failures: {total_failed}")
        print("=" * 70)

        if total_assigned > 0:
            print(f"\n🎉 Successfully assigned {total_assigned} issues to OPL Management!")
            print(f"🌐 View project: {self.base_url}/orgs/{self.org_name}/projects/{self.project_number}")

        if total_failed > 0:
            print(f"\n⚠️  {total_failed} issues failed assignment")

        return total_assigned > 0

def main():
    """Main function."""
    try:
        assigner = GraphQLProjectAssigner()
        success = assigner.assign_all_issues()
        
        if not success:
            print("\n❌ Assignment failed or no issues were assigned")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Assignment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Assignment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()