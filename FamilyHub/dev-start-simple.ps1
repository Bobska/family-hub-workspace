# FamilyHub Local Development Server Start Script
Write-Host "Starting FamilyHub Development Server..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: Not in FamilyHub directory" -ForegroundColor Red
    exit 1
}

# Run Django server
python manage.py runserver
