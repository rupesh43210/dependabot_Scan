# 📁 Project Structure

## Optimized Organization (v2.0)

This project has been reorganized for better maintainability, modularity, and scalability.

```
dependabot_Scan/
├── 📂 src/                          # Source code (organized by function)
│   ├── 📂 scanners/                 # Vulnerability scanning modules
│   │   ├── __init__.py
│   │   ├── vulnerability_scanner.py      # Dependabot scanner
│   │   └── code_scanning_scanner.py      # Code Scanning scanner
│   │
│   ├── 📂 reporters/                # Report generation modules
│   │   ├── __init__.py
│   │   ├── security_report_generator.py  # Dependabot reports
│   │   └── code_scanning_report_generator.py  # Code Scanning reports
│   │
│   ├── 📂 issue_managers/           # GitHub issue management
│   │   ├── __init__.py
│   │   ├── github_issue_manager.py       # Core issue manager
│   │   ├── create_security_issues.py     # Issue creation
│   │   ├── update_open_issue_status.py   # Issue updates
│   │   ├── close_fixed_issues.py         # Close fixed issues
│   │   ├── reopen_fixed.py               # Reopen issues
│   │   ├── add_to_project.py             # Project management
│   │   └── graphql_assign_issues.py      # GraphQL assignments
│   │
│   ├── 📂 utils/                    # Shared utilities
│   │   ├── __init__.py
│   │   ├── config_loader.py              # Configuration handling
│   │   └── logger.py                     # Logging utilities
│   │
│   ├── security_pipeline.py         # Dependabot pipeline
│   ├── code_scanning_pipeline.py    # Code Scanning pipeline
│   └── __init__.py
│
├── 📂 docs/                         # Documentation
│   ├── CODE_SCANNING_README.md
│   ├── CODE_SCANNING_IMPLEMENTATION.md
│   ├── REPORT_ORGANIZATION.md
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 📂 scripts/                      # Utility scripts
│   ├── setup_env.py                 # Environment setup
│   ├── run_security_pipeline.ps1   # PowerShell runner
│   └── run_code_scanning.ps1       # PowerShell runner
│
├── 📂 reports/                      # Generated reports
│   ├── dependabot_alerts/           # Dependabot scan results
│   └── codeql_alerts/               # Code Scanning results
│
├── 📂 venv/                         # Python virtual environment
├── 📂 __pycache__/                  # Python cache (gitignored)
│
├── 🐍 run_dependabot.py             # Main entry point - Dependabot
├── 🐍 run_code_scanning.py          # Main entry point - Code Scanning
│
├── 📄 config.json                   # Configuration file
├── 📄 config.json.sample            # Configuration template
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env                          # Environment variables (gitignored)
├── 📄 .env.sample                   # Environment template
├── 📄 .gitignore                    # Git ignore rules
└── 📄 README.md                     # Main documentation
```

---

## 🎯 Module Responsibilities

### Scanners (`src/scanners/`)
- **vulnerability_scanner.py**: Scans Dependabot alerts via GitHub API
- **code_scanning_scanner.py**: Scans Code Scanning alerts (CodeQL, Snyk, etc.)

### Reporters (`src/reporters/`)
- **security_report_generator.py**: Generates Dependabot reports (CSV/Excel)
- **code_scanning_report_generator.py**: Generates Code Scanning reports (CSV/Excel)
- Both include severity color coding and risk scoring

### Issue Managers (`src/issue_managers/`)
- **github_issue_manager.py**: Core GitHub API interaction for issue management
- **create_security_issues.py**: Automated issue creation from scans
- **update_open_issue_status.py**: Updates existing issues with new scan data
- **close_fixed_issues.py**: Closes issues for fixed vulnerabilities
- **reopen_fixed.py**: Reopens issues if vulnerabilities return
- **add_to_project.py**: Adds issues to GitHub Projects
- **graphql_assign_issues.py**: Assigns issues using GraphQL API

### Utilities (`src/utils/`)
- **config_loader.py**: Configuration file handling and validation
- **logger.py**: Centralized logging setup

---

## 🚀 Quick Start with New Structure

### Option 1: Python Entry Points (Recommended)

```bash
# Run Dependabot scanner
python run_dependabot.py --scope "10R1"

# Run Code Scanning scanner
python run_code_scanning.py --scope "scoped"
```

### Option 2: Direct Module Execution

```bash
# From root directory
python -m src.security_pipeline --scope "10R1"
python -m src.code_scanning_pipeline --scope "scoped"
```

### Option 3: PowerShell Scripts

```powershell
# Run from scripts folder
.\scripts\run_security_pipeline.ps1
.\scripts\run_code_scanning.ps1
```

---

## 🔄 Migration from Old Structure

### What Changed?

#### Before (v1.x):
```
├── vulnerability_scanner.py
├── security_report_generator.py
├── code_scanning_scanner.py
├── code_scanning_report_generator.py
├── github_issue_manager.py
├── security_pipeline.py
├── code_scanning_pipeline.py
└── (scattered files)
```

#### After (v2.0):
```
├── src/
│   ├── scanners/
│   ├── reporters/
│   ├── issue_managers/
│   ├── utils/
│   └── pipelines
└── (organized structure)
```

### Backwards Compatibility

**Old files are preserved** in the root directory for backwards compatibility. You can still run:
```bash
python security_pipeline.py --scope "10R1"
python code_scanning_pipeline.py --scope "scoped"
```

However, it's recommended to migrate to the new entry points:
```bash
python run_dependabot.py --scope "10R1"
python run_code_scanning.py --scope "scoped"
```

---

## 📦 Benefits of New Structure

### 1. **Modularity**
- Each module has a single, well-defined responsibility
- Easier to test individual components
- Reusable across different pipelines

### 2. **Maintainability**
- Logical grouping of related functionality
- Easier to locate and modify code
- Clear separation of concerns

### 3. **Scalability**
- Easy to add new scanners (e.g., `src/scanners/sonarqube_scanner.py`)
- Easy to add new reporters (e.g., `src/reporters/pdf_generator.py`)
- Pluggable architecture

### 4. **Import Clarity**
```python
# Old way
from vulnerability_scanner import VulnerabilityScanner

# New way (more explicit)
from scanners.vulnerability_scanner import VulnerabilityScanner
```

### 5. **Better Testing**
- Unit tests can import specific modules
- Mock dependencies easily
- Test utilities independently

---

## 🔧 Development Guidelines

### Adding a New Scanner

1. Create scanner in `src/scanners/`:
```python
# src/scanners/new_scanner.py
class NewScanner:
    def __init__(self, config):
        self.config = config
    
    def scan(self):
        # Implementation
        pass
```

2. Add to `src/scanners/__init__.py`:
```python
from .new_scanner import NewScanner
__all__ = [..., 'NewScanner']
```

3. Create corresponding reporter in `src/reporters/`

4. Create pipeline in `src/new_pipeline.py`

5. Create entry point: `run_new_scanner.py`

### Adding Utilities

Add shared functionality to `src/utils/`:
- Configuration helpers
- Data processing utilities
- API wrappers
- Formatting functions

---

## 📝 Import Examples

### From Pipeline Scripts

```python
# In src/security_pipeline.py
from scanners.vulnerability_scanner import VulnerabilityScanner
from reporters.security_report_generator import SecurityReportGenerator
from utils.config_loader import load_config
from utils.logger import setup_logger
```

### From Root Entry Points

```python
# In run_dependabot.py
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from security_pipeline import SecurityPipeline
```

---

## 🗑️ Cleanup (Optional)

Once you're comfortable with the new structure, you can remove old files:

```powershell
# Remove old scanner files from root
Remove-Item vulnerability_scanner.py, code_scanning_scanner.py

# Remove old reporter files
Remove-Item security_report_generator.py, code_scanning_report_generator.py

# Remove old issue manager files
Remove-Item github_issue_manager.py, create_security_issues.py, etc.

# Remove old documentation from root
Remove-Item CODE_SCANNING_*.md, REPORT_ORGANIZATION.md

# Keep these in root:
# - run_dependabot.py
# - run_code_scanning.py
# - config.json
# - requirements.txt
# - .env
# - README.md
```

**Note**: The old `security_pipeline.py` and `code_scanning_pipeline.py` in root can be kept for backward compatibility or removed once all users migrate to new entry points.

---

## 🎓 Learning Path

1. **Start Simple**: Use the new `run_dependabot.py` or `run_code_scanning.py`
2. **Explore Modules**: Look at individual modules in `src/` folders
3. **Understand Utils**: Check utility functions in `src/utils/`
4. **Customize**: Extend scanners or reporters for your needs

---

## 📞 Support

If you encounter issues with the new structure:
1. Check this documentation
2. Review `README.md` for usage examples
3. Check individual module docstrings
4. Fall back to old entry points if needed

---

## 🔮 Future Enhancements

Planned improvements:
- [ ] Add unit tests in `tests/` directory
- [ ] Add integration tests
- [ ] Create plugin system for custom scanners
- [ ] Add configuration validation tool
- [ ] Create CLI with `click` or `typer`
- [ ] Package as installable Python package
- [ ] Add Docker support
- [ ] Create web dashboard
