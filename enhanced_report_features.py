#!/usr/bin/env python3
"""
Enhanced Report Features for MiDAS Security Pipeline

Additional reporting capabilities including compliance mapping,
trend analysis, and advanced visualizations.

Author: GitHub Copilot
Version: 2.1.0
"""

from typing import Dict, List, Tuple
import pandas as pd
import json
from datetime import datetime, timedelta


class ComplianceReporter:
    """Generate compliance reports for various security frameworks."""
    
    # OWASP Top 10 mapping
    OWASP_MAPPING = {
        'npm': 'A06:2021 - Vulnerable and Outdated Components',
        'pip': 'A06:2021 - Vulnerable and Outdated Components',
        'bundler': 'A06:2021 - Vulnerable and Outdated Components',
        'maven': 'A06:2021 - Vulnerable and Outdated Components',
        'nuget': 'A06:2021 - Vulnerable and Outdated Components',
        'composer': 'A06:2021 - Vulnerable and Outdated Components',
    }
    
    def __init__(self, vulnerability_data: pd.DataFrame):
        self.data = vulnerability_data
    
    def generate_owasp_compliance_report(self) -> Dict:
        """Generate OWASP Top 10 compliance report."""
        compliance_data = {
            'framework': 'OWASP Top 10 2021',
            'scan_date': datetime.now().isoformat(),
            'total_vulnerabilities': len(self.data),
            'compliance_categories': {}
        }
        
        # Map vulnerabilities to OWASP categories
        for ecosystem in self.data['package_ecosystem'].unique():
            if ecosystem in self.OWASP_MAPPING:
                category = self.OWASP_MAPPING[ecosystem]
                ecosystem_vulns = self.data[self.data['package_ecosystem'] == ecosystem]
                
                if category not in compliance_data['compliance_categories']:
                    compliance_data['compliance_categories'][category] = {
                        'vulnerability_count': 0,
                        'open_vulnerabilities': 0,
                        'critical_count': 0,
                        'high_count': 0,
                        'affected_repositories': set()
                    }
                
                compliance_data['compliance_categories'][category]['vulnerability_count'] += len(ecosystem_vulns)
                compliance_data['compliance_categories'][category]['open_vulnerabilities'] += len(
                    ecosystem_vulns[ecosystem_vulns['alert_state'] == 'open']
                )
                compliance_data['compliance_categories'][category]['critical_count'] += len(
                    ecosystem_vulns[ecosystem_vulns['severity'] == 'CRITICAL']
                )
                compliance_data['compliance_categories'][category]['high_count'] += len(
                    ecosystem_vulns[ecosystem_vulns['severity'] == 'HIGH']
                )
                compliance_data['compliance_categories'][category]['affected_repositories'].update(
                    ecosystem_vulns['repository'].unique()
                )
        
        # Convert sets to counts
        for category in compliance_data['compliance_categories']:
            compliance_data['compliance_categories'][category]['affected_repositories'] = len(
                compliance_data['compliance_categories'][category]['affected_repositories']
            )
        
        return compliance_data


class TrendAnalyzer:
    """Analyze vulnerability trends and patterns."""
    
    def __init__(self, vulnerability_data: pd.DataFrame):
        self.data = vulnerability_data
    
    def analyze_discovery_patterns(self) -> Dict:
        """Analyze vulnerability discovery patterns."""
        if 'alert_created_at' not in self.data.columns:
            return {'error': 'No creation date data available'}
        
        # Convert dates and analyze patterns
        self.data['created_date'] = pd.to_datetime(self.data['alert_created_at'], errors='coerce')
        
        # Monthly discovery trends
        monthly_discoveries = self.data.groupby(
            self.data['created_date'].dt.to_period('M')
        ).size().to_dict()
        
        # Severity trends over time
        severity_trends = {}
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_data = self.data[self.data['severity'] == severity]
            severity_trends[severity] = severity_data.groupby(
                severity_data['created_date'].dt.to_period('M')
            ).size().to_dict()
        
        return {
            'monthly_discoveries': {str(k): v for k, v in monthly_discoveries.items()},
            'severity_trends': {
                severity: {str(k): v for k, v in trends.items()}
                for severity, trends in severity_trends.items()
            },
            'peak_discovery_month': max(monthly_discoveries, key=monthly_discoveries.get) if monthly_discoveries else None,
            'total_discovery_months': len(monthly_discoveries)
        }
    
    def analyze_resolution_velocity(self) -> Dict:
        """Analyze how quickly vulnerabilities are being resolved."""
        if 'days_to_resolution' not in self.data.columns:
            return {'error': 'No resolution time data available'}
        
        resolved_vulns = self.data[self.data['days_to_resolution'].notna()]
        
        if resolved_vulns.empty:
            return {'error': 'No resolved vulnerabilities with timing data'}
        
        # Velocity by severity
        velocity_by_severity = {}
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_vulns = resolved_vulns[resolved_vulns['severity'] == severity]
            if not severity_vulns.empty:
                velocity_by_severity[severity] = {
                    'average_days': round(severity_vulns['days_to_resolution'].mean(), 1),
                    'median_days': round(severity_vulns['days_to_resolution'].median(), 1),
                    'fastest_resolution': severity_vulns['days_to_resolution'].min(),
                    'slowest_resolution': severity_vulns['days_to_resolution'].max(),
                    'count': len(severity_vulns)
                }
        
        return {
            'overall_metrics': {
                'average_resolution_days': round(resolved_vulns['days_to_resolution'].mean(), 1),
                'median_resolution_days': round(resolved_vulns['days_to_resolution'].median(), 1),
                'total_resolved': len(resolved_vulns)
            },
            'velocity_by_severity': velocity_by_severity,
            'sla_compliance': self._calculate_sla_compliance(resolved_vulns)
        }
    
    def _calculate_sla_compliance(self, resolved_vulns: pd.DataFrame) -> Dict:
        """Calculate SLA compliance based on standard security timelines."""
        sla_targets = {
            'CRITICAL': 7,   # 7 days
            'HIGH': 30,      # 30 days
            'MEDIUM': 90,    # 90 days
            'LOW': 180       # 180 days
        }
        
        compliance = {}
        for severity, target_days in sla_targets.items():
            severity_vulns = resolved_vulns[resolved_vulns['severity'] == severity]
            if not severity_vulns.empty:
                within_sla = len(severity_vulns[severity_vulns['days_to_resolution'] <= target_days])
                compliance[severity] = {
                    'target_days': target_days,
                    'total_resolved': len(severity_vulns),
                    'within_sla': within_sla,
                    'compliance_rate': round((within_sla / len(severity_vulns)) * 100, 1)
                }
        
        return compliance


class RiskAnalyzer:
    """Advanced risk analysis and scoring."""
    
    def __init__(self, vulnerability_data: pd.DataFrame):
        self.data = vulnerability_data
    
    def calculate_repository_risk_matrix(self) -> pd.DataFrame:
        """Create a risk matrix for all repositories."""
        risk_matrix = []
        
        for repo in self.data['repository'].unique():
            repo_data = self.data[self.data['repository'] == repo]
            open_vulns = repo_data[repo_data['alert_state'] == 'open']
            
            # Calculate various risk metrics
            risk_score = sum(
                self._get_severity_weight(vuln['severity']) for _, vuln in open_vulns.iterrows()
            )
            
            # Calculate vulnerability density
            total_vulns = len(repo_data)
            vuln_density = total_vulns / max(repo_data['package_name'].nunique(), 1) if 'package_name' in repo_data.columns else total_vulns
            
            # Calculate aging factor
            aging_factor = 0
            if 'vulnerability_age_days' in open_vulns.columns:
                avg_age = open_vulns['vulnerability_age_days'].mean()
                aging_factor = min(avg_age / 365, 2.0) if not pd.isna(avg_age) else 0  # Cap at 2x for 1+ year old
            
            # Determine risk level
            risk_level = self._determine_risk_level(risk_score, len(open_vulns), aging_factor)
            
            risk_matrix.append({
                'Repository': repo,
                'Open_Vulnerabilities': len(open_vulns),
                'Total_Vulnerabilities': total_vulns,
                'Risk_Score': risk_score,
                'Vulnerability_Density': round(vuln_density, 2),
                'Average_Age_Days': round(open_vulns['vulnerability_age_days'].mean(), 1) if 'vulnerability_age_days' in open_vulns.columns and not open_vulns.empty else 0,
                'Critical_Count': len(open_vulns[open_vulns['severity'] == 'CRITICAL']),
                'High_Count': len(open_vulns[open_vulns['severity'] == 'HIGH']),
                'Medium_Count': len(open_vulns[open_vulns['severity'] == 'MEDIUM']),
                'Low_Count': len(open_vulns[open_vulns['severity'] == 'LOW']),
                'Risk_Level': risk_level,
                'Priority_Rank': risk_score + (aging_factor * 10)  # Boost priority for aged vulnerabilities
            })
        
        # Sort by priority rank
        risk_df = pd.DataFrame(risk_matrix)
        if not risk_df.empty:
            risk_df = risk_df.sort_values('Priority_Rank', ascending=False)
            risk_df['Rank'] = range(1, len(risk_df) + 1)
        
        return risk_df
    
    def _get_severity_weight(self, severity: str) -> int:
        """Get severity weight for risk calculations."""
        weights = {'CRITICAL': 50, 'HIGH': 20, 'MEDIUM': 5, 'LOW': 1}
        return weights.get(severity, 1)
    
    def _determine_risk_level(self, risk_score: float, vuln_count: int, aging_factor: float) -> str:
        """Determine overall risk level for a repository."""
        # Adjust risk score based on aging
        adjusted_score = risk_score * (1 + aging_factor)
        
        if adjusted_score >= 100 or vuln_count >= 10:
            return 'CRITICAL'
        elif adjusted_score >= 50 or vuln_count >= 5:
            return 'HIGH'
        elif adjusted_score >= 20 or vuln_count >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'


class SecurityMetrics:
    """Calculate advanced security metrics and KPIs."""
    
    def __init__(self, vulnerability_data: pd.DataFrame):
        self.data = vulnerability_data
    
    def calculate_security_kpis(self) -> Dict:
        """Calculate key security performance indicators."""
        total_vulns = len(self.data)
        open_vulns = self.data[self.data['alert_state'] == 'open']
        resolved_vulns = self.data[self.data['alert_state'].isin(['fixed', 'dismissed'])]
        
        kpis = {
            'vulnerability_management': {
                'total_vulnerabilities': total_vulns,
                'open_vulnerabilities': len(open_vulns),
                'resolution_rate': round((len(resolved_vulns) / total_vulns) * 100, 1) if total_vulns > 0 else 0,
                'mean_time_to_resolution': round(resolved_vulns['days_to_resolution'].mean(), 1) if 'days_to_resolution' in resolved_vulns.columns else 0,
                'vulnerability_backlog': len(open_vulns)
            },
            'risk_metrics': {
                'critical_exposure': len(open_vulns[open_vulns['severity'] == 'CRITICAL']),
                'high_exposure': len(open_vulns[open_vulns['severity'] == 'HIGH']),
                'average_cvss': round(self.data['cvss_score'].mean(), 2) if 'cvss_score' in self.data.columns else 0,
                'repositories_at_risk': len(open_vulns['repository'].unique())
            },
            'operational_metrics': {
                'scanned_repositories': self.data['repository'].nunique(),
                'vulnerable_packages': self.data['package_name'].nunique() if 'package_name' in self.data.columns else 0,
                'ecosystems_covered': self.data['package_ecosystem'].nunique() if 'package_ecosystem' in self.data.columns else 0
            }
        }
        
        # Calculate trends if historical data is available
        if 'alert_created_at' in self.data.columns:
            kpis['trend_indicators'] = self._calculate_trend_indicators()
        
        return kpis
    
    def _calculate_trend_indicators(self) -> Dict:
        """Calculate trend indicators for vulnerability patterns."""
        # This would be enhanced with historical data comparison
        current_month = datetime.now().replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        
        # Placeholder for trend calculations
        return {
            'new_vulnerabilities_trend': 'stable',  # Would calculate from historical data
            'resolution_velocity_trend': 'improving',
            'risk_exposure_trend': 'decreasing',
            'note': 'Trend analysis requires historical data comparison'
        }
    
    def generate_security_scorecard(self) -> Dict:
        """Generate a comprehensive security scorecard."""
        kpis = self.calculate_security_kpis()
        
        # Calculate grades based on industry benchmarks
        scorecard = {
            'overall_grade': self._calculate_overall_grade(kpis),
            'category_grades': {
                'vulnerability_management': self._grade_vuln_management(kpis['vulnerability_management']),
                'risk_exposure': self._grade_risk_exposure(kpis['risk_metrics']),
                'operational_coverage': self._grade_operational_metrics(kpis['operational_metrics'])
            },
            'improvement_areas': self._identify_improvement_areas(kpis),
            'strengths': self._identify_strengths(kpis)
        }
        
        return scorecard
    
    def _calculate_overall_grade(self, kpis: Dict) -> str:
        """Calculate overall security grade."""
        # Simplified grading logic - would be more sophisticated in production
        resolution_rate = kpis['vulnerability_management']['resolution_rate']
        critical_exposure = kpis['risk_metrics']['critical_exposure']
        
        if resolution_rate >= 90 and critical_exposure == 0:
            return 'A'
        elif resolution_rate >= 80 and critical_exposure <= 2:
            return 'B'
        elif resolution_rate >= 70 and critical_exposure <= 5:
            return 'C'
        elif resolution_rate >= 60:
            return 'D'
        else:
            return 'F'
    
    def _grade_vuln_management(self, vm_metrics: Dict) -> str:
        """Grade vulnerability management practices."""
        resolution_rate = vm_metrics['resolution_rate']
        
        if resolution_rate >= 95:
            return 'A+'
        elif resolution_rate >= 90:
            return 'A'
        elif resolution_rate >= 80:
            return 'B'
        elif resolution_rate >= 70:
            return 'C'
        else:
            return 'D'
    
    def _grade_risk_exposure(self, risk_metrics: Dict) -> str:
        """Grade current risk exposure."""
        critical = risk_metrics['critical_exposure']
        high = risk_metrics['high_exposure']
        
        if critical == 0 and high <= 2:
            return 'A'
        elif critical <= 1 and high <= 5:
            return 'B'
        elif critical <= 3 and high <= 10:
            return 'C'
        else:
            return 'D'
    
    def _grade_operational_metrics(self, op_metrics: Dict) -> str:
        """Grade operational coverage and practices."""
        # Simple grading based on coverage
        repos = op_metrics['scanned_repositories']
        ecosystems = op_metrics['ecosystems_covered']
        
        if repos >= 50 and ecosystems >= 5:
            return 'A'
        elif repos >= 20 and ecosystems >= 3:
            return 'B'
        elif repos >= 10 and ecosystems >= 2:
            return 'C'
        else:
            return 'D'
    
    def _identify_improvement_areas(self, kpis: Dict) -> List[str]:
        """Identify key areas for improvement."""
        areas = []
        
        vm = kpis['vulnerability_management']
        risk = kpis['risk_metrics']
        
        if vm['resolution_rate'] < 80:
            areas.append('Improve vulnerability resolution processes')
        
        if risk['critical_exposure'] > 0:
            areas.append('Address critical severity vulnerabilities immediately')
        
        if vm['mean_time_to_resolution'] > 60:
            areas.append('Reduce time to vulnerability resolution')
        
        if risk['high_exposure'] > 10:
            areas.append('Prioritize high severity vulnerability remediation')
        
        return areas
    
    def _identify_strengths(self, kpis: Dict) -> List[str]:
        """Identify organizational strengths."""
        strengths = []
        
        vm = kpis['vulnerability_management']
        risk = kpis['risk_metrics']
        op = kpis['operational_metrics']
        
        if vm['resolution_rate'] >= 90:
            strengths.append('Excellent vulnerability resolution rate')
        
        if risk['critical_exposure'] == 0:
            strengths.append('No critical vulnerabilities in production')
        
        if op['scanned_repositories'] >= 50:
            strengths.append('Comprehensive repository coverage')
        
        if vm['mean_time_to_resolution'] <= 30:
            strengths.append('Fast vulnerability response times')
        
        return strengths