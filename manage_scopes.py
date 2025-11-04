#!/usr/bin/env python3
"""
Repository Scope Management Utility

Simple utility to manage repository scopes for vulnerability scanning.

Usage:
  python manage_scopes.py --list                    # List all scopes
  python manage_scopes.py --show RQA                # Show specific scope
  python manage_scopes.py --set-active RQA          # Set active scope
  python manage_scopes.py --add-scope "release-1.2" # Add new scope
"""

import argparse
import sys
from repository_scope_manager import RepositoryScopeManager


def main():
    parser = argparse.ArgumentParser(
        description="Repository Scope Management Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--list', action='store_true', help='List all available scopes')
    parser.add_argument('--show', metavar='SCOPE', help='Show details for a specific scope')
    parser.add_argument('--set-active', metavar='SCOPE', help='Set the active scope')
    parser.add_argument('--add-repo', nargs=2, metavar=('SCOPE', 'REPO'), help='Add repository to scope')
    parser.add_argument('--remove-repo', nargs=2, metavar=('SCOPE', 'REPO'), help='Remove repository from scope')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    
    scope_manager = RepositoryScopeManager()
    
    if args.list:
        scope_manager.print_scope_info()
    
    elif args.show:
        scope_manager.print_scope_info(args.show)
    
    elif args.set_active:
        if scope_manager.set_active_scope(args.set_active):
            print(f"✅ Active scope set to: {args.set_active}")
        else:
            sys.exit(1)
    
    elif args.add_repo:
        scope_name, repo_name = args.add_repo
        scope_manager.add_repository_to_scope(scope_name, repo_name)
    
    elif args.remove_repo:
        scope_name, repo_name = args.remove_repo
        scope_manager.remove_repository_from_scope(scope_name, repo_name)


if __name__ == "__main__":
    main()