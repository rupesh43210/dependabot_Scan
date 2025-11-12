# Report Organization Structure

## Overview
Reports are now organized into two main subfolders under `./reports/`:

```
reports/
├── dependabot_alerts/          # Dependabot vulnerability reports
│   └── 10R1_security_reports_YYYYMMDD_HHMMSS/
│       ├── executive_summary.csv
│       ├── executive_summary.xlsx
│       ├── detailed_vulnerabilities.csv
│       ├── detailed_vulnerabilities.xlsx
│       ├── executive_kpi_summary.csv
│       └── README.md
│
└── codeql_alerts/             # Code Scanning (CodeQL/SAST) reports
    └── 10R1_code_scanning_reports_YYYYMMDD_HHMMSS/
        ├── executive_summary.csv
        ├── detailed_alerts.csv
        └── README.md
```

## Configuration

### config.json Settings

```json
{
  "scan": {
    "output_dir": "./reports",                              // Base directory (legacy)
    "dependabot_output_dir": "./reports/dependabot_alerts", // Dependabot reports
    "codeql_output_dir": "./reports/codeql_alerts",        // Code Scanning reports
    ...
  }
}
```

### Customization

You can customize the output directories by modifying `config.json`:

**Example 1: Different root folders**
```json
{
  "scan": {
    "dependabot_output_dir": "./security_scans/dependencies",
    "codeql_output_dir": "./security_scans/code_analysis"
  }
}
```

**Example 2: Team-specific folders**
```json
{
  "scan": {
    "dependabot_output_dir": "./team_reports/backend/dependabot",
    "codeql_output_dir": "./team_reports/backend/codeql"
  }
}
```

**Example 3: Date-based organization**
```json
{
  "scan": {
    "dependabot_output_dir": "./reports/2024/dependabot",
    "codeql_output_dir": "./reports/2024/codeql"
  }
}
```

## Benefits

### 1. Clear Separation
- **Dependabot alerts** focus on vulnerable dependencies
- **CodeQL alerts** focus on code-level security issues
- No confusion between alert types

### 2. Easy Navigation
```powershell
# View all Dependabot reports
cd reports/dependabot_alerts

# View all CodeQL reports
cd reports/codeql_alerts
```

### 3. Independent Management
- Archive Dependabot reports separately
- Share CodeQL reports with different teams
- Apply different retention policies

### 4. Scalability
- Add more alert types in the future (e.g., `container_scanning`, `secret_detection`)
- Maintain consistent structure as your security tooling grows

## Usage

### Running Scans

**Dependabot Scan:**
```powershell
.\venv\Scripts\Activate.ps1
python security_pipeline.py --scope "scoped"
```
Reports saved to: `./reports/dependabot_alerts/10R1_security_reports_YYYYMMDD_HHMMSS/`

**CodeQL Scan:**
```powershell
.\venv\Scripts\Activate.ps1
python code_scanning_pipeline.py --scope "scoped"
```
Reports saved to: `./reports/codeql_alerts/10R1_code_scanning_reports_YYYYMMDD_HHMMSS/`

### Viewing Latest Reports

**PowerShell:**
```powershell
# Latest Dependabot report
cd (Get-ChildItem ".\reports\dependabot_alerts" | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName

# Latest CodeQL report
cd (Get-ChildItem ".\reports\codeql_alerts" | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

**Bash/Linux:**
```bash
# Latest Dependabot report
cd $(ls -td ./reports/dependabot_alerts/*/ | head -1)

# Latest CodeQL report
cd $(ls -td ./reports/codeql_alerts/*/ | head -1)
```

## Report Comparison

| Aspect | Dependabot Reports | CodeQL Reports |
|--------|-------------------|----------------|
| **Location** | `reports/dependabot_alerts/` | `reports/codeql_alerts/` |
| **Focus** | Vulnerable dependencies | Code security flaws |
| **Alert Types** | CVEs in packages | Security patterns in code |
| **Severity** | CRITICAL, HIGH, MEDIUM, LOW | CRITICAL, HIGH, MEDIUM, LOW, ERROR, WARNING, NOTE |
| **Fix Approach** | Update package versions | Modify source code |
| **Files** | executive_summary.xlsx, detailed_vulnerabilities.xlsx | executive_summary.csv, detailed_alerts.csv |

## Migration Notes

### Existing Reports
- Old reports in `./reports/` remain unchanged
- New scans will use the new subfolder structure
- No automatic migration of old reports

### Moving Old Reports (Optional)
```powershell
# Move old Dependabot reports
Move-Item ".\reports\10R1_security_reports_*" ".\reports\dependabot_alerts\"

# Move old CodeQL reports (if any)
Move-Item ".\reports\*code_scanning*" ".\reports\codeql_alerts\"
```

## Best Practices

### 1. Regular Cleanup
```powershell
# Keep only last 30 days of reports
$cutoffDate = (Get-Date).AddDays(-30)
Get-ChildItem ".\reports\*\*" -Directory | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate } | 
    Remove-Item -Recurse -Force
```

### 2. Archiving
```powershell
# Archive old reports monthly
$month = (Get-Date).AddMonths(-1).ToString("yyyy-MM")
Compress-Archive -Path ".\reports\dependabot_alerts\*$month*" -DestinationPath ".\archive\dependabot_$month.zip"
Compress-Archive -Path ".\reports\codeql_alerts\*$month*" -DestinationPath ".\archive\codeql_$month.zip"
```

### 3. Monitoring
```powershell
# Count alerts by type
$dependabotReports = Get-ChildItem ".\reports\dependabot_alerts" -Recurse -Filter "executive_summary.csv"
$codeqlReports = Get-ChildItem ".\reports\codeql_alerts" -Recurse -Filter "executive_summary.csv"

Write-Host "Dependabot Reports: $($dependabotReports.Count)"
Write-Host "CodeQL Reports: $($codeqlReports.Count)"
```

## Troubleshooting

### Reports Not Appearing in New Location

**Check config.json:**
```powershell
Get-Content config.json | Select-String "output_dir"
```

**Expected output:**
```
"output_dir": "./reports",
"dependabot_output_dir": "./reports/dependabot_alerts",
"codeql_output_dir": "./reports/codeql_alerts",
```

### Permission Issues

Ensure the directories are writable:
```powershell
New-Item -Path ".\reports\dependabot_alerts" -ItemType Directory -Force
New-Item -Path ".\reports\codeql_alerts" -ItemType Directory -Force
```

### Old Reports Mixed with New

If you have old reports in `./reports/`, manually move them:
```powershell
# Create subfolders if they don't exist
New-Item -Path ".\reports\dependabot_alerts" -ItemType Directory -Force
New-Item -Path ".\reports\codeql_alerts" -ItemType Directory -Force

# Move security reports to dependabot folder
Get-ChildItem ".\reports\*security_reports*" -Directory | 
    Move-Item -Destination ".\reports\dependabot_alerts\"

# Move code scanning reports to codeql folder
Get-ChildItem ".\reports\*code_scanning*" -Directory | 
    Move-Item -Destination ".\reports\codeql_alerts\"
```

## Summary

✅ **Organized Structure**: Clear separation between Dependabot and CodeQL reports  
✅ **Configurable**: Easy to customize via config.json  
✅ **Backward Compatible**: Existing security_pipeline.py and code_scanning_pipeline.py work seamlessly  
✅ **Scalable**: Ready for additional security scanning tools in the future  
✅ **Easy Navigation**: Logical folder structure for quick access
