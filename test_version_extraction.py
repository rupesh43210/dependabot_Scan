#!/usr/bin/env python3
"""
Quick test for current version extraction improvements
"""

from vulnerability_scanner import VulnerabilityScanner
import os
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
scanner = VulnerabilityScanner(github_token)

# Test with a single repository to see current version extraction
print('Testing current version extraction improvements...')
vulns = scanner.get_repository_vulnerabilities('MiDAS', 'MiDAS-Platform')
if vulns:
    print(f'Found {len(vulns)} vulnerabilities')
    for i, vuln in enumerate(vulns[:5]):  # Test first 5
        current_version = vuln.get('current_version', 'Not extracted')
        package_name = vuln.get('package_name', 'Unknown')
        ecosystem = vuln.get('ecosystem', 'Unknown')
        print(f'{i+1}. Package: {package_name} ({ecosystem}) - Current: {current_version}')
else:
    print('No vulnerabilities found for testing')