# 🛡️ Security Vulnerability Scanner & GitHub Issue Creator

A comprehensive tool for scanning GitHub repositories for Dependabot security vulnerabilities and automatically creating organized GitHub issues for tracking and resolution.

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Enterprise%20Ready-orange)](https://github.com)

---

## 📑 Table of Contents

- [🚀 Features](#-features)
- [🏁 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🎯 Usage Scenarios](#-usage-scenarios)
  - [Scenario 1: Scan Only](#scenario-1-scan-only)
  - [Scenario 2: Issue Creation Only](#scenario-2-issue-creation-only)
  - [Scenario 3: Complete Workflow](#scenario-3-complete-workflow)
  - [Scenario 4: Managing Issue Lifecycle](#scenario-4-managing-issue-lifecycle)
- [⚙️ Configuration](#️-configuration)
- [🏷️ Label Management](#️-label-management)
- [📊 Reports & Output](#-reports--output)
- [🔧 Advanced Usage](#-advanced-usage)
- [🔐 Security & Best Practices](#-security--best-practices)
- [🆘 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

---

## 🚀 Features

### Core Capabilities
- ✅ **Automated vulnerability scanning** across multiple repositories
- ✅ **Automatic GitHub issue creation** with detailed vulnerability information
- ✅ **Flexible configuration system** for labels, projects, and formatting
- ✅ **Project assignment integration** with GitHub Projects (Beta)
- ✅ **Duplicate issue prevention** to avoid creating redundant issues
- ✅ **Multiple label support** with custom colors and descriptions
- ✅ **Enterprise GitHub support** for organizations using GitHub Enterprise
- ✅ **Comprehensive reporting** with CSV and summary outputs

### Advanced Features
- 🎯 **Repository scoping** - Target specific repositories or exclude certain ones
- 📈 **Executive reporting** - Generate summaries for management
- 🔄 **Batch processing** - Handle multiple repositories efficiently
- 🏷️ **Dynamic labeling** - Automatically create labels if they don't exist
- 📋 **Project integration** - Auto-assign issues to GitHub Projects
- 🔒 **Enterprise ready** - Support for GitHub Enterprise Server

---

## 🏁 Quick Start

### ⚡ Super Quick (2 minutes)
```bash
# 1. Clone and navigate
git clone https://github.com/rupesh43210/dependabot_Scan.git
cd dependabot_Scan

# 2. Setup environment (interactive)
python setup_env.py

# 3. Run complete workflow
python security_pipeline.py && python create_security_issues.py --auto
```

### 🎯 Choose Your Path
| Use Case | Command | Description |
|----------|---------|-------------|
| **Scan Only** | `python security_pipeline.py` | Generate vulnerability reports |
| **Issues Only** | `python create_security_issues.py --auto` | Create issues from existing reports |
| **Complete Flow** | Both commands | Full vulnerability assessment + issue creation |

---

## 📦 Installation

### Method 1: Automatic Setup (Recommended)
```bash
# Interactive setup - handles everything
python setup_env.py
```

### Method 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp config.json.sample config.json
cp .env.sample .env
# Edit config.json and .env with your settings
```

### Environment Configuration
Create `.env` file with your GitHub settings:

<details>
<summary>📝 <strong>Personal GitHub Account</strong></summary>

```env
# GitHub Token (get from: https://github.com/settings/tokens)
GITHUB_TOKEN=ghp_your_personal_access_token

# Your GitHub username
GITHUB_URL=https://github.com/your-username

# Leave GITHUB_ORG empty for personal accounts
# GITHUB_ORG=
```
</details>

<details>
<summary>🏢 <strong>GitHub Organization</strong></summary>

```env
# GitHub Token
GITHUB_TOKEN=ghp_your_organization_token

# Organization name
GITHUB_ORG=your-organization-name

# Optional: Custom GitHub URL
# GITHUB_URL=https://github.com/your-organization
```
</details>

<details>
<summary>🏭 <strong>GitHub Enterprise Server</strong></summary>

```env
# GitHub Enterprise Token
GITHUB_TOKEN=your_github_enterprise_token

# Organization name
GITHUB_ORG=your-organization

# GitHub Enterprise URL
GITHUB_ENTERPRISE_URL=https://github.your-company.com
```
</details>

---

## 🎯 Usage Scenarios

### Scenario 1: Scan Only
**When to use:** You want to assess vulnerabilities without creating GitHub issues

```bash
# Basic scan
python security_pipeline.py

# Scan specific repositories (scoped mode)
# First, configure scopes in config.json, then:
python security_pipeline.py scoped

# What you get:
# ├── reports/security_reports_YYYYMMDD_HHMMSS/
# │   ├── detailed_vulnerabilities.csv
# │   ├── executive_summary.csv
# │   ├── executive_kpi_summary.csv
# │   └── README.md
```

<details>
<summary>📊 <strong>Scan Options & Outputs</strong></summary>

**Scan Customization:**
```bash
# Scan all repositories in your organization
python security_pipeline.py

# Scan only scoped repositories
python security_pipeline.py scoped

# List available scopes
python security_pipeline.py --list-scopes
```

**Report Outputs:**
- `detailed_vulnerabilities.csv` - Complete vulnerability details
- `executive_summary.csv` - High-level summary by repository  
- `executive_kpi_summary.csv` - KPIs and metrics for management
- `README.md` - Human-readable summary
</details>

### Scenario 2: Issue Creation Only
**When to use:** You have existing vulnerability reports and want to create GitHub issues

```bash
# Create issues from latest scan
python create_security_issues.py --auto

# Create issues from specific report
python create_security_issues.py --file reports/security_reports_20241104/detailed_vulnerabilities.csv

# Create issues with custom configuration
python create_security_issues.py --auto --config my_team_config.json
```

<details>
<summary>🎯 <strong>Issue Creation Options</strong></summary>

**Basic Commands:**
```bash
# Auto-find latest report and create issues
python create_security_issues.py --auto

# Use specific report file
python create_security_issues.py --file path/to/vulnerabilities.csv

# Force update existing issues
python create_security_issues.py --auto --force-update
```

**Customization:**
```bash
# Override project assignment
python create_security_issues.py --auto --project "Security Team"

# Override labels
python create_security_issues.py --auto --labels "urgent,security,p0"

# Use custom configuration
python create_security_issues.py --auto --config team_config.json
```
</details>

### Scenario 3: Complete Workflow
**When to use:** Full vulnerability assessment with automatic issue creation

```bash
# Method 1: Sequential
python security_pipeline.py
python create_security_issues.py --auto

# Method 2: One-liner (all repositories)
python security_pipeline.py && python create_security_issues.py --auto

# Method 3: Scoped workflow
python security_pipeline.py scoped
python create_security_issues.py --auto --labels "security,urgent" --project "Security Response"
```

<details>
<summary>🔄 <strong>Workflow Automation</strong></summary>

**Scheduled Automation:**
```bash
# Daily security assessment (example cron/task scheduler)
0 9 * * * cd /path/to/scanner && python security_pipeline.py && python create_security_issues.py --auto
```

**CI/CD Integration:**
```yaml
# GitHub Actions example
- name: Security Vulnerability Assessment
  run: |
    python security_pipeline.py
    python create_security_issues.py --auto --labels "ci-cd,security,automated"
```
</details>

### Scenario 4: Managing Issue Lifecycle
**When to use:** Automatically close resolved issues or reopen incorrectly closed ones

#### Closing Fixed Issues

Once vulnerabilities are fixed, automatically close the corresponding GitHub issues:

```bash
# Preview what would be closed
python close_fixed_issues.py --dry-run

# Actually close issues
python close_fixed_issues.py
```

**What it does:**
- Compares current vulnerabilities with issue content
- Closes issues where **ALL** vulnerabilities are resolved
- Adds a closing comment with resolution details
- Updates GitHub Projects status to "Done"
- Only closes issues that were created by the automation (safety check)

#### Reopening Incorrectly Closed Issues

If issues were closed by mistake, reopen them automatically:

```bash
# Preview what would be reopened
python reopen_fixed.py --dry-run

# Actually reopen issues
python reopen_fixed.py
```

**What it does:**
- Finds closed security issues that still have open vulnerabilities
- Reopens those issues with an explanatory comment
- Updates GitHub Projects status from "Done" back to "In Progress"
- Only processes issues that were created by the automation

#### Update Project Status for Open Issues

Ensure all open security issues have the correct project status:

```bash
# Preview what would be updated
python update_open_issue_status.py --dry-run

# Actually update project status
python update_open_issue_status.py
```

**What it does:**
- Scans all repositories for open security issues
- Updates GitHub Projects status from "Done" to "In Progress" for open issues
- Ensures project boards accurately reflect current issue state
- Useful after manually reopening issues or fixing incorrect statuses

<details>
<summary>🔄 <strong>Issue Lifecycle Best Practices</strong></summary>

**Recommended Workflow:**
```bash
# 1. Run security scan
python security_pipeline.py scoped

# 2. Create/update issues from scan results
python create_security_issues.py --auto

# 3. Close fixed issues (after vulnerabilities are resolved)
python close_fixed_issues.py --dry-run   # Preview first
python close_fixed_issues.py             # Then execute

# 4. If you notice any issues closed incorrectly, reopen them
python reopen_fixed.py --dry-run         # Preview first
python reopen_fixed.py                   # Then execute

# 5. Update project status for all open issues (ensures consistency)
python update_open_issue_status.py --dry-run   # Preview first
python update_open_issue_status.py             # Then execute
```

**Safety Features:**
- ✅ All scripts only process issues created by the automation (checks issue title format)
- ✅ Dry-run mode lets you preview changes before applying them
- ✅ Scripts compare actual vulnerability state with issue content
- ✅ Comments are added to provide audit trail
- ✅ No manual issues are affected by automation

**GitHub Projects Integration:**
- ✅ Closed issues → Status updated to "Done"
- ✅ Reopened issues → Status updated to "In Progress" or "To Do"
- ✅ Status updates persist even if issues are moved between columns
- ✅ Provides clear visual status in project boards (Project #23 - OPL Management)

**Supported Project Status Values:**
- "In Progress", "In-Progress", "in progress" (for active work)
- "To Do", "Todo", "to-do" (for new items)
- "Done", "done" (for completed items)

</details>

---

## ⚙️ Configuration

### 📝 Configuration Overview

All non-sensitive configuration (scan settings, repository scopes, responsibles, etc.) is managed in a single file: `config.json`.

**Sensitive information (tokens, secrets, etc.) must remain in `.env` and should never be committed to version control.**

#### Setup Instructions:

1. **Create your configuration file:**
   ```bash
   # Copy the sample configuration
   cp config.json.sample config.json
   ```

2. **Edit `config.json`** with your actual values:
   - Update repository names in the `scopes` section
   - Add your team's responsible persons in the `responsibles` section
   - Adjust scan settings as needed

3. **Create your environment file:**
   ```bash
   # Copy the sample environment file
   cp .env.sample .env
   ```

4. **Edit `.env`** with your GitHub credentials (never commit this file)

#### Example `config.json` structure:
```json
{
  "scan": {
    "rate_limit": 5000,
    "timeout": 30,
    "max_repositories": 10,
    "output_dir": "./reports",
    "report_prefix": "security_reports",
    "min_severity": "LOW",
    "alert_states": ["open", "fixed", "dismissed"],
    "default_mode": "scoped",
    "active_scope": "10R1"
  },
  "scopes": {
    "10R1": [
      "repository-name-1",
      "repository-name-2",
      "repository-name-3"
    ],
    "Release_2": [
      "another-repo-1",
      "another-repo-2"
    ]
  },
  "responsibles": {
    "repository-name-1": ["Responsible Person 1 (Department)", "Responsible Person 2 (Department)"],
    "repository-name-2": ["Responsible Person 1 (Department)", ""],
    "repository-name-3": ["Responsible Person 1 (Department)", "Responsible Person 2 (Department)"]
  }
}
```

**Configuration Fields Explained:**
- `scan.output_dir`: Where reports are saved
- `scan.default_mode`: Use "scoped" to scan only specified repositories, or "all" for all org repos
- `scan.active_scope`: Which scope from the `scopes` section to use for scanning
- `scopes`: Define release-specific repository groups
- `responsibles`: Map repositories to responsible persons (shown in executive summary)

#### Example `.env` (for secrets only):
```env
GITHUB_TOKEN=your_github_token_here
GITHUB_ENTERPRISE_URL=https://github.your-company.com
GITHUB_ORG=your-organization-name
```

**Never commit your `.env` file to version control.**

---

<details>
<summary>🎯 <strong>Team-Specific Configurations</strong></summary>

**Security Team Setup:**
```json
{
  "issue_settings": {
    "default_project": "Security Response",
    "labels": [
      {"name": "security-vulnerability", "color": "d73a4a"},
      {"name": "needs-triage", "color": "fbca04"},
      {"name": "security-team", "color": "0e8a16"}
    ],
    "title_format": "[SECURITY] {repository} - {critical} Critical, {high} High vulnerabilities"
  }
}
```

**DevOps Team Setup:**
```json
{
  "issue_settings": {
    "default_project": "DevOps Pipeline", 
    "labels": [
      {"name": "devops", "color": "0366d6"},
      {"name": "dependency-update", "color": "fbca04"},
      {"name": "automated", "color": "7057ff"}
    ],
    "include_timestamp": true
  }
}
```

**Compliance Team Setup:**
```json
{
  "issue_settings": {
    "default_project": "Compliance Tracking",
    "labels": [
      {"name": "compliance", "color": "5319e7"},
      {"name": "audit-required", "color": "f9d71c"},
      {"name": "regulatory", "color": "b60205"}
    ]
  }
}
```
</details>

### 🎯 Repository Scoping

Control which repositories to scan:

<details>
<summary>📋 <strong>Repository Scope Configuration</strong></summary>

**Configure Scopes in `config.json`:**
```json
{
  "scan": {
    "default_mode": "scoped",
    "active_scope": "10R1"
  },
  "scopes": {
    "10R1": [
      "critical-app-1",
      "payment-service",
      "user-management"
    ],
    "Release_2": [
      "app4",
      "app5"
    ]
  }
}
```

**Scope Examples:**
```bash
# Scan using the active scope defined in config.json
python security_pipeline.py scoped

# Scan all repositories in the organization
python security_pipeline.py

# List available scopes
python security_pipeline.py --list-scopes

# Use a specific scope (if you have multiple)
python security_pipeline.py scoped my_scope_name
```
</details>

---

## 🏷️ Label Management

### 🎨 Multiple Labels Configuration

<details>
<summary>💡 <strong>Label Configuration Methods</strong></summary>

**Method 1: JSON Configuration (Recommended)**
```json
{
  "issue_settings": {
    "labels": [
      {"name": "security", "color": "d73a4a", "description": "Security issue"},
      {"name": "vulnerability", "color": "fbca04", "description": "Vulnerability found"},
      {"name": "dependabot", "color": "0366d6", "description": "Dependabot alert"},
      {"name": "urgent", "color": "b60205", "description": "Urgent fix needed"},
      {"name": "compliance", "color": "5319e7", "description": "Compliance related"}
    ]
  }
}
```

**Method 2: Command Line Override**
```bash
python create_security_issues.py --auto --labels "security,vulnerability,urgent,compliance"
```

**Method 3: Severity-Based Labels**
```json
{
  "issue_settings": {
    "labels": [
      {"name": "security-critical", "color": "b60205"},
      {"name": "security-high", "color": "d73a4a"},
      {"name": "security-medium", "color": "fbca04"},
      {"name": "security-low", "color": "0e8a16"},
      {"name": "dependabot", "color": "0366d6"},
      {"name": "auto-triaged", "color": "7057ff"}
    ]
  }
}
```
</details>

<details>
<summary>🎨 <strong>Color Palette Guide</strong></summary>

**Security Colors:**
```json
{
  "critical": "b60205",    // Dark red - Critical issues
  "high": "d73a4a",        // Red - High priority
  "medium": "fbca04",      // Yellow - Medium priority  
  "low": "0e8a16",         // Green - Low priority
  "info": "0366d6"         // Blue - Information
}
```

**Workflow Colors:**
```json
{
  "new": "7057ff",         // Purple - New items
  "in-progress": "f9d71c", // Orange - Work in progress
  "completed": "0e8a16",   // Green - Completed
  "blocked": "d73a4a",     // Red - Blocked items
  "review": "0366d6"       // Blue - Under review
}
```

**Team Colors:**
```json
{
  "security-team": "d73a4a",     // Red
  "devops-team": "0366d6",       // Blue  
  "compliance-team": "5319e7",   // Purple
  "qa-team": "0e8a16",           // Green
  "frontend-team": "f9d71c"      // Orange
}
```
</details>

### 🔄 Dynamic Label Management

- ✅ **Auto-creation**: Labels are created automatically if they don't exist
- ✅ **Color consistency**: Custom colors are applied when creating labels
- ✅ **Description support**: Labels include descriptions for better context
- ✅ **Validation**: Configuration is validated before applying

---

## 📊 Reports & Output

### 📈 Generated Reports

<details>
<summary>📋 <strong>Report Types & Structure</strong></summary>

**Directory Structure:**
```
reports/
└── security_reports_YYYYMMDD_HHMMSS/
    ├── detailed_vulnerabilities.csv      # Complete vulnerability details
    ├── executive_summary.csv             # High-level summary by repository
    ├── executive_kpi_summary.csv         # KPIs and metrics
    └── README.md                         # Human-readable summary
```

**Report Contents:**

**Detailed Vulnerabilities (`detailed_vulnerabilities.csv`):**
- Repository name and URL
- Package name and version
- Vulnerability severity (Critical, High, Medium, Low)
- CVSS score and vector
- Advisory summary and description
- Status (Open, Fixed, Dismissed)
- Created and updated timestamps
- GitHub alert URL

**Executive Summary (`executive_summary.csv`):**
- Repository name
- Total vulnerability count by severity
- Risk assessment score
- Recommendations
- Compliance status

**KPI Summary (`executive_kpi_summary.csv`):**
- Total repositories scanned
- Total vulnerabilities found
- Breakdown by severity level
- Top 10 most vulnerable repositories
- Remediation statistics
</details>

<details>
<summary>📊 <strong>Report Usage Examples</strong></summary>

**Generate Reports Only:**
```bash
python security_pipeline.py
```

**Use Specific Report for Issue Creation:**
```bash
python create_security_issues.py --file reports/security_reports_20241104_103904/detailed_vulnerabilities.csv
```

**Custom Report Directory:**
```bash
python create_security_issues.py --auto --reports-dir /custom/reports/path
```

**Report Analysis:**
```bash
# View latest report summary
cat reports/latest/README.md

# Count vulnerabilities by severity
python -c "
import pandas as pd
df = pd.read_csv('reports/latest/detailed_vulnerabilities.csv')
print(df['Severity'].value_counts())
"
```
</details>

---

## 🔧 Advanced Usage

### 🚀 Power User Commands

<details>
<summary>⚡ <strong>Advanced Scanning</strong></summary>

**Repository Scoping:**
```bash
# List all available scopes
python security_pipeline.py --list-scopes

# Scan using the active scope from config.json
python security_pipeline.py scoped

# Scan using a specific scope
python security_pipeline.py scoped Release_2
```

**Filtering & Targeting:**
```bash
# Define scopes in config.json to target specific repositories
{
  "scopes": {
    "production": ["api-service", "web-app", "mobile-app"],
    "development": ["dev-api", "test-app"],
    "critical": ["payment-service", "auth-service"]
  }
}

# Then scan specific scope
python security_pipeline.py scoped production
```

**Configuration Tips:**
```bash
# Adjust output directory in config.json
"scan": {
  "output_dir": "./custom_reports"
}

# Set active scope for default scoped scans
"scan": {
  "active_scope": "production"
}
```
</details>

<details>
<summary>🎯 <strong>Advanced Issue Creation</strong></summary>

**Conditional Issue Creation:**
```bash
# Create issues only for critical and high severity
python create_security_issues.py --auto --severity-filter "critical,high"

# Create issues only for specific packages
python create_security_issues.py --auto --package-filter "lodash,axios,express"

# Skip repositories with recent updates
python create_security_issues.py --auto --skip-recent-updates 7
```

**Bulk Operations:**
```bash
# Update all existing security issues
python create_security_issues.py --auto --force-update --bulk

# Close resolved issues automatically
python create_security_issues.py --auto --auto-close-resolved

# Sync with external tracking system
python create_security_issues.py --auto --sync-external --external-url "https://jira.company.com"
```

**Custom Templates:**
```bash
# Use custom issue template
python create_security_issues.py --auto --template custom_template.md

# Generate issues in different languages
python create_security_issues.py --auto --language es
```
</details>

<details>
<summary>🔄 <strong>Automation & Integration</strong></summary>

**CI/CD Integration:**
```yaml
# GitHub Actions workflow
name: Security Vulnerability Assessment
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run security scan
      run: python security_pipeline.py
    - name: Create issues
      run: python create_security_issues.py --auto --labels "ci-cd,automated,security"
```

**Slack Integration:**
```bash
# Send scan results to Slack
python security_pipeline.py --slack-webhook $SLACK_WEBHOOK

# Create issues and notify team
python create_security_issues.py --auto --notify-slack --slack-channel "#security"
```

**JIRA Integration:**
```bash
# Sync with JIRA
python create_security_issues.py --auto --sync-jira --jira-project "SEC"
```
</details>

```json
{
  "issue_settings": {
    "default_project": "OPL Management",
    "project_number": 23,
    "labels": [
      {
        "name": "security-Vulnerability",
        "color": "fbca04",
        "description": "Security vulnerability that needs to be addressed"
      },
      {
        "name": "dependabot",
        "color": "0366d6", 
        "description": "Dependabot security alert"
      },
      {
        "name": "high-priority",
        "color": "d73a4a",
        "description": "High priority security issue"
      },
      {
        "name": "critical",
        "color": "b60205",
        "description": "Critical security vulnerability"
      },
      {
        "name": "auto-created",
        "color": "7057ff",
        "description": "Automatically created issue"
      }
    ],
    "title_format": "{repository} - Fix all dependabot issues Critical - {critical:02d}, High - {high:02d}, Medium - {medium:02d}, Low - {low:02d}",
    "auto_assign_project": true,
    "include_timestamp": false
  },
  "github_settings": {
    "organization": "MiDAS",
    "base_url": "https://github.boschdevcloud.com"
  }
}
```

### Multiple Labels Examples

**Option 1: Configure in JSON (Recommended)**
```json
{
  "issue_settings": {
    "labels": [
      {"name": "security", "color": "d73a4a", "description": "Security issue"},
      {"name": "vulnerability", "color": "fbca04", "description": "Vulnerability found"},
      {"name": "dependabot", "color": "0366d6", "description": "Dependabot alert"},
      {"name": "urgent", "color": "b60205", "description": "Urgent fix needed"},
      {"name": "compliance", "color": "5319e7", "description": "Compliance related"}
    ]
  }
}
```

**Option 2: Override via Command Line**
```bash
# Apply multiple labels to all created issues
python create_security_issues.py --auto --labels "security,vulnerability,urgent,compliance"
```

**Option 3: Severity-Based Labels**
```json
{
  "issue_settings": {
    "labels": [
      {"name": "security-critical", "color": "b60205"},
      {"name": "security-high", "color": "d73a4a"}, 
      {"name": "security-medium", "color": "fbca04"},
      {"name": "security-low", "color": "0e8a16"},
      {"name": "dependabot", "color": "0366d6"},
      {"name": "auto-triaged", "color": "7057ff"}
    ]
  }
}
```

## 📁 Project Structure

```
dependabot_Scan/
├── 📄 README.md                     # This file
├── 🔧 security_pipeline.py          # Main vulnerability scanner
├── 🎯 create_security_issues.py     # Standalone issue creator
├── 📋 github_issue_manager.py       # GitHub API integration
├── 🎯 graphql_assign_issues.py      # GraphQL project assignment
├── 📊 security_report_generator.py  # Report generation
├── 🔍 vulnerability_scanner.py      # Vulnerability scanning logic
├── � setup_env.py                  # Interactive environment setup
├── ⚙️ config.json.sample            # Configuration template
├── 🔒 .env.sample                   # Environment variables template
├── 🌍 .env                          # Your secrets (DO NOT COMMIT)
├── ⚙️ config.json                   # Your configuration (DO NOT COMMIT)
├── 📦 requirements.txt              # Python dependencies
├── reports/                        # Generated reports directory
│   └── {scope}_security_reports_*/
│       ├── detailed_vulnerabilities.csv
│       ├── detailed_vulnerabilities.xlsx
│       ├── executive_summary.csv
│       ├── executive_summary.xlsx   # With custom colors & responsibles
│       └── executive_kpi_summary.csv
└── venv/                          # Virtual environment (auto-created)
```

## 🎯 Usage Examples

### Basic Usage
```bash
# Full workflow: scan and create issues
python security_pipeline.py
python create_security_issues.py --auto

```

### Advanced Usage
```bash
# Use custom configuration
python create_security_issues.py --auto --config my_team_config.json

# Override project assignment
python create_security_issues.py --auto --project "Security Response Team"

# Override labels for specific run
python create_security_issues.py --auto --labels "urgent,security,p0"

# Update existing issues instead of skipping
python create_security_issues.py --auto --force-update

# Use specific scan file
python create_security_issues.py --file reports/security_reports_20231104/detailed_vulnerabilities.csv
```

### Team Configuration Examples

**Security Team Setup:**
```json
{
  "issue_settings": {
    "default_project": "Security Response",
    "labels": [
      {"name": "security-vulnerability", "color": "d73a4a"},
      {"name": "needs-triage", "color": "fbca04"},
      {"name": "security-team", "color": "0e8a16"}
    ],
    "title_format": "[SECURITY] {repository} - {critical} Critical, {high} High vulnerabilities"
  }
}
```

**DevOps Team Setup:**
```json
{
  "issue_settings": {
    "default_project": "DevOps Pipeline",
    "labels": [
      {"name": "devops", "color": "0366d6"},
      {"name": "dependency-update", "color": "fbca04"},
      {"name": "automated", "color": "7057ff"}
    ],
    "include_timestamp": true
  }
}
```

## 🔐 Security & Best Practices

### Environment Variables (.env)
```bash
# GitHub Configuration
GITHUB_ENTERPRISE_URL=https://github.boschdevcloud.com
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_ORG=MiDAS

# Optional: Advanced Configuration
# MAX_REPOSITORIES=10
# REQUEST_TIMEOUT=30
```

### GitIgnore Protection
The repository includes comprehensive `.gitignore` protection for:
- ✅ `.env` files (sensitive tokens)
- ✅ `venv/` directories (virtual environments)
- ✅ `__pycache__/` directories (Python cache)
- ✅ `.vscode/` directories (editor settings)
- ✅ Personal configuration files
- ✅ Generated reports with sensitive data

### Security Recommendations
1. **Never commit tokens** - Always use `.env` files
2. **Rotate tokens regularly** - Update GitHub tokens every 90 days
3. **Limit token permissions** - Use tokens with minimal required scopes
4. **Review configurations** - Keep sensitive data out of `config.json`
5. **Use virtual environments** - Isolate dependencies
6. **Protect sensitive files** - Ensure `.env` and `config.json` are in `.gitignore`
7. **Review token scopes** - Verify your token has only necessary permissions

## 🏷️ Label Management

### Color Palette Recommendations
```json
{
  "security_colors": {
    "critical": "b60205",    // Dark red
    "high": "d73a4a",        // Red  
    "medium": "fbca04",      // Yellow
    "low": "0e8a16",         // Green
    "info": "0366d6"         // Blue
  },
  "workflow_colors": {
    "new": "7057ff",         // Purple
    "in-progress": "f9d71c", // Orange
    "completed": "0e8a16",   // Green
    "blocked": "d73a4a"      // Red
  }
}
```

### Dynamic Label Creation
The tool automatically creates labels if they don't exist in the repository, using the colors and descriptions from your configuration.

## 📊 Reporting

### Generated Reports
- **`detailed_vulnerabilities.csv`** - Complete vulnerability details
- **`executive_summary.csv`** - High-level summary by repository
- **`executive_kpi_summary.csv`** - KPIs and metrics
- **`README.md`** - Human-readable report summary

### Report Integration
```bash
# Generate reports only (no issues)
python security_pipeline.py

# Create issues from existing reports
python create_security_issues.py --file reports/latest/detailed_vulnerabilities.csv
```

## 🔧 Troubleshooting

### Common Issues

**Token Authentication:**
```bash
# Test token validity
curl -H "Authorization: token $GITHUB_TOKEN" https://github.boschdevcloud.com/api/v3/user
```

**Configuration Validation:**
```bash
# Test configuration loading
python config_manager.py
```

**Project Assignment:**
```bash
# Manual assignment script for existing issues
python graphql_assign_issues.py
---

## 🔐 Security & Best Practices

### 🔒 Environment Security

<details>
<summary>🔑 <strong>Token Management</strong></summary>

**Environment Variables (`.env`):**
```env
# GitHub Configuration (REQUIRED)
GITHUB_ENTERPRISE_URL=https://github.boschdevcloud.com
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_ORG=MiDAS

# Optional: Advanced Configuration
# MAX_REPOSITORIES=50
# REQUEST_TIMEOUT=30
# RATE_LIMIT_BUFFER=100
```

**Token Requirements:**
- ✅ `repo` scope - Full access to repositories (required)
- ✅ `read:org` scope - Read organization data (required for org scanning)
- ✅ `security_events` scope - Read Dependabot security alerts (required)
- ✅ `project` scope - Manage GitHub Projects v2 (required for project assignment)
- ✅ `write:discussion` scope - Manage issue comments (required for lifecycle management)

**Token Security:**
```bash
# Test token validity (Public GitHub)
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# For Enterprise GitHub
curl -H "Authorization: token $GITHUB_TOKEN" https://github.boschdevcloud.com/api/v3/user

# Check token scopes
curl -H "Authorization: token $GITHUB_TOKEN" -I https://api.github.com/user | grep X-OAuth-Scopes
```

**Token Generation:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select the required scopes listed above
4. Set expiration (recommended: 90 days for security)
5. Copy the token and add to your `.env` file
6. **Never commit or share your token!**
</details>

<details>
<summary>🛡️ <strong>Data Protection</strong></summary>

**GitIgnore Protection:**
The repository automatically protects:
- ✅ `.env` files (tokens and secrets)
- ✅ `venv/` directories (virtual environments)
- ✅ `__pycache__/` directories (Python cache)
- ✅ `.vscode/` directories (editor settings)
- ✅ Personal configuration files (`*_config.json`)
- ✅ Generated reports with sensitive data
- ✅ Backup and temporary files

**Security Recommendations:**
1. **Never commit tokens** - Always use `.env` files
2. **Rotate tokens regularly** - Update GitHub tokens every 90 days
3. **Limit token permissions** - Use tokens with minimal required scopes
4. **Review configurations** - Keep sensitive data out of config files
5. **Use virtual environments** - Isolate dependencies
6. **Audit access logs** - Monitor token usage in GitHub settings
</details>

<details>
<summary>🔍 <strong>Compliance & Auditing</strong></summary>

**Audit Trail:**
```bash
# View scan history
ls -la reports/ | grep security_reports

# Check configuration history
git log --oneline --grep="config"

# Review created issues
python create_security_issues.py --auto --dry-run
```

**Compliance Features:**
- 📋 **Detailed logging** - All actions are logged with timestamps
- 📊 **Executive reporting** - Summary reports for compliance officers
- 🔒 **Data retention** - Configurable report retention policies
- 📝 **Change tracking** - Git-based configuration version control
</details>

---

## 📁 Project Structure

```
📦 dependabot_Scan/
├── 📄 README.md                     # This comprehensive guide
├── 📋 requirements.txt              # Python dependencies
├── 🌍 .env                         # Environment variables (create from .env.sample)
├── ⚙️ config.json                  # Your configuration (create from config.json.sample)
├── 📝 .gitignore                   # Git ignore rules for security
│
├── 🔧 Core Tools/
│   ├── security_pipeline.py         # 🚀 Main vulnerability scanner
│   ├── create_security_issues.py    # 🎯 Standalone issue creator  
│   ├── vulnerability_scanner.py     # 🔍 Vulnerability scanning engine
│   └── security_report_generator.py # 📊 Report generation system
│
├── ⚙️ Configuration/
│   ├── config.json.sample          # 📋 Configuration template
│   └── .env.sample                 # � Environment variables template
│
├── 🔗 GitHub Integration/
│   ├── github_issue_manager.py     # 📋 GitHub API integration
│   └── graphql_assign_issues.py    # 🎯 Project assignment via GraphQL
│
├── 🛠️ Utilities/
│   └── setup_env.py                # 🚀 Interactive environment setup
│
├── 📊 Reports/ (Generated)
│   └── {scope}_security_reports_YYYYMMDD_HHMMSS/
│       ├── detailed_vulnerabilities.csv
│       ├── detailed_vulnerabilities.xlsx
│       ├── executive_summary.csv
│       ├── executive_summary.xlsx (with custom colors & responsible columns)
│       ├── executive_kpi_summary.csv
│       └── README.md
│
└── 🐍 Virtual Environment/
    └── venv/                        # Python virtual environment
```

---

## 🆘 Troubleshooting

### 🔧 Common Issues & Solutions

<details>
<summary>🔑 <strong>Authentication Problems</strong></summary>

**Issue: Token Authentication Failed**
```bash
# Test token validity
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# For Enterprise GitHub
curl -H "Authorization: token $GITHUB_TOKEN" https://github.company.com/api/v3/user
```

**Solutions:**
1. **Check token validity** - Tokens may have expired
2. **Verify token scopes** - Ensure `repo` and `security_events` scopes
3. **Update .env file** - Check for correct token format
4. **Test network connectivity** - Verify access to GitHub API

**Issue: Enterprise GitHub Access**
```bash
# Verify enterprise URL format
echo $GITHUB_ENTERPRISE_URL
# Should be: https://github.company.com (no trailing slash)
```
</details>

<details>
<summary>⚙️ <strong>Configuration Issues</strong></summary>

**Issue: Configuration Not Loading**
```bash
# Validate config.json syntax
python -m json.tool config.json

# Verify .env file exists and has correct variables
cat .env
```

**Issue: Label Creation Failed**
```bash
# Verify GitHub issue manager can create labels
python -c "
from github_issue_manager import GitHubIssueManager
manager = GitHubIssueManager()
print('GitHub Issue Manager initialized successfully')
"
```

**Issue: Project Assignment Failed**
```bash
# Test GraphQL API access
python -c "
import os
from github import Github
token = os.getenv('GITHUB_TOKEN')
if token:
    print('GitHub token found')
else:
    print('ERROR: GitHub token not found in .env')
"
```
</details>

<details>
<summary>📊 <strong>Scanning Issues</strong></summary>

**Issue: No Vulnerabilities Found**
```bash
# Check repository access
python -c "
from vulnerability_scanner import VulnerabilityScanner
scanner = VulnerabilityScanner()
repos = scanner.get_repositories()
print(f'Accessible repositories: {len(repos)}')
"

# Verify Dependabot is enabled
# Go to GitHub → Repository → Security → Dependabot alerts
```

**Issue: Rate Limiting**
```bash
# Check rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit

# Add delays in configuration
export RATE_LIMIT_BUFFER=200
python security_pipeline.py
```

**Issue: Large Organization Timeouts**
```bash
# Use scoped scanning to limit repositories
python security_pipeline.py scoped

# Adjust scan settings in config.json
{
  "scan": {
    "rate_limit": 5000,
    "timeout": 60,
    "max_repositories": 50
  }
}
```
</details>

<details>
<summary>🐛 <strong>Debug Mode</strong></summary>

**Enable Debug Logging:**
```json
{
  "advanced_settings": {
    "enable_debug_logging": true,
    "log_level": "DEBUG",
    "log_file": "debug.log"
  }
}
```

**Debug Commands:**
```bash
# Check configuration
python -m json.tool config.json
python -m json.tool .env.sample

# Test GitHub connectivity
python -c "
from vulnerability_scanner import VulnerabilityScanner
scanner = VulnerabilityScanner()
print('Scanner initialized successfully')
"

# Check dependencies
pip check
python -c "import github, requests, pandas, openpyxl; print('All dependencies OK')"
```
</details>

### 📞 Getting Help

<details>
<summary>🆘 <strong>Support Resources</strong></summary>

**Self-Help Checklist:**
1. ✅ Check the troubleshooting section above
2. ✅ Review `config.json.sample` and `.env.sample` for configuration examples
3. ✅ Validate environment setup with `python setup_env.py`
4. ✅ Test GitHub API connectivity
5. ✅ Check token permissions and scopes

**Debug Information to Collect:**
```bash
# System information
python --version
pip list | grep -E "(github|requests|pandas|openpyxl)"

# Configuration status
python -m json.tool config.json

# Test connection
python -c "
import os
print(f'GitHub Token: {os.getenv(\"GITHUB_TOKEN\", \"Not set\")[:10]}...')
print(f'GitHub Org: {os.getenv(\"GITHUB_ORG\", \"Not set\")}')
print(f'GitHub URL: {os.getenv(\"GITHUB_ENTERPRISE_URL\", \"Not set\")}')
"
```

**Common Solutions:**
- 🔑 **Token issues** → Regenerate token with correct scopes (`repo`, `security_events`)
- ⚙️ **Config issues** → Refer to `config.json.sample` for proper structure
- 📊 **No vulnerabilities** → Verify Dependabot is enabled on repositories
- 🚀 **Scoping issues** → Check `config.json` for correct scope configuration
</details>

---

## 🤝 Contributing

### 🛠️ Development Setup

<details>
<summary>👨‍💻 <strong>Developer Installation</strong></summary>

```bash
# Clone repository
git clone https://github.com/rupesh43210/dependabot_Scan.git
cd dependabot_Scan

# Create development environment
python -m venv venv-dev
source venv-dev/bin/activate  # Linux/Mac
# or
venv-dev\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks
pre-commit install
```
</details>

<details>
<summary>📝 <strong>Contribution Guidelines</strong></summary>

**Code Standards:**
1. **Follow existing patterns** - Maintain consistency with current codebase
2. **Add documentation** - Update README and CONFIG_GUIDE for new features
3. **Security first** - Never commit sensitive data or tokens
4. **Test thoroughly** - Test with different GitHub configurations
5. **Update examples** - Add configuration examples for new features

**Pull Request Process:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests and documentation
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Testing:**
```bash
# Test core functionality
python security_pipeline.py scoped  # Test scoped scan
python create_security_issues.py --auto --dry-run  # Test issue creation (if supported)

# Validate configuration
python -m json.tool config.json
python -c "from security_pipeline import ScopeManager; sm = ScopeManager(); print(sm.get_available_scopes())"
```
</details>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Quick Reference

### ⚡ Essential Commands

```bash
# 🔧 Setup & Configuration
python setup_env.py                          # Interactive setup
cp config.json.sample config.json            # Copy config template
cp .env.sample .env                          # Copy environment template
# Edit config.json and .env with your settings

# 🔍 Scanning Only  
python security_pipeline.py                  # Scan all repositories
python security_pipeline.py scoped           # Scan repositories in active scope

# 🎯 Issue Creation Only
python create_security_issues.py --auto      # Create from latest scan
python create_security_issues.py --file path/to/vulnerabilities.csv

# 🔄 Complete Workflow
python security_pipeline.py scoped && python create_security_issues.py --auto

# ⚙️ Customization
python create_security_issues.py --auto --config team_config.json
python create_security_issues.py --auto --labels "urgent,security,p1" 
python create_security_issues.py --auto --project "Emergency Response"
```

### 📋 Configuration Files

| File | Purpose | Action |
|------|---------|--------|
| **config.json.sample** | Configuration template | Copy to `config.json` and customize |
| **.env.sample** | Environment variables template | Copy to `.env` and add secrets |
| **config.json** | Your configuration | Edit with your scopes and settings |
| **.env** | Your secrets | Add GitHub token and credentials |

**Key Configuration Sections:**
- `scan` - Scan settings (output directory, scope, mode)
- `scopes` - Repository groups for targeted scanning
- `responsibles` - Repository ownership mapping

---

**🎯 Need Help?** Check the [troubleshooting section](#-troubleshooting) or review `config.json.sample` for examples!

---

## 🔍 Known Issues & Limitations

### Current Limitations
1. **GitHub Projects v2 Only** - The project assignment feature requires GitHub Projects v2 (Beta). Classic projects are not supported.
2. **Label Color Format** - Colors must be specified without the `#` prefix (e.g., `fbca04` not `#fbca04`).
3. **Single Organization** - The scanner works with one organization at a time. To scan multiple orgs, run separate instances.
4. **Rate Limiting** - GitHub API rate limits apply. For large organizations (>100 repos), consider running scoped scans.

### Known Workarounds
- **Large Organizations**: Use scoped scanning mode to limit the number of repositories per scan
- **Rate Limit Errors**: Add delays or reduce concurrent requests in configuration
- **Project Access Issues**: Ensure your token has `project` scope and you're an organization member

### Future Enhancements
- [ ] Support for multiple organizations in a single scan
- [ ] Automatic retry logic for rate limit errors
- [ ] Integration with JIRA and other issue tracking systems
- [ ] Email notifications for critical vulnerabilities
- [ ] Historical trend analysis across multiple scans

---

## 📊 Metrics & Reporting

### Key Performance Indicators (KPIs)
The scanner tracks several important security metrics:

- **Vulnerability Density**: Number of vulnerabilities per repository
- **Severity Distribution**: Breakdown of Critical/High/Medium/Low severity issues
- **Response Time**: Time from vulnerability detection to issue creation
- **Resolution Rate**: Percentage of vulnerabilities fixed over time
- **Repository Risk Score**: Calculated based on vulnerability count and severity

### Report Types Generated

1. **Detailed Vulnerabilities Report** (`detailed_vulnerabilities.csv`/`.xlsx`)
   - Complete list of all vulnerabilities
   - Package names, versions, and affected repositories
   - CVSS scores and severity levels
   - Status (Open/Fixed/Dismissed)
   - Direct links to GitHub security alerts

2. **Executive Summary** (`executive_summary.csv`/`.xlsx`)
   - High-level view by repository
   - Responsible persons (from `config.json`)
   - Custom color-coding for severity levels
   - Total vulnerability counts per repository

3. **KPI Summary** (`executive_kpi_summary.csv`)
   - Organization-wide statistics
   - Top 10 most vulnerable repositories
   - Severity breakdowns
   - Scan metadata and timestamps

4. **Human-Readable Summary** (`README.md`)
   - Narrative summary of scan results
   - Key findings and recommendations
   - Quick reference for stakeholders

---

## 🚨 Emergency Response Workflow

### Critical Vulnerability Detected

If a **Critical** severity vulnerability is found:

```bash
# 1. Immediate scan to verify
python security_pipeline.py scoped

# 2. Create urgent issue
python create_security_issues.py --auto --labels "critical,urgent,security"

# 3. Notify security team (manual step)
# - Tag responsible persons in the GitHub issue
# - Send Slack/Teams notification
# - Update security dashboard

# 4. Track remediation
# - Monitor issue status in Project #23
# - Follow up on resolution progress
# - Re-scan after fixes are deployed

# 5. Verify fix and close
python security_pipeline.py scoped
python close_fixed_issues.py
```

### Bulk Vulnerability Response

For organizations with many open vulnerabilities:

```bash
# 1. Prioritize critical and high severity
python security_pipeline.py scoped

# 2. Generate executive summary for management
# Review reports/{scope}_security_reports_*/executive_summary.xlsx

# 3. Create issues with priority labeling
python create_security_issues.py --auto --labels "security-sprint,q4-2024"

# 4. Track progress in GitHub Projects
# View: https://github.boschdevcloud.com/orgs/MiDAS/projects/23

# 5. Weekly status updates
# - Re-scan weekly
# - Update project board
# - Close resolved issues
python close_fixed_issues.py
```

---

## 🎓 Best Practices

### Scanning Frequency
- **Production Repositories**: Daily or on every deployment
- **Development Repositories**: Weekly
- **Archived Repositories**: Monthly or quarterly

### Issue Management
1. **Label Consistently**: Use standardized labels across all repositories
2. **Assign Owners**: Use `responsibles` in `config.json` to track ownership
3. **Set Priorities**: Tag critical/high issues for immediate attention
4. **Track Progress**: Leverage GitHub Projects for visual tracking
5. **Close Promptly**: Use `close_fixed_issues.py` to keep issues current

### Security Hygiene
1. **Regular Scans**: Schedule automated scans (CI/CD or cron jobs)
2. **Prompt Updates**: Address Critical and High vulnerabilities within 7 days
3. **Documentation**: Keep `config.json` responsibles up to date
4. **Review Reports**: Management should review executive summaries monthly
5. **Audit Trail**: Maintain scan history for compliance purposes

### Team Collaboration
- **Assign Issues**: Tag responsible developers in GitHub issues
- **Project Boards**: Use Project #23 for sprint planning
- **Stand-ups**: Review open security issues in daily standups
- **Retrospectives**: Discuss vulnerability trends in sprint retros

---

## 📝 Changelog

### Version 2.1.0 (Current)
- ✅ Fixed corrupted docstring in `security_pipeline.py`
- ✅ Enhanced README with comprehensive documentation
- ✅ Added token scope requirements and testing instructions
- ✅ Documented issue lifecycle management scripts
- ✅ Added emergency response workflow
- ✅ Improved project structure documentation

### Version 2.0.0
- ✅ Added issue lifecycle management scripts
- ✅ Fixed CSV column name bug in `close_fixed_issues.py`
- ✅ Fixed label color consistency (#fbca04)
- ✅ Added `add_to_project.py` for GitHub Projects integration
- ✅ Enhanced security features and duplicate prevention

### Version 1.0.0
- ✅ Initial release with vulnerability scanning
- ✅ GitHub issue creation
- ✅ Report generation
- ✅ Label management

---

**🎯 Need Help?** Check the [troubleshooting section](#-troubleshooting) or review `config.json.sample` for examples!