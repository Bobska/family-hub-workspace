# FamilyHub Superuser Setup Script
# Creates admin users for all environments

param(
    [string]$Environment = "all",
    [string]$Username = "admin",
    [string]$Password = "admin",
    [string]$Email = "admin@familyhub.local"
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

function Create-FamilyHubSuperuser {
    Write-ColorOutput "Creating FamilyHub Superuser..." "Yellow"
    
    try {
        $familyHubPath = Join-Path $PSScriptRoot "..\FamilyHub"
        if (Test-Path $familyHubPath) {
            Set-Location $familyHubPath
            
            # Activate virtual environment
            if (Test-Path "venv\Scripts\activate.ps1") {
                & "venv\Scripts\activate.ps1"
            }
            
            # Set environment for development
            $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings.development"
            
            # Check if superuser already exists
            $checkResult = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())" 2>$null
            
            if ($checkResult -match "(\d+)") {
                $count = [int]$Matches[1]
                if ($count -gt 0) {
                    Write-ColorOutput "✅ FamilyHub already has $count superuser(s)" "Green"
                    return
                }
            }
            
            # Create superuser
            $createCommand = @"
from django.contrib.auth.models import User
if not User.objects.filter(username='$Username').exists():
    User.objects.create_superuser('$Username', '$Email', '$Password')
    print('✅ Superuser created successfully')
else:
    print('✅ Superuser already exists')
"@
            
            python manage.py shell -c $createCommand
            Write-ColorOutput "✅ FamilyHub superuser setup complete" "Green"
        }
        else {
            Write-ColorOutput "❌ FamilyHub directory not found" "Red"
        }
    }
    catch {
        Write-ColorOutput "❌ Error setting up FamilyHub superuser: $_" "Red"
    }
}

function Create-TimesheetSuperuser {
    Write-ColorOutput "Creating Standalone Timesheet Superuser..." "Yellow"
    
    try {
        $timesheetPath = Join-Path $PSScriptRoot "..\standalone-apps\timesheet"
        if (Test-Path $timesheetPath) {
            Set-Location $timesheetPath
            
            # Activate virtual environment
            if (Test-Path "venv\Scripts\activate.ps1") {
                & "venv\Scripts\activate.ps1"
            }
            
            # Set environment for standalone
            $env:DJANGO_SETTINGS_MODULE = "timesheet_project.settings"
            
            # Check if superuser already exists
            $checkResult = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())" 2>$null
            
            if ($checkResult -match "(\d+)") {
                $count = [int]$Matches[1]
                if ($count -gt 0) {
                    Write-ColorOutput "✅ Standalone Timesheet already has $count superuser(s)" "Green"
                    return
                }
            }
            
            # Create superuser
            $createCommand = @"
from django.contrib.auth.models import User
if not User.objects.filter(username='$Username').exists():
    User.objects.create_superuser('$Username', '$Email', '$Password')
    print('✅ Superuser created successfully')
else:
    print('✅ Superuser already exists')
"@
            
            python manage.py shell -c $createCommand
            Write-ColorOutput "✅ Standalone Timesheet superuser setup complete" "Green"
        }
        else {
            Write-ColorOutput "❌ Standalone Timesheet directory not found" "Red"
        }
    }
    catch {
        Write-ColorOutput "❌ Error setting up Standalone Timesheet superuser: $_" "Red"
    }
}

function Create-DockerSuperuser {
    Write-ColorOutput "Creating Docker PostgreSQL Superuser..." "Yellow"
    
    try {
        # Check if PostgreSQL container is running
        $containerStatus = docker ps --filter "name=familyhub-postgres" --format "{{.Status}}"
        
        if (-not $containerStatus) {
            Write-ColorOutput "❌ PostgreSQL container not running. Start with: .\dev.ps1 docker" "Red"
            return
        }
        
        $familyHubPath = Join-Path $PSScriptRoot "..\FamilyHub"
        if (Test-Path $familyHubPath) {
            Set-Location $familyHubPath
            
            # Activate virtual environment and install Docker requirements
            if (Test-Path "venv\Scripts\activate.ps1") {
                & "venv\Scripts\activate.ps1"
            }
            
            # Install required packages for Docker settings
            pip install dj-database-url psycopg2-binary python-dotenv | Out-Null
            
            # Set environment for Docker
            $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings_docker"
            
            # Run migrations first to ensure tables exist
            python manage.py migrate --run-syncdb
            
            # Create superuser
            $createCommand = @"
from django.contrib.auth.models import User
if not User.objects.filter(username='$Username').exists():
    User.objects.create_superuser('$Username', '$Email', '$Password')
    print('✅ Docker superuser created successfully')
else:
    print('✅ Docker superuser already exists')
"@
            
            python manage.py shell -c $createCommand
            Write-ColorOutput "✅ Docker PostgreSQL superuser setup complete" "Green"
        }
        else {
            Write-ColorOutput "❌ FamilyHub directory not found" "Red"
        }
    }
    catch {
        Write-ColorOutput "❌ Error setting up Docker superuser: $_" "Red"
    }
}

function Show-SuperuserStatus {
    Write-ColorOutput "Superuser Status Report" "Cyan"
    Write-ColorOutput "======================" "Cyan"
    
    # Check FamilyHub
    try {
        Set-Location (Join-Path $PSScriptRoot "..\FamilyHub")
        $env:DJANGO_SETTINGS_MODULE = "FamilyHub.settings.development"
        $result = python manage.py shell -c "from django.contrib.auth.models import User; users = User.objects.filter(is_superuser=True); print(f'FamilyHub: {users.count()} superuser(s)'); [print(f'  - {u.username} ({u.email})') for u in users]" 2>$null
        Write-ColorOutput $result "Green"
    }
    catch {
        Write-ColorOutput "FamilyHub: Error checking superusers" "Red"
    }
    
    # Check Standalone Timesheet
    try {
        Set-Location (Join-Path $PSScriptRoot "..\standalone-apps\timesheet")
        $env:DJANGO_SETTINGS_MODULE = "timesheet_project.settings"
        $result = python manage.py shell -c "from django.contrib.auth.models import User; users = User.objects.filter(is_superuser=True); print(f'Standalone: {users.count()} superuser(s)'); [print(f'  - {u.username} ({u.email})') for u in users]" 2>$null
        Write-ColorOutput $result "Green"
    }
    catch {
        Write-ColorOutput "Standalone: Error checking superusers" "Red"
    }
    
    Write-ColorOutput "" 
    Write-ColorOutput "Default Credentials:" "Yellow"
    Write-ColorOutput "Username: $Username" "White"
    Write-ColorOutput "Password: $Password" "White"
    Write-ColorOutput "Email: $Email" "White"
}

# Main execution
Write-ColorOutput "FamilyHub Superuser Setup" "Cyan"
Write-ColorOutput "========================" "Cyan"

switch ($Environment.ToLower()) {
    "familyhub" { Create-FamilyHubSuperuser }
    "timesheet" { Create-TimesheetSuperuser }
    "docker" { Create-DockerSuperuser }
    "status" { Show-SuperuserStatus }
    "all" {
        Create-FamilyHubSuperuser
        Create-TimesheetSuperuser
        Write-ColorOutput ""
        Write-ColorOutput "Note: Docker environment requires containers to be running." "Yellow"
        Write-ColorOutput "Run '.\dev.ps1 docker' first, then '.\scripts\setup_superusers.ps1 docker'" "Yellow"
        Write-ColorOutput ""
        Show-SuperuserStatus
    }
    default {
        Write-ColorOutput "Usage: .\setup_superusers.ps1 [all|familyhub|timesheet|docker|status]" "Yellow"
        Write-ColorOutput ""
        Write-ColorOutput "Examples:" "White"
        Write-ColorOutput "  .\setup_superusers.ps1                    # Setup all environments" "White"
        Write-ColorOutput "  .\setup_superusers.ps1 status             # Show current status" "White"
        Write-ColorOutput "  .\setup_superusers.ps1 familyhub          # Setup FamilyHub only" "White"
        Write-ColorOutput "  .\setup_superusers.ps1 docker             # Setup Docker only" "White"
    }
}

# Return to original directory
Set-Location $PSScriptRoot
