#!/usr/bin/env python3
"""
Test GitHub API access and token permissions
"""
import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
username = 'rupesh43210'

print("🔍 Testing GitHub API Access")
print("=" * 70)

try:
    # Initialize GitHub client
    g = Github(token)
    
    # Test 1: Get authenticated user
    print("\n1️⃣  Testing authentication...")
    try:
        auth_user = g.get_user()
        print(f"   ✅ Authenticated as: {auth_user.login}")
        print(f"   Name: {auth_user.name}")
        print(f"   Email: {auth_user.email}")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        exit(1)
    
    # Test 2: Get user by username
    print(f"\n2️⃣  Testing access to user '{username}'...")
    try:
        user = g.get_user(username)
        print(f"   ✅ User found: {user.login}")
        print(f"   Name: {user.name}")
        print(f"   Public repos: {user.public_repos}")
    except Exception as e:
        print(f"   ❌ Failed to get user: {e}")
    
    # Test 3: List repositories
    print(f"\n3️⃣  Testing repository access...")
    try:
        repos = list(user.get_repos(type='all'))
        print(f"   ✅ Found {len(repos)} repositories:")
        for i, repo in enumerate(repos[:10], 1):
            print(f"      {i}. {repo.name} ({'private' if repo.private else 'public'})")
        if len(repos) > 10:
            print(f"      ... and {len(repos) - 10} more")
    except Exception as e:
        print(f"   ❌ Failed to list repositories: {e}")
    
    # Test 4: Check token scopes
    print(f"\n4️⃣  Checking token scopes...")
    try:
        rate_limit = g.get_rate_limit()
        print(f"   Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
        
        # Try to access a private repo (if token has repo scope)
        print(f"\n5️⃣  Testing Dependabot alerts access...")
        if repos:
            test_repo = repos[0]
            print(f"   Testing with repository: {test_repo.name}")
            try:
                # This requires security_events scope
                import requests
                headers = {
                    'Authorization': f'token {token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                url = f"https://api.github.com/repos/{username}/{test_repo.name}/dependabot/alerts"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    alerts = response.json()
                    print(f"   ✅ Can access Dependabot alerts: {len(alerts)} alerts found")
                elif response.status_code == 404:
                    print(f"   ⚠️  Repository not found or Dependabot not enabled")
                elif response.status_code == 403:
                    print(f"   ❌ Permission denied - Token needs 'security_events' scope")
                else:
                    print(f"   ⚠️  Response code: {response.status_code}")
                    print(f"   Message: {response.text[:200]}")
            except Exception as e:
                print(f"   ❌ Error testing Dependabot access: {e}")
    except Exception as e:
        print(f"   ❌ Error checking scopes: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Test completed!")
    
except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    exit(1)
