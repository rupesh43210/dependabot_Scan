# Code Scanning Security Reports

## Overview

This module provides automated security reporting for **GitHub Code Scanning alerts** (SAST findings from CodeQL and other security analysis tools). It scans repositories for code-level security vulnerabilities and generates comprehensive reports.

## Features

- 🔍 **Automated Code Scanning Alert Collection** - Fetches alerts from GitHub Code Scanning API
- 📊 **Repository-Focused Reports** - Executive summaries organized by repository
- 🎯 **Risk Scoring** - Prioritizes repositories based on severity and alert count
- 📈 **Detailed Technical Reports** - Complete alert information with file locations and line numbers
- 🌿 **Branch Tracking** - Records which branch was scanned for each repository
- 🔄 **Scope Management** - Scan specific repository groups defined in config
- 🧹 **Automatic Cleanup** - Removes temporary files after report generation

## What This Module Scans

This module analyzes **Code Scanning alerts**, which include:

- **CodeQL findings** - Semantic code analysis from GitHub's CodeQL engine
- **Third-party SAST tools** - Alerts from integrated security tools (Snyk, SonarQube, etc.)
- **Custom queries** - Results from custom CodeQL queries

**Alert Information Captured:**
- Rule ID and name
- Severity level (Critical, High, Medium, Low)
- Security severity classification
- Tool name and version
- File path and line numbers
- Alert state (open, fixed, dismissed)
- Timestamps and age tracking
- Dismissal reasons and comments

## Differences from Dependabot Scanner

| Feature | Dependabot Scanner | Code Scanning Scanner |
|---------|-------------------|----------------------|
| **Purpose** | Dependency vulnerabilities | Code-level security issues |
| **Alert Source** | Dependabot Alerts API | Code Scanning API |
| **Findings** | Vulnerable packages | Security flaws in code |
| **Tools** | GitHub Dependabot | CodeQL, Snyk, SonarQube, etc. |
| **Reports Folder** | `reports/` | `code_scanning_reports/` |
| **Module Files** | `vulnerability_scanner.py`<br>`security_report_generator.py`<br>`security_pipeline.py` | `code_scanning_scanner.py`<br>`code_scanning_report_generator.py`<br>`code_scanning_pipeline.py` |

## Installation

### Prerequisites

```powershell
# Python 3.8 or higher
python --version

# Install dependencies (shared with main Dependabot scanner)
pip install -r requirements.txt
```

### Configuration

The code scanning module uses the same `config.json` as the Dependabot scanner:

```json
{
  "github": {
    "enterprise_url": "https://github.boschdevcloud.com",
    "token": "your_github_token_here",
    "organization": "your-org-name"
  },
  "scopes": [
    {
      "name": "10R1",
      "description": "Release 10 R1 repositories",
      "repositories": [
        "repo-name-1",
        "repo-name-2"
      ]
    }
  ]
}
```

**Required GitHub Token Permissions:**
- `repo` (full repository access)
- `security_events` (read code scanning alerts)

## Usage

### Interactive Mode

```powershell
# Run the pipeline - it will prompt you to select a scope
python code_scanning_pipeline.py
```

### Command-Line Mode

```powershell
# Scan a specific scope
python code_scanning_pipeline.py --scope "10R1"

# Use a custom config file
python code_scanning_pipeline.py --config "./custom_config.json" --scope "10R1"

# Keep temporary files for debugging
python code_scanning_pipeline.py --scope "10R1" --keep-temp
```

### Programmatic Usage

```python
from code_scanning_pipeline import CodeScanningPipeline

# Initialize pipeline
pipeline = CodeScanningPipeline(config_path="./config.json")

# Run scan for specific scope
pipeline.run(scope_name="10R1", skip_cleanup=False)
```

## Output Structure

### Report Directory

```
code_scanning_reports/
└── 10R1_code_scanning_reports_20241111_120000/
    ├── executive_summary.csv
    ├── executive_summary.xlsx      🆕 Formatted Excel version
    ├── detailed_alerts.csv
    ├── detailed_alerts.xlsx         🆕 Formatted Excel version
    └── README.md
```

### Report File Formats

The Code Scanning module generates reports in two formats:

#### 📄 CSV Files (Plain Text)
- `executive_summary.csv` - Repository-focused summary
- `detailed_alerts.csv` - Complete alert details
- Best for: Automated processing, version control, scripts

#### 📊 Excel Files (Formatted) 🆕
- `executive_summary.xlsx` - Professionally formatted summary
- `detailed_alerts.xlsx` - Formatted detailed alerts
- Features:
  - **Blue headers** with white text for easy identification
  - **Auto-adjusted column widths** for optimal readability
  - **Borders** on all cells for clear data separation
  - **Frozen top row** for header visibility when scrolling
- Best for: Manual review, presentations, management reports

### Executive Summary (executive_summary.csv / .xlsx)

Repository-focused summary with risk scoring:

| Column | Description |
|--------|-------------|
| Priority Rank | Ranking based on risk score |
| Repository Name | Repository identifier |
| **Scanned Branch** 🆕 | Branch that was scanned |
| Risk Score | Calculated risk score |
| Total Open | Count of open alerts |
| Critical | Critical severity count |
| High | High severity count |
| Medium | Medium severity count |
| Low | Low severity count |
| Error | Error-level alerts |
| Warning | Warning-level alerts |
| Note | Note-level alerts |
| Total All Alerts | All alerts (open + fixed + dismissed) |
| Fixed Alerts | Count of fixed alerts |
| Dismissed Alerts | Count of dismissed alerts |

### Detailed Alerts (detailed_alerts.csv / .xlsx)

Complete alert information:

| Column | Description |
|--------|-------------|
| Repository Name | Repository identifier |
| **Scanned Branch** 🆕 | Branch that was scanned |
| Status | Alert state (OPEN, FIXED, DISMISSED) |
| Security Severity | Security-focused severity level |
| Rule Severity | General rule severity |
| Alert Title | Human-readable alert name |
| Rule ID | Unique rule identifier |
| Description | Detailed alert description |
| Tool | Analysis tool (CodeQL, Snyk, etc.) |
| Tool Version | Version of the analysis tool |
| File Path | Location of the security issue |
| Line | Line number in the file |
| Created At | When the alert was created |
| Fixed At | When the alert was fixed |
| Dismissed At | When the alert was dismissed |
| Dismissed By | User who dismissed the alert |
| Dismissal Reason | Reason for dismissal |
| Dismissal Comment | Additional dismissal comments |
| Alert URL | Direct link to alert on GitHub |
| Age (Days) | Days since alert was created |
| Tags | Associated security tags |

## Risk Scoring

Repositories are prioritized using a weighted risk scoring system:

| Severity | Weight |
|----------|--------|
| CRITICAL | 50 |
| HIGH | 20 |
| MEDIUM | 5 |
| LOW | 1 |
| ERROR | 20 |
| WARNING | 3 |
| NOTE | 1 |

**Formula:** `Risk Score = Σ(Alert Count × Severity Weight)`

## Examples

### Example 1: Quick Scan

```powershell
# Scan "10R1" scope repositories
python code_scanning_pipeline.py --scope "10R1"
```

### Example 2: Debug Run

```powershell
# Keep temporary files to inspect intermediate results
python code_scanning_pipeline.py --scope "10R1" --keep-temp
```

### Example 3: Custom Configuration

```powershell
# Use a different config file
python code_scanning_pipeline.py --config "./prod_config.json" --scope "production"
```

## Module Architecture

```
┌─────────────────────────────────────────┐
│   code_scanning_pipeline.py            │
│   (Orchestration & Workflow)            │
└────────────┬────────────────────────────┘
             │
             ├──> ┌────────────────────────────────┐
             │    │  code_scanning_scanner.py      │
             │    │  - Fetch alerts via API        │
             │    │  - Process alert data          │
             │    │  - Track repository metadata   │
             │    │  - Export JSON/CSV             │
             │    └────────────────────────────────┘
             │
             └──> ┌────────────────────────────────┐
                  │  code_scanning_report_generator.py │
                  │  - Load alert data             │
                  │  - Calculate risk scores       │
                  │  - Generate executive summary  │
                  │  - Create detailed reports     │
                  │  - Export CSV files            │
                  └────────────────────────────────┘
```

## Troubleshooting

### No Alerts Found

```
⚠️  No alert data found, showing all scoped repositories as clean
```

**Solution:** This is normal if repositories don't have Code Scanning enabled or have no security issues. The report will show all scoped repositories with zero alerts.

### Authentication Error

```
❌ Error: Bad credentials
```

**Solution:** Verify your GitHub token in `config.json` has the required permissions (`repo`, `security_events`).

### Repository Not Found

```
❌ Error: Repository not found: org-name/repo-name
```

**Solution:** 
- Check repository name spelling in `config.json`
- Verify your token has access to the repository
- Confirm the organization name is correct

### API Rate Limiting

```
⚠️  Rate limit exceeded
```

**Solution:** 
- Wait for the rate limit to reset
- Use a token with higher rate limits
- Reduce the number of repositories in the scope

## Branch Tracking Feature 🆕

The **Scanned Branch** column ensures you know which branch was analyzed:

- **Repositories with alerts**: Branch from the first alert
- **Repositories without alerts**: Branch from repository metadata
- **All repositories**: Default branch is captured early in the scan process

This prevents "N/A" values and provides complete branch information across all reports.

## Comparison with Dependabot Reports

Both modules follow the same reporting structure for consistency:

### Similarities
- ✅ Repository-focused executive summaries
- ✅ Detailed technical reports with all findings
- ✅ Risk scoring and prioritization
- ✅ Scanned branch tracking
- ✅ CSV export format
- ✅ Scope-based filtering
- ✅ Automatic cleanup of temporary files

### Key Differences
- **Alert Types**: Dependencies vs. code-level security issues
- **Severity Levels**: CVE scores vs. rule-based severity
- **Location Info**: Package names vs. file paths and line numbers
- **Tools**: Dependabot vs. CodeQL/SAST tools
- **Output Folder**: `reports/` vs. `code_scanning_reports/`

## Best Practices

1. **Regular Scanning**: Run code scanning alongside Dependabot scans for complete security coverage
2. **Scope Management**: Create focused scopes for different teams or release versions
3. **Branch Consistency**: Scan the same branch (usually `main` or `develop`) consistently
4. **Alert Triage**: Review high and critical alerts first using the priority ranking
5. **Integration**: Automate scanning in CI/CD pipelines for continuous monitoring

## Support

For issues or questions:
- Check the main `README.md` in the root directory
- Review the `config.json.sample` for configuration examples
- Examine generated `README.md` files in report directories for scan-specific details

## Version

**Version:** 1.0.0  
**Last Updated:** November 2024  
**Compatible With:** GitHub Enterprise Server, GitHub.com
