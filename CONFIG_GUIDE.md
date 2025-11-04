# GitHub Issue Creator - Configuration Guide

## Overview

The GitHub Issue Creator now supports flexible configuration through JSON files, allowing you to easily customize:
- Project assignments
- Labels and colors
- Issue title formats
- GitHub organization settings
- And much more!

## Configuration Files

### Default Configuration
The tool uses `issue_config.json` as the default configuration file. If this file doesn't exist, the tool will use built-in defaults.

### Current Default Settings
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
      }
    ],
    "auto_assign_project": true,
    "include_timestamp": false
  },
  "github_settings": {
    "organization": "MiDAS",
    "base_url": "https://github.boschdevcloud.com"
  }
}
```

## Usage Examples

### Basic Usage (Default Configuration)
```bash
# Uses issue_config.json or built-in defaults
python create_security_issues.py --auto
```

### Custom Configuration File
```bash
# Use a specific configuration file
python create_security_issues.py --auto --config my_custom_config.json
```

### Override Settings via Command Line
```bash
# Use config file but override specific settings
python create_security_issues.py --auto --config custom_config.json --project "Emergency Team"
python create_security_issues.py --auto --labels "urgent,security,critical"
python create_security_issues.py --auto --label-color "#ff0000"
```

## Configuration Options

### Issue Settings
- **default_project**: Default project name for assignment
- **project_number**: GitHub project number (for automatic assignment)
- **labels**: Array of label configurations with name, color, and description
- **title_format**: Template for issue titles (supports placeholders)
- **auto_assign_project**: Whether to automatically assign issues to projects
- **include_timestamp**: Whether to include creation timestamp in issue body
- **force_update_existing**: Default behavior for updating existing issues

### GitHub Settings
- **organization**: GitHub organization name
- **base_url**: GitHub base URL (for Enterprise GitHub)

### Severity Settings
- **minimum_severity**: Minimum severity level to include
- **severity_order**: Order of severity levels
- **severity_colors**: Color mapping for severity levels

### Report Settings
- **default_reports_directory**: Default directory for scan reports
- **supported_formats**: Supported file formats
- **auto_detect_latest**: Whether to auto-detect latest scan

### Advanced Settings
- **batch_size**: API batch processing size
- **api_timeout**: API request timeout
- **retry_attempts**: Number of retry attempts
- **enable_debug_logging**: Enable detailed logging

## Configuration Examples

### Example 1: Different Project and Multiple Labels
```json
{
  "issue_settings": {
    "default_project": "Security Team",
    "project_number": 15,
    "labels": [
      {
        "name": "security",
        "color": "d73a4a",
        "description": "Security-related issue"
      },
      {
        "name": "critical", 
        "color": "ff0000",
        "description": "Critical priority issue"
      },
      {
        "name": "dependabot",
        "color": "0366d6", 
        "description": "Dependabot security alert"
      }
    ],
    "include_timestamp": true
  }
}
```

### Example 2: Minimal Configuration (Just Override Project)
```json
{
  "issue_settings": {
    "default_project": "DevOps Team",
    "project_number": 8
  }
}
```

### Example 3: Custom Title Format
```json
{
  "issue_settings": {
    "title_format": "[SECURITY] {repository} - {critical} Critical, {high} High vulnerabilities found",
    "labels": [
      {
        "name": "security-alert",
        "color": "e11d21",
        "description": "Security vulnerability alert"
      }
    ]
  }
}
```

### Example 4: Different Organization
```json
{
  "github_settings": {
    "organization": "MyCompany",
    "base_url": "https://github.com"
  },
  "issue_settings": {
    "default_project": "Security Response",
    "project_number": 1
  }
}
```

## Title Format Placeholders

The title format supports these placeholders:
- `{repository}`: Repository name
- `{critical}`: Number of critical vulnerabilities  
- `{high}`: Number of high vulnerabilities
- `{medium}`: Number of medium vulnerabilities
- `{low}`: Number of low vulnerabilities

Example:
```
"{repository} - Fix all dependabot issues Critical - {critical:02d}, High - {high:02d}, Medium - {medium:02d}, Low - {low:02d}"
```

## Command Line Override Priority

Settings are applied in this order (later overrides earlier):
1. Built-in defaults
2. Configuration file settings
3. Command line arguments

## Managing Configurations

### View Current Configuration
```bash
python config_manager.py
```

### Generate Example Configurations
```bash
python config_examples.py
```

### Test Different Configurations
The tool will validate your configuration on startup and show any errors or warnings.

## Best Practices

1. **Start with minimal config**: Only override what you need to change
2. **Test configurations**: Use the config examples to test before production use
3. **Version control**: Keep your configuration files in version control
4. **Validate colors**: Ensure hex colors don't include the # prefix in the config file
5. **Project numbers**: Verify project numbers match your GitHub projects

## Troubleshooting

### Configuration Not Loading
- Check JSON syntax with a validator
- Ensure file path is correct
- Check file permissions

### Colors Not Applying
- Remove # prefix from hex colors in config file
- Use 6-digit hex codes (e.g., "fbca04" not "fbc")

### Project Assignment Failing
- Verify project number matches your GitHub project
- Ensure you have permissions to assign to the project
- Check that the project exists in your organization

## Migration from Command Line Arguments

If you were using command line arguments, you can move them to config files:

**Before:**
```bash
python create_security_issues.py --auto --project "OPL Management" --labels "security-Vulnerability" --label-color "#fbca04"
```

**After (in config file):**
```json
{
  "issue_settings": {
    "default_project": "OPL Management", 
    "labels": [
      {
        "name": "security-Vulnerability",
        "color": "fbca04"
      }
    ]
  }
}
```

**New usage:**
```bash
python create_security_issues.py --auto
```

This makes the tool much more maintainable and allows for team-wide configuration standards!