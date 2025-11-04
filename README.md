# Security Vulnerability Scanner & GitHub Issue Creator

A comprehensive tool for scanning GitHub repositories for Dependabot security vulnerabilities and automatically creating organized GitHub issues for tracking and resolution.

## 🚀 Features

- **Automated vulnerability scanning** across multiple repositories
- **Automatic GitHub issue creation** with detailed vulnerability information
- **Flexible configuration system** for labels, projects, and formatting
- **Project assignment integration** with GitHub Projects (Beta)
- **Duplicate issue prevention** to avoid creating redundant issues
- **Multiple label support** with custom colors and descriptions
- **Enterprise GitHub support** for organizations using GitHub Enterprise
- **Comprehensive reporting** with CSV and summary outputs

## 📋 Quick Start

### 1. Setup Environment
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your GitHub token and organization details
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Vulnerability Scan
```bash
# Scan all repositories and generate reports
python security_pipeline.py
```

### 4. Create GitHub Issues
```bash
# Create issues from latest scan with default settings
python create_security_issues.py --auto
```

## 🔧 Configuration

### Issue Configuration (`issue_config.json`)

The tool uses a flexible JSON configuration system. Here's how to configure multiple labels:

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
├── ⚙️ config_manager.py            # Configuration management
├── 📋 github_issue_manager.py       # GitHub API integration
├── 📊 security_report_generator.py  # Report generation
├── 🔍 vulnerability_scanner.py      # Vulnerability scanning logic
├── 📝 issue_config.json            # Issue creation configuration
├── 🌍 .env                         # Environment variables (create from .env.example)
├── 📦 requirements.txt             # Python dependencies
├── 📖 CONFIG_GUIDE.md              # Detailed configuration guide
├── reports/                        # Generated reports directory
│   └── security_reports_*/
│       ├── detailed_vulnerabilities.csv
│       ├── executive_summary.csv
│       └── executive_kpi_summary.csv
└── venv/                          # Virtual environment (auto-created)
```

## 🎯 Usage Examples

### Basic Usage
```bash
# Full workflow: scan and create issues
python security_pipeline.py
python create_security_issues.py --auto

# View current configuration
python config_manager.py

# Generate configuration examples
python config_examples.py
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
2. **Rotate tokens regularly** - Update GitHub tokens periodically
3. **Limit token permissions** - Use tokens with minimal required scopes
4. **Review configurations** - Keep sensitive data out of config files
5. **Use virtual environments** - Isolate dependencies

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
```

### Debug Mode
Enable debug logging in configuration:
```json
{
  "advanced_settings": {
    "enable_debug_logging": true
  }
}
```

## 🤝 Contributing

1. Follow existing code structure and patterns
2. Update configuration examples when adding new features
3. Ensure sensitive data never enters version control
4. Test with different GitHub Enterprise configurations
5. Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review configuration examples
3. Validate environment setup
4. Check GitHub API connectivity

---

**Quick Reference Commands:**
```bash
# Complete workflow
python security_pipeline.py && python create_security_issues.py --auto

# Configuration management  
python config_manager.py                    # View current config
python config_examples.py                   # Generate examples

# Custom configurations
python create_security_issues.py --auto --config team_config.json
python create_security_issues.py --auto --labels "urgent,security,p1"
python create_security_issues.py --auto --project "Emergency Response"
```