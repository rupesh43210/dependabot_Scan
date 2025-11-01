#!/usr/bin/env python3
"""
MiDAS Complete Security Pipeline - Enhanced Version

Complete end-to-end security vulnerability assessment pipeline
for GitHub Enterprise MiDAS organization with advanced analytics,
compliance reporting, and comprehensive visualizations.

Features:
- Enhanced vulnerability scanning with lifecycle tracking
- Advanced analytics and trend analysis
- Compliance reporting (OWASP Top 10, etc.)
- Interactive risk matrices and dashboards
- Executive and technical reporting
- Security KPIs and performance scorecards

Author: GitHub Copilot
Version: 2.1.0
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Check if virtual environment is activated, if not try to activate it
def ensure_venv():
    """Ensure virtual environment is activated."""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Not in virtual environment
        venv_path = Path(__file__).parent / "venv"
        if venv_path.exists():
            if os.name == 'nt':  # Windows
                activate_script = venv_path / "Scripts" / "python.exe"
                if activate_script.exists():
                    print("🔄 Virtual environment not active. Restarting with venv...")
                    subprocess.run([str(activate_script), __file__] + sys.argv[1:])
                    sys.exit(0)
            else:  # Unix/Linux
                activate_script = venv_path / "bin" / "python"
                if activate_script.exists():
                    print("🔄 Virtual environment not active. Restarting with venv...")
                    subprocess.run([str(activate_script), __file__] + sys.argv[1:])
                    sys.exit(0)
        print("⚠️ Virtual environment not found or not properly set up")

# Ensure venv is activated
ensure_venv()

from vulnerability_scanner import VulnerabilityScanner
from security_report_generator import SecurityReportGenerator


class MiDASSecurityPipeline:
    """
    Complete security assessment pipeline for MiDAS organization.
    
    Features:
    - End-to-end vulnerability scanning
    - Professional report generation
    - Automated cleanup
    - Risk-based prioritization
    - Executive and technical reporting
    """
    
    def __init__(self, github_token: str, org_name: str = "MiDAS"):
        """
        Initialize the security pipeline.
        
        Args:
            github_token: GitHub Enterprise personal access token
            org_name: Organization name to scan
        """
        self.github_token = github_token
        self.org_name = org_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_files = []
        
        # Initialize components
        self.scanner = VulnerabilityScanner(github_token)
        self.report_generator = SecurityReportGenerator()
    
    def run_vulnerability_scan(self) -> bool:
        """
        Execute comprehensive vulnerability scan.
        
        Returns:
            True if scan completed successfully
        """
        print("🔍 STEP 1: VULNERABILITY SCANNING")
        print("=" * 70)
        
        # Scan organization
        vulnerabilities = self.scanner.scan_organization(self.org_name)
        
        if not vulnerabilities:
            print("❌ No vulnerabilities found or scan failed")
            return False
        
        # Save scan results
        json_file, csv_file = self.scanner.save_results(vulnerabilities, self.timestamp)
        self.temp_files.extend([json_file, csv_file])
        
        # Save vulnerability summary
        summary_file = f"temp_vulnerability_summary_{self.timestamp}.json"
        self._save_vulnerability_summary(vulnerabilities, summary_file)
        self.temp_files.append(summary_file)
        
        return True
    
    def _save_vulnerability_summary(self, vulnerabilities: list, filename: str):
        """Save vulnerability summary statistics."""
        import json
        
        # Calculate summary statistics
        summary = {
            'scan_timestamp': self.timestamp,
            'total_vulnerabilities': len(vulnerabilities),
            'repositories_scanned': self.scanner.stats['repositories_scanned'],
            'repositories_with_vulnerabilities': self.scanner.stats['repositories_with_vulnerabilities'],
            'severity_breakdown': {},
            'top_vulnerable_repos': {}
        }
        
        # Severity breakdown
        severities = [v.get('severity', 'UNKNOWN') for v in vulnerabilities]
        for severity in set(severities):
            summary['severity_breakdown'][severity] = severities.count(severity)
        
        # Top vulnerable repositories
        repo_counts = {}
        for vuln in vulnerabilities:
            repo = vuln.get('repository', 'Unknown')
            repo_counts[repo] = repo_counts.get(repo, 0) + 1
        
        # Sort and take top 10
        sorted_repos = sorted(repo_counts.items(), key=lambda x: x[1], reverse=True)
        summary['top_vulnerable_repos'] = dict(sorted_repos[:10])
        
        # Save summary
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
    
    def generate_security_reports(self) -> Optional[str]:
        """
        Generate comprehensive security reports with enhanced analytics.
        
        Returns:
            Path to generated reports directory
        """
        print("\n📊 STEP 2: ENHANCED SECURITY REPORT GENERATION")
        print("=" * 70)
        
        # Load vulnerability data
        json_file = f"temp_vulnerabilities_{self.timestamp}.json"
        if not self.report_generator.load_vulnerability_data(json_file):
            print("❌ Failed to load vulnerability data for reporting")
            return None
        
        # Generate all reports using enhanced generator
        try:
            # Generate both types of executive summaries
            repo_executive_df = self.report_generator.generate_repository_executive_summary()
            enhanced_executive_df = self.report_generator.generate_executive_summary()
            detailed_df = self.report_generator.generate_detailed_report()
            
            if repo_executive_df.empty and enhanced_executive_df.empty and detailed_df.empty:
                print("⚠️  No data available for report generation")
                return None
            
            # Save comprehensive reports
            reports_dir = self.report_generator.save_reports(repo_executive_df, enhanced_executive_df, detailed_df)
            
            if not reports_dir:
                print("⚠️  Failed to save reports")
                return None
            
            print(f"\n✅ Comprehensive security reports generated successfully!")
            print(f"📁 Reports location: {reports_dir}")
            
            # Print summary of generated reports
            print("\n📋 Generated Report Suite:")
            report_descriptions = {
                'executive_summary.xlsx': '📈 Multi-sheet executive workbook (Repository Summary + Enhanced Analytics + Dashboard)',
                'executive_summary.csv': '📊 Repository-focused executive summary',
                'executive_kpi_summary.csv': '🎯 Enhanced KPI and metrics summary',
                'detailed_vulnerabilities.xlsx': '🔍 Complete vulnerability inventory with severity sheets', 
                'detailed_vulnerabilities.csv': '📄 Complete vulnerability inventory'
            }
            
            reports_path = Path(reports_dir)
            for report_file in reports_path.glob('*'):
                if report_file.is_file():
                    description = report_descriptions.get(report_file.name, '📄 Additional report file')
                    print(f"  • {report_file.name} - {description}")
            
            return reports_dir
            
        except Exception as e:
            print(f"❌ Error generating enhanced reports: {e}")
            return None

    def _archive_source_data(self, reports_dir: str):
        """Archive source data files in the reports directory."""
        import shutil
        
        reports_path = Path(reports_dir)
        source_data_dir = reports_path / "source_data"
        source_data_dir.mkdir(exist_ok=True)
        
        # Copy source files
        for temp_file in self.temp_files:
            if Path(temp_file).exists():
                # Remove timestamp from filename for clean archive
                clean_name = temp_file.replace(f"_{self.timestamp}", "")
                dest_path = source_data_dir / clean_name
                shutil.copy2(temp_file, dest_path)
        
        print(f"📁 Source data archived in: {source_data_dir}")
    
    def cleanup_temporary_files(self):
        """Clean up temporary files generated during the scan."""
        print("\n🧹 STEP 3: CLEANUP")
        print("=" * 70)
        
        cleaned_count = 0
        for temp_file in self.temp_files:
            try:
                if Path(temp_file).exists():
                    Path(temp_file).unlink()
                    print(f"🗑️  Removed: {temp_file}")
                    cleaned_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {temp_file}: {e}")
        
        print(f"✅ Cleaned up {cleaned_count} temporary files")
    
    def print_final_summary(self, reports_dir: Optional[str]):
        """Print final pipeline summary."""
        print("\n" + "=" * 70)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
        # Security posture summary
        stats = self.scanner.stats
        print("📊 **SECURITY POSTURE SUMMARY**")
        print(f"   Total Open Vulnerabilities: {stats.get('vulnerabilities_found', 0)}")
        
        # Load executive summary for critical stats
        if reports_dir:
            try:
                import pandas as pd
                exec_file = Path(reports_dir) / "executive_summary.csv"
                if exec_file.exists():
                    exec_df = pd.read_csv(exec_file)
                    if not exec_df.empty:
                        critical = exec_df['Critical'].sum()
                        high = exec_df['High'].sum()
                        repos_analyzed = len(exec_df)
                        
                        print(f"   Critical Issues: {critical}")
                        print(f"   High Severity Issues: {high}")
                        print(f"   Repositories Analyzed: {repos_analyzed}")
                        
                        print(f"\n📁 **REPORTS LOCATION**")
                        print(f"   {reports_dir}")
                        
                        if critical > 0 or high > 0:
                            print(f"\n🎯 **IMMEDIATE ACTIONS REQUIRED**")
                            if critical > 0:
                                print(f"   🚨 URGENT: {critical} critical vulnerabilities need immediate attention")
                            if high > 0:
                                print(f"   ⚠️  HIGH PRIORITY: {high} high-severity issues require prompt remediation")
                        
                        # Top risk repositories
                        if len(exec_df) > 0:
                            print(f"\n📈 **TOP RISK REPOSITORIES**")
                            top_repos = exec_df.head(3)
                            for idx, row in top_repos.iterrows():
                                risk_emoji = "🚨" if row['Risk Score'] > 100 else "⚠️" if row['Risk Score'] > 50 else "📊"
                                print(f"   {idx + 1}. {risk_emoji} {row['Repository Name']} (Risk Score: {row['Risk Score']})")
            except Exception as e:
                print(f"   Could not load detailed summary: {e}")
        
        print(f"\n✅ Pipeline completed in {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def run_complete_pipeline(self) -> bool:
        """
        Execute the complete security assessment pipeline.
        
        Returns:
            True if pipeline completed successfully
        """
        print("🚀 Starting MiDAS Complete Security Assessment Pipeline")
        print(f"📅 Timestamp: {self.timestamp}")
        print("=" * 70)
        
        try:
            # Step 1: Vulnerability Scanning
            if not self.run_vulnerability_scan():
                return False
            
            # Step 2: Report Generation
            reports_dir = self.generate_security_reports()
            
            # Step 3: Cleanup
            self.cleanup_temporary_files()
            
            # Final Summary
            self.print_final_summary(reports_dir)
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Pipeline interrupted by user")
            self.cleanup_temporary_files()
            return False
        except Exception as e:
            print(f"\n❌ Pipeline failed with error: {e}")
            self.cleanup_temporary_files()
            return False


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub Enterprise token in the .env file")
        sys.exit(1)
    
    # Get organization name (default to MiDAS)
    org_name = os.getenv('GITHUB_ORG', 'MiDAS')
    
    # Initialize and run pipeline
    pipeline = MiDASSecurityPipeline(github_token, org_name)
    
    success = pipeline.run_complete_pipeline()
    
    if success:
        print("\n🎉 Security assessment completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Security assessment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()