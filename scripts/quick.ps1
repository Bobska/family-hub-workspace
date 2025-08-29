# Universal Quick Launcher for FamilyHub Development
# One script to rule them all - launches any development environment

param(
    [string]$App = "help",
    [int]$Port,
    [string]$ServerHost = "127.0.0.1",
    [switch]$NoReload,
    [switch]$Both
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

function Show-Help {
    Write-ColorOutput "FamilyHub Universal Quick Launcher" "Cyan"
    Write-ColorOutput "====================================" "Cyan"
    Write-Host ""
    Write-ColorOutput "Available Commands:" "Yellow"
    Write-Host "  familyhub   - Start FamilyHub integrated environment (port 8000)"
    Write-Host "  timesheet   - Start standalone timesheet app (port 8001)"
    Write-Host "  both        - Start both servers simultaneously"
    Write-Host "  status      - Show current server status"
    Write-Host "  docker      - Show Docker container status"
    Write-Host "  superusers  - Manage superusers across environments"
    Write-Host "  migrate     - Run migrations for both environments"
    Write-Host ""
    Write-ColorOutput "Examples:" "Green"
    Write-Host "  .\scripts\quick.ps1 familyhub"
    Write-Host "  .\scripts\quick.ps1 timesheet"
    Write-Host "  .\scripts\quick.ps1 both"
    Write-Host "  .\scripts\quick.ps1 migrate"
    Write-Host "  .\scripts\quick.ps1 familyhub -Port 8080"
    Write-Host "  .\scripts\quick.ps1 timesheet -NoReload"
    Write-Host ""
    Write-ColorOutput "Quick URLs:" "Magenta"
    Write-Host "  FamilyHub:     http://127.0.0.1:8000/"
    Write-Host "  Timesheet:     http://127.0.0.1:8001/"
    Write-Host "  FamilyHub Admin: http://127.0.0.1:8000/admin/"
    Write-Host "  Timesheet Admin: http://127.0.0.1:8001/admin/"
    Write-Host ""
    Write-ColorOutput "Default Credentials: admin / admin" "Magenta"
}

function Start-FamilyHub {
    $defaultPort = if ($Port) { $Port } else { 8000 }
    Write-ColorOutput "Starting FamilyHub..." "Green"
    
    $scriptPath = Join-Path $PSScriptRoot "start_familyhub.ps1"
    if ($NoReload) {
        & $scriptPath -Port $defaultPort -ServerHost $ServerHost -NoReload
    } else {
        & $scriptPath -Port $defaultPort -ServerHost $ServerHost
    }
}

function Start-Timesheet {
    $defaultPort = if ($Port) { $Port } else { 8001 }
    Write-ColorOutput "Starting Timesheet..." "Green"
    
    $scriptPath = Join-Path $PSScriptRoot "start_timesheet.ps1"
    if ($NoReload) {
        & $scriptPath -Port $defaultPort -ServerHost $ServerHost -NoReload
    } else {
        & $scriptPath -Port $defaultPort -ServerHost $ServerHost
    }
}

function Start-Both {
    Write-ColorOutput "Starting Both Servers..." "Cyan"
    Write-ColorOutput "========================" "Cyan"
    Write-Host ""
    Write-ColorOutput "This will start:" "Yellow"
    Write-Host "  - FamilyHub on http://127.0.0.1:8000/"
    Write-Host "  - Timesheet on http://127.0.0.1:8001/"
    Write-Host ""
    Write-ColorOutput "Note: You'll need to open two PowerShell windows to run both servers." "Yellow"
    Write-Host ""
    Write-ColorOutput "Commands to run in separate windows:" "Green"
    Write-Host "  Window 1: .\scripts\quick.ps1 familyhub"
    Write-Host "  Window 2: .\scripts\quick.ps1 timesheet"
    Write-Host ""
    Write-ColorOutput "Or use the individual start scripts:" "Green"
    Write-Host "  Window 1: .\scripts\start_familyhub.ps1"
    Write-Host "  Window 2: .\scripts\start_timesheet.ps1"
}

function Show-Status {
    Write-ColorOutput "Server Status Report" "Cyan"
    Write-ColorOutput "====================" "Cyan"
    Write-Host ""
    
    # Check if servers are running by testing ports
    try {
        $familyHubTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 8000 -WarningAction SilentlyContinue
        $timesheetTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 8001 -WarningAction SilentlyContinue
        
        Write-ColorOutput "Server Status:" "Yellow"
        if ($familyHubTest.TcpTestSucceeded) {
            Write-ColorOutput "  [RUNNING] FamilyHub (8000): Active" "Green"
            Write-ColorOutput "     URL: http://127.0.0.1:8000/" "White"
        } else {
            Write-ColorOutput "  [STOPPED] FamilyHub (8000): Inactive" "Red"
        }
        
        if ($timesheetTest.TcpTestSucceeded) {
            Write-ColorOutput "  [RUNNING] Timesheet (8001): Active" "Green"
            Write-ColorOutput "     URL: http://127.0.0.1:8001/" "White"
        } else {
            Write-ColorOutput "  [STOPPED] Timesheet (8001): Inactive" "Red"
        }
    }
    catch {
        Write-ColorOutput "Could not check server status" "Yellow"
    }
    
    Write-Host ""
    Write-ColorOutput "Quick Start Commands:" "Yellow"
    Write-Host "  .\scripts\quick.ps1 familyhub    # Start FamilyHub"
    Write-Host "  .\scripts\quick.ps1 timesheet    # Start Timesheet"
}

function Show-Docker {
    Write-ColorOutput "Docker Container Status" "Cyan"
    Write-ColorOutput "========================" "Cyan"
    
    try {
        $dockerOutput = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Where-Object { $_ -match "familyhub" }
        if ($dockerOutput) {
            Write-ColorOutput $dockerOutput "White"
        } else {
            Write-ColorOutput "No FamilyHub Docker containers running" "Yellow"
        }
    }
    catch {
        Write-ColorOutput "Docker not available or not running" "Red"
    }
}

function Show-Superusers {
    Write-ColorOutput "Managing Superusers" "Cyan"
    Write-ColorOutput "===================" "Cyan"
    
    $superuserScript = Join-Path $PSScriptRoot "setup_superusers.ps1"
    if (Test-Path $superuserScript) {
        & $superuserScript status
    } else {
        Write-ColorOutput "Superuser script not found" "Red"
    }
}

function Run-Migrations {
    Write-ColorOutput "Running Migrations for All Environments" "Cyan"
    Write-ColorOutput "========================================" "Cyan"
    Write-Host ""
    
    # Get workspace root directory
    $workspaceRoot = Split-Path -Parent $PSScriptRoot
    
    # FamilyHub Migrations
    Write-ColorOutput "FamilyHub Migrations:" "Yellow"
    $familyHubPath = Join-Path $workspaceRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $familyHubPath "venv\Scripts\Activate.ps1"
        if (Test-Path $venvPath) {
            & $venvPath
        }
        
        $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings.development"
        Write-Host "  Running makemigrations..."
        python manage.py makemigrations
        Write-Host "  Running migrate..."
        python manage.py migrate
        Write-ColorOutput "  FamilyHub migrations completed" "Green"
    } else {
        Write-ColorOutput "  FamilyHub directory not found" "Red"
    }
    
    Write-Host ""
    
    # Timesheet Migrations
    Write-ColorOutput "Timesheet Migrations:" "Yellow"
    $timesheetPath = Join-Path $workspaceRoot "standalone-apps\timesheet"
    if (Test-Path $timesheetPath) {
        Set-Location $timesheetPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $timesheetPath "venv\Scripts\Activate.ps1"
        if (Test-Path $venvPath) {
            & $venvPath
        }
        
        $env:DJANGO_SETTINGS_MODULE = "timesheet_project.settings"
        Write-Host "  Running makemigrations..."
        python manage.py makemigrations
        Write-Host "  Running migrate..."
        python manage.py migrate
        Write-ColorOutput "  Timesheet migrations completed" "Green"
    } else {
        Write-ColorOutput "  Timesheet directory not found" "Red"
    }
    
    # Return to workspace root
    Set-Location $workspaceRoot
    Write-Host ""
    Write-ColorOutput "All migrations completed!" "Green"
}

# Main execution
switch ($App.ToLower()) {
    "familyhub" { Start-FamilyHub }
    "timesheet" { Start-Timesheet }
    "both" { Start-Both }
    "status" { Show-Status }
    "docker" { Show-Docker }
    "superusers" { Show-Superusers }
    "migrate" { Run-Migrations }
    "help" { Show-Help }
    default { 
        Write-ColorOutput "Unknown command: $App" "Red"
        Write-Host ""
        Show-Help 
    }
}
