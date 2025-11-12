# Configuration Folder

This folder contains **application-specific configuration** files for the Security Scanner project.

> **📍 Important**: The `.env` file remains in the **project root** (not in this folder) following the 12-factor app methodology and industry best practices. Tools like `python-dotenv` expect environment files at the project root.

## Files

### config.json
Main configuration file containing:
- **scan settings**: Output directories, active scope
- **scopes**: Repository groupings
- **responsibles**: Team assignments (optional)

**Note:** This file is gitignored as it may contain user-specific settings.

### config.json.sample
Template configuration file with example structure. Copy this to `config.json` and customize for your environment.

## Usage

1. **First Time Setup:**
   ```bash
   cp config/config.json.sample config/config.json
   # Edit config/config.json with your settings
   ```

2. **Configuration Structure:**
   ```json
   {
     "scan": {
       "output_dir": "./reports",
       "dependabot_output_dir": "./reports/dependabot_alerts",
       "codeql_output_dir": "./reports/codeql_alerts",
       "active_scope": "10R1"
     },
     "scopes": {
       "10R1": ["repo1", "repo2", "repo3"]
     }
   }
   ```

3. **Environment Variables:**
   Configure sensitive data in `.env` file in project root:
   ```
   GITHUB_TOKEN=your_token_here
   GITHUB_ENTERPRISE_URL=https://github.your-company.com
   GITHUB_ORG=your-org-name
   ```

## Best Practices

- ✅ Keep `config.json` out of version control (gitignored)
- ✅ Update `config.json.sample` when adding new configuration options
- ✅ Document all configuration options
- ✅ Use environment variables for sensitive data

## Configuration Options

### scan settings
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `output_dir` | string | Base output directory | `./reports` |
| `dependabot_output_dir` | string | Dependabot reports location | `./reports/dependabot_alerts` |
| `codeql_output_dir` | string | Code Scanning reports location | `./reports/codeql_alerts` |
| `active_scope` | string | Default scope to use | - |

### scopes
Dictionary mapping scope names to lists of repository names.

Example:
```json
{
  "scopes": {
    "critical": ["app1", "app2"],
    "10R1": ["MiDAS-Platform", "MBD-UTA"]
  }
}
```

### responsibles (optional)
Maps repositories to responsible teams/individuals.

Example:
```json
{
  "responsibles": {
    "repo1": "Team A",
    "repo2": "Team B"
  }
}
```
