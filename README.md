# 🛡️ Security Vulnerability Scanner v2.1

A professional, enterprise-grade vulnerability assessment pipeline for GitHub organizations and personal accounts. This optimized system provides comprehensive security scanning, intelligent reporting, and risk-based prioritization with advanced analytics.

![Pipeline Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Enterprise-orange)

## 🚀 Features

### 🔍 Core Capabilities
- **🔐 Complete Vulnerability Scanning**: Automated Dependabot alert extraction from all repositories
- **👤 Personal & Enterprise Support**: Works with both personal GitHub accounts and organizations
- **🧠 Intelligent CVSS Scoring**: Smart fallback scoring for missing CVSS values with severity-based estimates
- **📊 Professional Reporting**: Executive summaries, detailed technical reports, and trend analysis
- **⚡ Risk-Based Prioritization**: Automated risk scoring, ranking, and vulnerability lifecycle tracking
- **📈 Advanced Analytics**: Vulnerability trends, resolution metrics, and compliance dashboards
- **📋 Excel Integration**: Professional formatting with conditional coloring and interactive charts
- **🏢 Enterprise-Ready**: Production-grade with comprehensive error handling and audit trails

### 🎯 Advanced Features
- **📝 Comprehensive Logging**: Detailed audit trails for compliance and debugging
- **🧹 Automated Cleanup**: Intelligent temporary file management
- **📦 Source Data Archiving**: Complete traceability and historical data preservation
- **📊 Multi-format Output**: CSV, Excel, and JSON reports for different stakeholders
- **⏱️ Rate Limiting Protection**: Intelligent GitHub API rate limit management
- **✅ Environment Validation**: Comprehensive setup verification and health checks
- **🔄 Vulnerability Lifecycle Tracking**: Resolution dates, dismissal tracking, and aging analysis
- **📈 Trend Analysis**: Historical vulnerability patterns and remediation effectiveness
- **🎨 Interactive Dashboards**: Rich visualizations and executive-friendly summaries

## 📁 Project Structure

```
security-vuln-scanner/
├── vulnerability_scanner.py      # Core vulnerability scanning engine
├── security_report_generator.py  # Professional report generation
├── security_pipeline.py          # Complete end-to-end pipeline
├── setup_env.py                  # Interactive environment setup
├── requirements.txt              # Python dependencies
├── .env.sample                   # Environment configuration template
├── .gitignore                    # Git ignore rules
└── README.md                     # Documentation
```
├── .env                         # Environment configuration (create from template)
├── reports/                     # Generated reports directory
├── logs/                        # Application logs
└── README.md                    # This file
```

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- GitHub personal access token (with `repo` and `security_events` scopes)
- Access to your GitHub personal account or organization

### 2. Quick Setup (Automated)
```bash
# Clone or download the repository
cd security-vuln-scanner

# Configure environment (interactive)
python setup_env.py

# Run pipeline (auto-creates venv and installs dependencies)
python security_pipeline.py
```

**That's it!** The pipeline automatically:
- Creates virtual environment if needed
- Installs all required dependencies
- Runs the complete security assessment

### 3. Environment Configuration

The scanner supports both **personal GitHub accounts** and **enterprise organizations**. Create a `.env` file based on your use case:

#### Option A: Personal GitHub Account

```env
# GitHub Personal Access Token (required)
# Get yours at: https://github.com/settings/tokens
# Required scopes: repo, security_events
GITHUB_TOKEN=ghp_your_personal_access_token

# Your GitHub profile URL (required for personal accounts)
GITHUB_URL=https://github.com/your-username

# Leave GITHUB_ORG commented out for personal accounts
# GITHUB_ORG=
```

#### Option B: GitHub Organization

```env
# GitHub Personal Access Token (required)
GITHUB_TOKEN=ghp_your_personal_access_token

# Organization name (required for organizations)
GITHUB_ORG=your-organization-name

# Optional: GITHUB_URL (not needed for organizations)
# GITHUB_URL=https://github.com/your-organization
```

#### Option C: GitHub Enterprise Server

```env
# GitHub Enterprise Token (required)
GITHUB_TOKEN=your_github_enterprise_token

# Organization name (required)
GITHUB_ORG=your-organization

# GitHub Enterprise base URL (required for Enterprise)
GITHUB_ENTERPRISE_URL=https://github.your-company.com
```

### 4. Getting Your GitHub Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token" (classic)
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `security_events` (Read Dependabot alerts)
4. Generate and copy the token
5. Add it to your `.env` file

## 🎯 Usage

### Quick Start

```bash
# Simply run the pipeline - it will auto-setup everything needed
python security_pipeline.py
```

The scanner will automatically:
- Detect if you're using a personal account or organization
- Scan all accessible repositories
- Generate comprehensive security reports
- Create a clean summary if no vulnerabilities are found

### What the Pipeline Does

**For Personal Accounts:**
- Scans all repositories under your GitHub username
- Checks for Dependabot security alerts
- Generates reports or a "clean bill of health" summary

**For Organizations:**
- Scans all repositories in the organization
- Aggregates security alerts across all repos
- Provides executive summaries and detailed technical reports

### Automated Setup & Execution
The pipeline automatically handles virtual environment creation and dependency installation:

**What happens automatically:**
1. 🔍 Checks if virtual environment exists
2. 📦 Creates `venv/` directory if missing
3. 📋 Installs all dependencies from `requirements.txt`
4. 🔄 Activates virtual environment
5. 🚀 Runs the complete security assessment
6. 📊 Generates reports based on findings

### Manual Setup (Optional)
If you prefer manual control:

```bash
# Create virtual environment manually
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python security_pipeline.py
```

### Individual Components

#### Vulnerability Scanning Only
```bash
python vulnerability_scanner.py
```

#### Report Generation Only
```bash
python security_report_generator.py <vulnerability_data.json>
```

#### Environment Testing
```bash
python setup_and_test.py
```

## 📊 Output Reports

### When Vulnerabilities Are Found

#### Executive Summary (`executive_summary.xlsx`)
- **Risk-ranked repositories**: Sorted by calculated risk score
- **Severity breakdown**: Critical, High, Medium, Low counts per repository
- **Visual formatting**: Color-coded risk levels
- **Summary statistics**: Total vulnerabilities and affected repositories

#### Detailed Technical Report (`detailed_vulnerabilities.xlsx`)
- **Complete vulnerability details**: CVE IDs, CVSS scores, descriptions
- **Remediation information**: Patched versions and fix guidance
- **Component analysis**: Affected packages and dependencies
- **Professional formatting**: Color-coded severity levels, text wrapping

#### Additional Files
- **CSV versions**: For data analysis and importing into other tools
- **Source data archive**: Complete raw data for audit trails
- **Comprehensive README**: Detailed statistics and recommendations

### When No Vulnerabilities Are Found

If your repositories have no Dependabot alerts, the scanner creates a **Clean Bill of Health Report**:

```
📁 reports/security_report_YYYYMMDD_HHMMSS/
   └── scan_summary.txt
```

The summary includes:
- ✅ Scan completion status
- 📊 Number of repositories scanned
- 🎉 Confirmation of zero vulnerabilities
- 💡 Security best practices and recommendations

**Example output:**
```
======================================================================
SECURITY SCAN SUMMARY
======================================================================

Scan Date: 2025-11-02 09:33:03
Account: your-username
Repositories Scanned: 42
Vulnerabilities Found: 0

✅ STATUS: ALL CLEAR

No Dependabot security alerts were found in any of your repositories.
Your codebase appears to be secure from known dependency vulnerabilities.

Recommendations:
- Continue monitoring for new security advisories
- Keep dependencies up to date
- Enable Dependabot security updates if not already enabled
```

## 🎨 Key Improvements in v2.1

### New Features
- **👤 Personal Account Support**: Now works with individual GitHub accounts, not just organizations
- **🔄 Flexible Configuration**: Auto-detects personal accounts vs organizations
- **✅ Zero Vulnerability Handling**: Treats clean scans as success with positive reporting
- **📝 Clean Bill of Health**: Generates summary reports even when no vulnerabilities are found
- **🔍 Smart Repository Detection**: Automatically tries organization then falls back to user account

### Code Quality
- **Modular Architecture**: Separated concerns into focused classes
- **Type Hints**: Complete type annotations for better IDE support
- **Error Handling**: Comprehensive exception handling and recovery
- **Documentation**: Detailed docstrings and inline comments
- **PEP 8 Compliance**: Clean, readable, maintainable code

### Performance Optimizations
- **Efficient API Usage**: Pagination and rate limiting
- **Memory Management**: Streaming data processing for large datasets
- **Reduced Dependencies**: Streamlined requirements
- **Caching**: Intelligent data caching where appropriate

### User Experience
- **Professional Output**: Enterprise-grade reports
- **Clear Progress**: Real-time scan progress indicators
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Setup Automation**: Guided setup and validation
- **Flexible Configuration**: Works with personal accounts and organizations seamlessly

### Security Enhancements
- **Formula Escaping**: Prevents Excel formula injection
- **Input Validation**: Comprehensive input sanitization
- **Token Security**: Secure token handling and validation
- **Audit Trail**: Complete scan history and traceability

## 🔧 Configuration Options

### Environment Variables

#### For Personal Accounts
```env
GITHUB_TOKEN=ghp_your_token           # Required: GitHub personal access token
GITHUB_URL=https://github.com/username # Required: Your GitHub profile URL
# GITHUB_ORG=                          # Optional: Leave commented for personal use
```

#### For Organizations
```env
GITHUB_TOKEN=ghp_your_token           # Required: GitHub personal access token
GITHUB_ORG=your-organization          # Required: Organization name
# GITHUB_URL=                          # Optional: Not needed for organizations
```

#### For GitHub Enterprise
```env
GITHUB_TOKEN=your_enterprise_token    # Required: GitHub Enterprise token
GITHUB_ORG=your-organization          # Required: Organization name
GITHUB_ENTERPRISE_URL=https://github.company.com  # Required: Enterprise URL
```

### Token Scopes Required

Your GitHub token needs the following scopes:
- ✅ **`repo`** - Full control of private repositories (to access repo data)
- ✅ **`security_events`** - Read Dependabot alerts (to scan vulnerabilities)

### Configuration Priority

The scanner uses this priority for account detection:
1. If `GITHUB_ORG` is set → Uses organization mode
2. If `GITHUB_URL` is set → Extracts username and uses personal account mode
3. Falls back to trying both organization then user account

## 📝 Real-World Examples

### Example 1: Scanning Your Personal Account

```bash
# 1. Create .env file
cat > .env << EOF
GITHUB_TOKEN=ghp_abc123xyz789...
GITHUB_URL=https://github.com/johndoe
EOF

# 2. Run the scanner
python security_pipeline.py

# Output:
# ℹ️  Using GitHub account: johndoe (from GITHUB_URL)
# 🔍 Starting vulnerability scan for johndoe
# Fetching repositories from johndoe...
#   Not an organization, trying as user account...
#   Found 25 repositories (user account)
# [1/25] Processing my-awesome-project...
# ...
```

### Example 2: Scanning an Organization

```bash
# 1. Create .env file
cat > .env << EOF
GITHUB_TOKEN=ghp_abc123xyz789...
GITHUB_ORG=my-company
EOF

# 2. Run the scanner
python security_pipeline.py

# Output:
# ℹ️  Using GitHub organization: my-company
# 🔍 Starting vulnerability scan for my-company
# Fetching repositories from my-company...
# Total repositories found: 150 (organization)
# ...
```

### Example 3: Clean Scan (No Vulnerabilities)

```bash
# When all repositories are secure:
✅ Vulnerability scan completed: 0 vulnerabilities found
✅ No vulnerabilities found - all repositories are secure!

📊 STEP 2: SECURITY REPORT GENERATION
✅ No vulnerabilities to report - creating clean bill of health report
📁 Reports location: reports/security_report_20251102_093228/

🎉 PIPELINE COMPLETED SUCCESSFULLY
📊 **SECURITY POSTURE SUMMARY**
   Total Open Vulnerabilities: 0
```

### Example 4: Scan with Vulnerabilities Found

```bash
# When vulnerabilities are detected:
✅ Vulnerability scan completed: 15 vulnerabilities found

📊 STEP 2: ENHANCED SECURITY REPORT GENERATION
✅ Comprehensive security reports generated successfully!
📁 Reports location: reports/security_report_20251102_143052

📋 Generated Report Suite:
  • executive_summary.xlsx - 📈 Multi-sheet executive workbook
  • detailed_vulnerabilities.xlsx - 🔍 Complete vulnerability inventory
  • ...
```

### Risk Scoring Weights
Customize risk scoring in `config_utils.py`:
```python
SEVERITY_WEIGHTS = {
    'CRITICAL': 50,
    'HIGH': 20,
    'MEDIUM': 5,
    'LOW': 1
}
```

### CVSS Default Scores
Configure fallback CVSS scores:
```python
CVSS_DEFAULTS = {
    'critical': 9.0,
    'high': 7.0,
    'medium': 5.0,
    'low': 3.0
}
```

## 📈 Monitoring & Maintenance

### Log Files
- Application logs: `logs/security_pipeline_YYYYMMDD.log`
- Scan statistics and error tracking
- Performance metrics and timing

### Automated Cleanup
- Temporary files automatically removed after each run
- Old log files can be cleaned up using utilities
- Report archiving for historical analysis

### Performance Metrics
- Repositories scanned per minute
- API rate limit usage
- Report generation timing
- Error rates and recovery

## 🛡️ Security Considerations

### Token Management
- Store tokens securely in `.env` file
- Use tokens with minimal required permissions
- Rotate tokens regularly
- Never commit tokens to version control

### Required Permissions
Your GitHub Enterprise token needs:
- `repo` scope for repository access
- `security_events` scope for Dependabot alerts
- `read:org` scope for organization access

### Data Security
- All data processing is local
- No data transmitted to external services
- Temporary files cleaned up automatically
- Audit trail maintained for compliance

## 🔄 Scheduled Operations

### Recommended Schedule
- **Daily**: Quick scans for critical/high severity updates
- **Weekly**: Complete organizational assessment
- **Monthly**: Comprehensive reporting and trend analysis

### Automation Options
```bash
# Windows Task Scheduler
# Linux/Mac cron job
0 2 * * 1 /path/to/python /path/to/security_pipeline.py
```

## 🆘 Troubleshooting

### Common Issues

#### Token Authentication Failed
```
Error: 401 Unauthorized
Solution: Verify GITHUB_TOKEN in .env file and ensure it hasn't expired
```

#### Missing Permissions
```
Error: 403 Forbidden
Solution: Ensure token has 'repo' and 'security_events' scopes
Go to: https://github.com/settings/tokens
```

#### Account Not Found
```
Error: 404 {"message": "Not Found"}
Solution: For personal accounts, verify GITHUB_URL is set correctly:
  GITHUB_URL=https://github.com/your-actual-username
```

#### No Repositories Found
```
Error: ❌ No repositories found or access denied
Solution: 
1. Verify your token has access to the repositories
2. Check if GITHUB_URL matches your actual username
3. Ensure repos are not all archived or deleted
```

#### Can't Access Private Repositories
```
Error: Cannot access private repositories
Solution: 
1. Token needs 'repo' scope (not just 'public_repo')
2. Regenerate token with proper permissions
3. Update GITHUB_TOKEN in .env file
```

#### Module Not Found
```
Error: ModuleNotFoundError: No module named 'requests'
Solution: 
1. Activate virtual environment: source venv/bin/activate
2. Install dependencies: pip install -r requirements.txt
3. Or let the pipeline auto-install: python3 security_pipeline.py
```

### Testing Your Configuration

Run the diagnostic test script:
```bash
python test_github_access.py
```

This will verify:
- ✅ Token authentication
- ✅ Account access
- ✅ Repository listing
- ✅ Dependabot alerts access

### Getting Help

If you encounter issues:
1. Check the logs in `logs/` directory
2. Verify your `.env` configuration
3. Run the test script to diagnose connectivity
4. Ensure your token has the required scopes

#### Network Connectivity
```
Error: Connection timeout
Solution: Check VPN/network access to GitHub Enterprise
```

#### Python Dependencies
```
Error: Module not found
Solution: pip install -r requirements.txt
```

### Debug Mode
Enable detailed logging:
```python
# In config_utils.py
setup_logging(level="DEBUG")
```

## 📊 Report Types & Features

### 📈 Executive Summary
**Target Audience**: Management, Security Leadership
- High-level vulnerability statistics
- Risk distribution charts
- Compliance status overview
- Trend analysis and KPIs
- Actionable recommendations

### 📋 Detailed Technical Report
**Target Audience**: Security Engineers, Developers
- Complete vulnerability inventory
- CVSS scores and risk assessments
- Resolution tracking with dates
- Repository-specific breakdowns
- Remediation guidance

### 🎯 Enhanced Analytics (New!)
- **Vulnerability Aging Analysis**: Track how long vulnerabilities remain open
- **Resolution Velocity Metrics**: Average time to fix by severity
- **Repository Risk Scoring**: Identify high-risk repositories
- **Compliance Dashboards**: Track against security standards
- **Trend Analysis**: Month-over-month vulnerability patterns

### 📊 Interactive Features
- **Conditional Formatting**: Color-coded severity levels
- **Sortable Columns**: Easy data navigation
- **Filter Capabilities**: Focus on specific criteria
- **Charts & Graphs**: Visual risk representation
- **Export Options**: Multiple format support

## 🔧 Configuration Options

### Environment Variables
```env
# Core Configuration
GITHUB_TOKEN=your_token_here
GITHUB_ORG=your-organization
GITHUB_ENTERPRISE_URL=https://github.boschdevcloud.com

# Advanced Options
SCAN_PRIVATE_REPOS=true
INCLUDE_ARCHIVED_REPOS=false
MAX_REPOS_PER_SCAN=100
RATE_LIMIT_DELAY=1
CVSS_FALLBACK_ENABLED=true

# Report Configuration
EXCEL_CHARTS_ENABLED=true
DETAILED_LOGGING=true
ARCHIVE_SOURCE_DATA=true
CLEANUP_TEMP_FILES=true
```

### Custom Severity Mappings
Modify `config_utils.py` to adjust CVSS score calculations:
```python
SEVERITY_WEIGHTS = {
    'CRITICAL': 50,  # Adjust weights as needed
    'HIGH': 20,
    'MEDIUM': 5,
    'LOW': 1
}
```

## 🔍 Understanding the Reports

### Risk Score Calculation
```
Repository Risk Score = Σ(Vulnerability Count × Severity Weight)
```

### Vulnerability Lifecycle Tracking
- **Days Open**: Time since vulnerability was first detected
- **Resolution Method**: Fixed, Dismissed, or Still Open
- **Resolution Date**: When vulnerability was addressed
- **Average Resolution Time**: Organizational performance metric

### Compliance Metrics
- **OWASP Top 10 Coverage**: Mapping to common vulnerability types
- **Industry Standards**: Alignment with security frameworks
- **Remediation SLA**: Track against organizational goals

## 🎨 Customization Guide

### Adding Custom Report Sections
```python
# In security_report_generator.py
def generate_custom_analysis(self):
    """Add your custom analysis here"""
    # Custom logic for specialized reports
    pass
```

### Modifying Excel Formatting
```python
# Customize colors and styles in SecurityReportGenerator
SEVERITY_COLORS = {
    'CRITICAL': {'bg': 'FF0000', 'font': 'FFFFFF'},
    # Add your custom color schemes
}
```

## 🚨 Security Considerations

### Token Security
- Store tokens in `.env` file (never commit)
- Use read-only tokens when possible
- Rotate tokens regularly
- Monitor token usage and access logs

### Data Privacy
- Reports may contain sensitive security information
- Implement appropriate access controls
- Consider data retention policies
- Ensure compliance with organizational security policies

### Network Security
- Use VPN when accessing GitHub Enterprise
- Validate SSL certificates
- Monitor API usage for anomalies
- Implement rate limiting and retry logic

## 🔄 Automation & CI/CD

### Scheduled Scanning
```bash
# Linux/macOS cron example (daily at 2 AM)
0 2 * * * cd /path/to/security-vuln-scanner && python security_pipeline.py

# Windows Task Scheduler
schtasks /create /tn "Security Scan" /tr "python security_pipeline.py" /sc daily /st 02:00
```

### Integration with CI/CD
```yaml
# GitHub Actions example
name: Security Vulnerability Scan
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run security scan
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python security_pipeline.py
```

## 🛡️ Enterprise Features

### Compliance Reporting
- **SOC 2 Type II**: Automated compliance evidence collection
- **ISO 27001**: Security control validation
- **PCI DSS**: Payment card industry requirements
- **Custom Frameworks**: Configurable compliance mappings

### Advanced Analytics
- **Predictive Analysis**: Vulnerability trend forecasting
- **Risk Correlation**: Cross-repository risk analysis
- **Remediation Recommendations**: AI-powered fix suggestions
- **Cost Analysis**: Resource allocation optimization

### Integration Capabilities
- **SIEM Integration**: Export to security platforms
- **Ticketing Systems**: Automatic issue creation
- **Slack/Teams**: Real-time alerting
- **Email Reports**: Automated distribution

## 🆘 Getting Help

### Troubleshooting Steps
1. **Check logs**: Review `logs/` directory for detailed error information
2. **Run diagnostics**: Execute `python setup_and_test.py`
3. **Verify environment**: Ensure all dependencies are installed
4. **Test connectivity**: Validate GitHub Enterprise access
5. **Review permissions**: Confirm token has required scopes

### Support Resources
- **Internal Documentation**: Check organizational security wiki
- **GitHub Enterprise Support**: For API-related issues
- **Python Community**: For general programming questions
- **Security Team**: For vulnerability classification questions

### Performance Optimization
- **Large Organizations**: Consider pagination and rate limiting
- **Network Issues**: Implement retry mechanisms
- **Memory Usage**: Monitor for large data sets
- **Parallel Processing**: Scale scanning for multiple organizations

## 📝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python setup_and_test.py

# Code formatting
black *.py

# Type checking
mypy *.py --ignore-missing-imports
```

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation for changes
- Maintain backwards compatibility

### Feature Requests
1. Create detailed feature specifications
2. Consider security implications
3. Ensure enterprise scalability
4. Add comprehensive testing
5. Update documentation

## 📄 License & Compliance

This project provides a generic security vulnerability scanning pipeline for any GitHub organization. Open source under MIT license.

### Data Handling
- **Confidentiality**: All vulnerability data is confidential
- **Data Retention**: Follow organizational data policies
- **Access Control**: Implement role-based access
- **Audit Trail**: Maintain comprehensive logs

## 🏷️ Version History

### v2.1.0 (Current) - November 2025
- ✅ **Personal Account Support**: Now works with individual GitHub accounts
- ✅ **Flexible Configuration**: Auto-detects personal accounts vs organizations
- ✅ **Smart Repository Detection**: Falls back from org to user account automatically
- ✅ **Zero Vulnerability Handling**: Creates "Clean Bill of Health" reports
- ✅ **Enhanced Error Messages**: Better guidance for configuration issues
- ✅ **Improved Documentation**: Comprehensive examples and troubleshooting

### v2.0.0 - November 2025
- ✅ Complete code optimization and cleanup (75% file reduction to 7 core files)
- ✅ Modular architecture with separated concerns
- ✅ Enhanced vulnerability lifecycle tracking with resolution dates
- ✅ Professional Excel formatting with conditional coloring
- ✅ Intelligent CVSS scoring with fallback mechanisms
- ✅ Comprehensive documentation and setup guides
- ✅ Advanced analytics and trend analysis
- ✅ Enterprise-grade error handling and logging

### v1.x (Legacy)
- ✅ Initial implementation
- ✅ Basic vulnerability scanning
- ✅ Simple reporting capabilities

---

## ❓ Frequently Asked Questions (FAQ)

### Q: Can I use this with my personal GitHub account?
**A:** Yes! As of v2.1, the scanner fully supports personal accounts. Just set `GITHUB_URL=https://github.com/your-username` in your `.env` file.

### Q: Do I need a paid GitHub account?
**A:** No, you can use it with a free GitHub account. However, you need to enable Dependabot alerts in your repository settings.

### Q: What if I have no vulnerabilities?
**A:** Great! The scanner will create a "Clean Bill of Health" report confirming all repositories are secure.

### Q: Can I scan both public and private repositories?
**A:** Yes, if your token has the `repo` scope, it will scan all accessible repositories (both public and private).

### Q: How often should I run scans?
**A:** We recommend:
- **Personal accounts**: Weekly or bi-weekly
- **Small teams**: Daily or every other day
- **Organizations**: Daily with automated scheduling

### Q: Does this work with GitHub Enterprise Server?
**A:** Yes! Set `GITHUB_ENTERPRISE_URL` to your enterprise server URL in the `.env` file.

### Q: Will this modify my repositories?
**A:** No, the scanner is read-only. It only reads Dependabot alerts and generates reports.

### Q: What's the difference between GITHUB_URL and GITHUB_ORG?
**A:** 
- `GITHUB_URL`: Use for personal accounts (e.g., `https://github.com/username`)
- `GITHUB_ORG`: Use for organizations (e.g., `my-company-name`)

### Q: Can I schedule automatic scans?
**A:** Yes! Use cron (Linux/Mac) or Task Scheduler (Windows):
```bash
# Daily at 2 AM
0 2 * * * cd /path/to/scanner && python3 security_pipeline.py
```

### Q: How do I know if my token has the right permissions?
**A:** Run the test script: `python test_github_access.py` to verify your token and permissions.

---

## 🎯 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Clone/download repository
- [ ] Create `.env` file (use template above for personal account or organization)
- [ ] Get GitHub token with `repo` and `security_events` scopes
- [ ] Run setup: `python setup_env.py` (optional, interactive)
- [ ] Execute scan: `python security_pipeline.py`
- [ ] Review reports in `reports/` directory
- [ ] Set up automated scheduling (optional)

**🚀 Ready to secure your code? Start scanning now!**

---

**Contact**: For support and questions, please open a GitHub issue or contact the development team.

**Last Updated**: November 2025