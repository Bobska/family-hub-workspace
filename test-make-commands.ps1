# Test Make Commands for FamilyHub
# Since the Makefile has emoji encoding issues, this script demonstrates what each command does

param(
    [string]$Command = "help"
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Magenta" { Write-Host $Message -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

function Test-Status {
    Write-ColorOutput "Testing 'make status' equivalent..." "Cyan"
    Write-Host ""
    Write-ColorOutput "Service Status:" "Yellow"
    Write-ColorOutput "===============" "Yellow"
    
    try {
        $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=familyhub"
        if ($containers) {
            Write-Host $containers
        } else {
            Write-ColorOutput "No FamilyHub containers running" "Yellow"
        }
    }
    catch {
        Write-ColorOutput "Error checking Docker status: $_" "Red"
    }
}

function Test-Quick {
    Write-ColorOutput "Testing 'make quick' equivalent..." "Cyan"
    Write-Host ""
    
    if (Test-Path "FamilyHub/docker-compose.quick.yml") {
        Write-ColorOutput "Found docker-compose.quick.yml - would run:" "Green"
        Write-Host "docker-compose -f FamilyHub/docker-compose.quick.yml up -d"
    } else {
        Write-ColorOutput "docker-compose.quick.yml not found" "Red"
    }
}

function Test-Dev {
    Write-ColorOutput "Testing 'make dev' equivalent..." "Cyan"
    Write-Host ""
    
    if (Test-Path "FamilyHub/docker-compose.dev.yml") {
        Write-ColorOutput "Found docker-compose.dev.yml - would run:" "Green"
        Write-Host "docker-compose -f FamilyHub/docker-compose.dev.yml up -d"
    } else {
        Write-ColorOutput "docker-compose.dev.yml not found" "Red"
    }
}

function Test-Prod {
    Write-ColorOutput "Testing 'make prod' equivalent..." "Cyan"
    Write-Host ""
    
    if (Test-Path "FamilyHub/docker-compose.production.yml") {
        Write-ColorOutput "Found docker-compose.production.yml - would run:" "Green"
        Write-Host "docker-compose -f FamilyHub/docker-compose.production.yml up -d"
    } else {
        Write-ColorOutput "docker-compose.production.yml not found" "Red"
    }
}

function Test-Logs {
    Write-ColorOutput "Testing 'make logs' equivalent..." "Cyan"
    Write-Host ""
    
    try {
        Write-ColorOutput "Getting recent logs from FamilyHub containers:" "Green"
        docker logs familyhub-web --tail 10 2>&1 | Select-Object -First 10
    }
    catch {
        Write-ColorOutput "Error getting logs: $_" "Red"
    }
}

function Test-Health {
    Write-ColorOutput "Testing 'make health' equivalent..." "Cyan"
    Write-Host ""
    
    Write-ColorOutput "Application Health Check:" "Yellow"
    Write-ColorOutput "========================" "Yellow"
    
    # Check PostgreSQL
    try {
        $pgTest = docker exec familyhub-postgres pg_isready -U django -d familyhub 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "PostgreSQL: Healthy" "Green"
        } else {
            Write-ColorOutput "PostgreSQL: Unhealthy" "Red"
        }
    }
    catch {
        Write-ColorOutput "PostgreSQL: Not accessible" "Yellow"
    }
    
    # Check Web Services
    $ports = @(5050, 8000, 8080)
    foreach ($port in $ports) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$port" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            Write-ColorOutput "Port $port`: Healthy" "Green"
        }
        catch {
            Write-ColorOutput "Port $port`: Not accessible" "Yellow"
        }
    }
}

function Test-Stop {
    Write-ColorOutput "Testing 'make stop' equivalent..." "Cyan"
    Write-Host ""
    Write-ColorOutput "Would run the following commands:" "Yellow"
    Write-Host "docker-compose -f FamilyHub/docker-compose.dev.yml down"
    Write-Host "docker-compose -f FamilyHub/docker-compose.production.yml down"
    Write-Host "docker-compose -f FamilyHub/docker-compose.quick.yml down"
    Write-Host "docker-compose down"
}

function Test-Build {
    Write-ColorOutput "Testing 'make build' equivalent..." "Cyan"
    Write-Host ""
    Write-ColorOutput "Would rebuild all containers with:" "Yellow"
    Write-Host "docker-compose build --no-cache"
}

function Test-Migrate {
    Write-ColorOutput "Testing 'make migrate' equivalent..." "Cyan"
    Write-Host ""
    
    $runningContainers = docker ps --format "{{.Names}}" | Where-Object { $_ -match "familyhub.*django|familyhub.*web" }
    if ($runningContainers) {
        Write-ColorOutput "Found Django container, would run:" "Green"
        Write-Host "docker exec $($runningContainers[0]) python manage.py makemigrations"
        Write-Host "docker exec $($runningContainers[0]) python manage.py migrate"
    } else {
        Write-ColorOutput "No Django container running, would run locally:" "Yellow"
        Write-Host "cd FamilyHub && python manage.py makemigrations && python manage.py migrate"
    }
}

function Show-Help {
    Write-ColorOutput "FamilyHub Make Commands Test Script" "Cyan"
    Write-ColorOutput "====================================" "Cyan"
    Write-Host ""
    Write-ColorOutput "Available Commands:" "Yellow"
    Write-Host "  status     - Check service status"
    Write-Host "  quick      - Test quick setup"
    Write-Host "  dev        - Test development environment"
    Write-Host "  prod       - Test production environment"
    Write-Host "  logs       - View recent logs"
    Write-Host "  health     - Check application health"
    Write-Host "  stop       - Show stop commands"
    Write-Host "  build      - Show build commands"
    Write-Host "  migrate    - Test migration commands"
    Write-Host "  all        - Run all tests"
    Write-Host ""
    Write-ColorOutput "Usage:" "Green"
    Write-Host "  .\test-make-commands.ps1 status"
    Write-Host "  .\test-make-commands.ps1 health"
    Write-Host "  .\test-make-commands.ps1 all"
}

function Test-All {
    Write-ColorOutput "Running All Make Command Tests..." "Cyan"
    Write-ColorOutput "=================================" "Cyan"
    Write-Host ""
    
    Test-Status
    Write-Host ""
    Test-Health
    Write-Host ""
    Test-Quick
    Write-Host ""
    Test-Dev
    Write-Host ""
    Test-Prod
    Write-Host ""
    Test-Logs
    Write-Host ""
    Test-Migrate
    Write-Host ""
    Test-Build
    Write-Host ""
    Test-Stop
}

# Main execution
switch ($Command.ToLower()) {
    "status" { Test-Status }
    "quick" { Test-Quick }
    "dev" { Test-Dev }
    "prod" { Test-Prod }
    "logs" { Test-Logs }
    "health" { Test-Health }
    "stop" { Test-Stop }
    "build" { Test-Build }
    "migrate" { Test-Migrate }
    "all" { Test-All }
    "help" { Show-Help }
    default { 
        Write-ColorOutput "Unknown command: $Command" "Red"
        Write-Host ""
        Show-Help 
    }
}
