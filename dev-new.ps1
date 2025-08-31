# FamilyHub Development Workflow - PowerShell Script
param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

function Show-Help {
    Write-ColorOutput "FamilyHub Development Workflow Commands" "Cyan"
    Write-ColorOutput "=======================================" "Cyan"
    Write-Host ""
    Write-ColorOutput "Available Commands:" "Yellow"
    Write-Host "  help       - Show this help message"
    Write-Host "  setup      - Setup local development environment"
    Write-Host "  start      - Start local development server (SQLite)"
    Write-Host "  docker     - Start Docker PostgreSQL setup"
    Write-Host "  status     - Show container status"
    Write-Host "  migrate    - Run Django migrations"
    Write-Host "  test       - Run tests"
    Write-Host "  shell      - Open Django shell"
    Write-Host ""
    Write-ColorOutput "Docker Commands:" "Yellow"
    Write-Host "  build      - Build Docker containers"
    Write-Host "  up         - Start Docker services"
    Write-Host "  down       - Stop Docker services"
    Write-Host "  restart    - Restart Docker services"
    Write-Host "  logs       - Show container logs"
    Write-Host ""
    Write-ColorOutput "Usage: .\dev.ps1 <command>" "Green"
    Write-Host ""
    Write-ColorOutput "Examples:" "Green"
    Write-Host "  .\dev.ps1 setup     # First-time setup"
    Write-Host "  .\dev.ps1 start     # Start local server"
    Write-Host "  .\dev.ps1 docker    # Start with Docker"
    Write-Host ""
}

function Start-Setup {
    Write-ColorOutput "Setting up FamilyHub development environment..." "Green"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        & .\dev-setup-new.ps1
        Set-Location $PSScriptRoot
    } else {
        Write-ColorOutput "Error: FamilyHub directory not found!" "Red"
        exit 1
    }
}

function Start-Local {
    Write-ColorOutput "Starting local development server..." "Green"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        & .\dev-start.ps1
        Set-Location $PSScriptRoot
    } else {
        Write-ColorOutput "Error: FamilyHub directory not found!" "Red"
        exit 1
    }
}

function Start-Docker {
    Write-ColorOutput "Starting Docker development environment..." "Green"
    
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        docker-compose up -d
        Write-ColorOutput "Docker services started. Access at http://localhost:8000" "Green"
    } else {
        Write-ColorOutput "Error: docker-compose not found!" "Red"
        exit 1
    }
}

function Show-Status {
    Write-ColorOutput "Checking development environment status..." "Blue"
    
    # Check local development
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path "$familyHubPath\venv") {
        Write-ColorOutput "✅ Local virtual environment: Ready" "Green"
    } else {
        Write-ColorOutput "❌ Local virtual environment: Not setup" "Red"
    }
    
    # Check Docker
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        $containers = docker-compose ps -q 2>$null
        if ($containers) {
            Write-ColorOutput "✅ Docker containers: Running" "Green"
        } else {
            Write-ColorOutput "⚪ Docker containers: Stopped" "Yellow"
        }
    } else {
        Write-ColorOutput "❌ Docker: Not available" "Red"
    }
}

function Run-Migrations {
    Write-ColorOutput "Running database migrations..." "Blue"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        & .\dev-migrate.ps1
        Set-Location $PSScriptRoot
    } else {
        Write-ColorOutput "Error: FamilyHub directory not found!" "Red"
        exit 1
    }
}

function Run-Tests {
    Write-ColorOutput "Running tests..." "Blue"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        & .\dev-test.ps1
        Set-Location $PSScriptRoot
    } else {
        Write-ColorOutput "Error: FamilyHub directory not found!" "Red"
        exit 1
    }
}

# Main script execution
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "setup" { Start-Setup }
    "start" { Start-Local }
    "docker" { Start-Docker }
    "status" { Show-Status }
    "migrate" { Run-Migrations }
    "test" { Run-Tests }
    "build" { docker-compose build }
    "up" { docker-compose up -d }
    "down" { docker-compose down }
    "restart" { docker-compose restart }
    "logs" { docker-compose logs -f }
    "shell" { 
        Set-Location "FamilyHub"
        & .\venv\Scripts\python.exe manage.py shell --settings=FamilyHub.settings.development
        Set-Location $PSScriptRoot
    }
    default {
        Write-ColorOutput "Unknown command: $Command" "Red"
        Write-ColorOutput "Run '.\dev.ps1 help' for available commands" "Yellow"
        exit 1
    }
}
