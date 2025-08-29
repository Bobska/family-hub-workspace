# FamilyHub Development Workflow - PowerShell Script
# Simple version without Unicode characters
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
    Write-Host "  quick      - Start quick development setup (SQLite)"
    Write-Host "  docker     - Start Docker PostgreSQL setup"
    Write-Host "  status     - Show container status"
    Write-Host "  health     - Run health checks"
    Write-Host "  migrate    - Run Django migrations"
    Write-Host "  shell      - Open Django shell"
    Write-Host "  test       - Run tests"
    Write-Host "  backup     - Backup PostgreSQL database"
    Write-Host "  restore    - Restore PostgreSQL database"
    Write-Host ""
    Write-ColorOutput "Usage: PowerShell -File dev.ps1 <command>" "Green"
    Write-Host ""
}

function Start-Quick {
    Write-ColorOutput "Starting Quick SQLite Development Setup..." "Green"
    
    # Navigate to FamilyHub directory
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        Write-ColorOutput "Navigated to FamilyHub directory" "Green"
    } else {
        Write-ColorOutput "FamilyHub directory not found" "Red"
        return
    }
    
    # Use default settings (SQLite)
    $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings"
    
    # Run Django checks
    Write-ColorOutput "Running Django health checks..." "Yellow"
    python manage.py check
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "Django health checks passed" "Green"
        
        # Run migrations
        Write-ColorOutput "Running migrations..." "Yellow"
        python manage.py migrate
        
        # Start Django development server
        Write-ColorOutput "Starting Django development server..." "Green"
        Write-ColorOutput "Server will be available at: http://localhost:8000" "Cyan"
        Write-ColorOutput "Database: SQLite" "Cyan"
        python manage.py runserver
    } else {
        Write-ColorOutput "Django health checks failed" "Red"
    }
}

function Backup-Database {
    Write-ColorOutput "Starting Database Backup..." "Green"
    
    $scriptPath = Join-Path $PSScriptRoot "scripts\backup_database.ps1"
    if (Test-Path $scriptPath) {
        & $scriptPath
    } else {
        Write-ColorOutput "Backup script not found at: $scriptPath" "Red"
    }
}

function Restore-Database {
    Write-ColorOutput "Starting Database Restore..." "Green"
    
    $scriptPath = Join-Path $PSScriptRoot "scripts\restore_database.ps1"
    if (Test-Path $scriptPath) {
        & $scriptPath -Help
    } else {
        Write-ColorOutput "Restore script not found at: $scriptPath" "Red"
    }
}

function Start-Docker {
    Write-ColorOutput "Starting Docker PostgreSQL Setup..." "Green"
    
    # Check if Docker is running
    try {
        docker version | Out-Null
        Write-ColorOutput "Docker is running" "Green"
    }
    catch {
        Write-ColorOutput "Docker is not running. Please start Docker Desktop." "Red"
        return
    }
    
    # Start Docker services
    Write-ColorOutput "Starting Docker services..." "Yellow"
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "Docker services started successfully" "Green"
        
        # Wait for database to be ready
        Write-ColorOutput "Waiting for PostgreSQL to be ready..." "Yellow"
        Start-Sleep -Seconds 10
        
        # Install dependencies
        Write-ColorOutput "Installing Python dependencies..." "Yellow"
        pip install -r requirements/base.txt
        
        # Navigate to FamilyHub directory
        $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
        Set-Location $familyHubPath
        
        # Set environment for Docker
        $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings_docker"
        
        # Run migrations
        Write-ColorOutput "Running migrations..." "Yellow"
        python manage.py migrate
        
        # Start Django development server
        Write-ColorOutput "Starting Django development server..." "Green"
        Write-ColorOutput "Server will be available at: http://localhost:8000" "Cyan"
        Write-ColorOutput "Database: PostgreSQL in Docker" "Cyan"
        python manage.py runserver
    } else {
        Write-ColorOutput "Failed to start Docker services" "Red"
    }
}

function Show-Status {
    Write-ColorOutput "Container Status" "Cyan"
    Write-ColorOutput "================" "Cyan"
    
    try {
        docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    }
    catch {
        Write-ColorOutput "Error checking Docker status" "Red"
    }
}

function Check-Health {
    Write-ColorOutput "Running Health Checks..." "Green"
    
    # Check Docker
    try {
        docker version | Out-Null
        Write-ColorOutput "Docker: Running" "Green"
    }
    catch {
        Write-ColorOutput "Docker: Not running" "Red"
    }
    
    # Check Django
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $familyHubPath "venv"
        if (Test-Path $venvPath) {
            & "$venvPath\Scripts\Activate.ps1"
        }
        
        Write-ColorOutput "Checking Django configuration..." "Yellow"
        $result = python manage.py check 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Django: Configuration OK" "Green"
        } else {
            Write-ColorOutput "Django: Configuration errors found" "Red"
            Write-Host $result
        }
    } else {
        Write-ColorOutput "FamilyHub directory not found" "Red"
    }
}

function Run-Migrate {
    Write-ColorOutput "Running Django Migrations..." "Green"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $familyHubPath "venv"
        if (Test-Path $venvPath) {
            & "$venvPath\Scripts\Activate.ps1"
        }
        
        python manage.py makemigrations
        python manage.py migrate
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Migrations completed successfully" "Green"
        } else {
            Write-ColorOutput "Migration errors occurred" "Red"
        }
    } else {
        Write-ColorOutput "FamilyHub directory not found" "Red"
    }
}

function Open-Shell {
    Write-ColorOutput "Opening Django Shell..." "Green"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $familyHubPath "venv"
        if (Test-Path $venvPath) {
            & "$venvPath\Scripts\Activate.ps1"
        }
        
        python manage.py shell
    } else {
        Write-ColorOutput "FamilyHub directory not found" "Red"
    }
}

function Run-Tests {
    Write-ColorOutput "Running Tests..." "Green"
    
    $familyHubPath = Join-Path $PSScriptRoot "FamilyHub"
    if (Test-Path $familyHubPath) {
        Set-Location $familyHubPath
        
        # Activate virtual environment if exists
        $venvPath = Join-Path $familyHubPath "venv"
        if (Test-Path $venvPath) {
            & "$venvPath\Scripts\Activate.ps1"
        }
        
        python manage.py test
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "All tests passed" "Green"
        } else {
            Write-ColorOutput "Some tests failed" "Red"
        }
    } else {
        Write-ColorOutput "FamilyHub directory not found" "Red"
    }
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "quick" { Start-Quick }
    "docker" { Start-Docker }
    "status" { Show-Status }
    "health" { Check-Health }
    "migrate" { Run-Migrate }
    "shell" { Open-Shell }
    "test" { Run-Tests }
    "backup" { Backup-Database }
    "restore" { Restore-Database }
    default {
        Write-ColorOutput "Unknown command: $Command" "Red"
        Write-ColorOutput "Run 'PowerShell -File dev.ps1 help' for available commands" "Yellow"
    }
}
