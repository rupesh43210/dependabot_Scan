# Code Scanning Pipeline Launcher
# Automatically activates venv and runs the code scanning pipeline

param(
    [string]$Scope,
    [string]$Config = ".\config.json",
    [switch]$KeepTemp
)

Write-Host "🛡️  Code Scanning Pipeline Launcher" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Check if venv exists
if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment activated`n" -ForegroundColor Green

# Build command
$command = "python code_scanning_pipeline.py"

if ($Config) {
    $command += " --config `"$Config`""
}

if ($Scope) {
    $command += " --scope `"$Scope`""
}

if ($KeepTemp) {
    $command += " --keep-temp"
}

# Run the pipeline
Write-Host "🚀 Running: $command`n" -ForegroundColor Cyan
Invoke-Expression $command

$exitCode = $LASTEXITCODE

# Deactivate is automatic when script ends
if ($exitCode -eq 0) {
    Write-Host "`n✅ Pipeline completed successfully" -ForegroundColor Green
} else {
    Write-Host "`n❌ Pipeline failed with exit code: $exitCode" -ForegroundColor Red
}

exit $exitCode
