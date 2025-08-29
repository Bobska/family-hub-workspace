# Simple FamilyHub Server Launcher
# Fixed version without encoding issues

param(
    [int]$Port = 8000,
    [string]$ServerHost = "127.0.0.1",
    [switch]$NoReload
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        "Magenta" { Write-Host $Message -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

function Start-FamilyHubServer {
    Write-ColorOutput "Starting FamilyHub Server..." "Green"
    Write-ColorOutput "============================" "Green"
    Write-Host ""
    
    # Get workspace root directory
    $workspaceRoot = Split-Path -Parent $PSScriptRoot
    $familyHubPath = Join-Path $workspaceRoot "FamilyHub"
    
    # Check if FamilyHub directory exists
    if (-not (Test-Path $familyHubPath)) {
        Write-ColorOutput "ERROR: FamilyHub directory not found at: $familyHubPath" "Red"
        return
    }
    
    Write-ColorOutput "Workspace: $workspaceRoot" "Cyan"
    Write-ColorOutput "FamilyHub Path: $familyHubPath" "Cyan"
    Write-Host ""
    
    # Navigate to FamilyHub directory
    Set-Location $familyHubPath
    Write-ColorOutput "Current Directory: $(Get-Location)" "Yellow"
    
    # Check if virtual environment exists
    $venvPath = Join-Path $familyHubPath "venv"
    if (-not (Test-Path $venvPath)) {
        Write-ColorOutput "WARNING: Virtual environment not found at: $venvPath" "Yellow"
        Write-ColorOutput "Attempting to run without virtual environment..." "Yellow"
    } else {
        Write-ColorOutput "Activating virtual environment..." "Green"
        $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            & $activateScript
            Write-ColorOutput "Virtual environment activated" "Green"
        } else {
            Write-ColorOutput "WARNING: Activate script not found, using system Python" "Yellow"
        }
    }
    
    # Set Django settings module
    $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings.development"
    Write-ColorOutput "Django Settings: $env:DJANGO_SETTINGS_MODULE" "Cyan"
    
    # Check if manage.py exists
    $managePath = Join-Path $familyHubPath "manage.py"
    if (-not (Test-Path $managePath)) {
        Write-ColorOutput "ERROR: manage.py not found at: $managePath" "Red"
        return
    }
    
    # Run system checks
    Write-ColorOutput "Running Django system checks..." "Yellow"
    python manage.py check --verbosity=0
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "WARNING: System checks failed, but continuing..." "Yellow"
    } else {
        Write-ColorOutput "System checks passed" "Green"
    }
    
    # Check for pending migrations
    Write-ColorOutput "Checking for pending migrations..." "Yellow"
    $migrationCheck = python manage.py showmigrations --plan | Select-String "\[ \]"
    if ($migrationCheck) {
        Write-ColorOutput "Found pending migrations. Running makemigrations and migrate..." "Yellow"
        
        # Run makemigrations
        python manage.py makemigrations
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Makemigrations completed" "Green"
        } else {
            Write-ColorOutput "WARNING: Makemigrations had issues" "Yellow"
        }
        
        # Run migrate
        python manage.py migrate
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Migrations applied successfully" "Green"
        } else {
            Write-ColorOutput "WARNING: Migration application failed" "Red"
        }
    } else {
        Write-ColorOutput "All migrations are up to date" "Green"
    }
    
    Write-Host ""
    Write-ColorOutput "SERVER INFORMATION:" "Magenta"
    Write-ColorOutput "==================" "Magenta"
    Write-Host "  Server URL:   http://$ServerHost`:$Port/"
    Write-Host "  Admin Panel:  http://$ServerHost`:$Port/admin/"
    Write-Host "  Credentials:  admin / admin"
    Write-Host "  Settings:     $env:DJANGO_SETTINGS_MODULE"
    Write-Host ""
    Write-ColorOutput "Press Ctrl+C to stop the server" "Yellow"
    Write-Host ""
    
    # Start the server
    try {
        if ($NoReload) {
            python manage.py runserver "$ServerHost`:$Port" --noreload
        } else {
            python manage.py runserver "$ServerHost`:$Port"
        }
    }
    catch {
        Write-ColorOutput "Server stopped or encountered an error" "Red"
    }
    finally {
        Write-ColorOutput "FamilyHub server stopped" "Yellow"
    }
}

# Main execution
Start-FamilyHubServer
