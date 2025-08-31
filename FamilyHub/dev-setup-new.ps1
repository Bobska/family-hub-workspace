#!/usr/bin/env pwsh
# FamilyHub Local Development - Setup Environment
# Quick script to set up the local development environment

Write-Host "⚡ FamilyHub Local Development Setup" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from the FamilyHub directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists, create if it doesn't
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Blue
    python -m venv venv
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment created!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "📥 Installing Python packages..." -ForegroundColor Blue
& .\venv\Scripts\python.exe -m pip install --upgrade pip

# Install core requirements
$packages = @(
    "Django==5.1.3",
    "django-environ",
    "python-decouple",
    "psycopg2-binary",
    "gunicorn", 
    "whitenoise",
    "Pillow",
    "pytz",
    "django-redis",
    "redis",
    "django-debug-toolbar"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    & .\venv\Scripts\python.exe -m pip install $package
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All packages installed successfully!" -ForegroundColor Green

# Run migrations
Write-Host "🗄️ Setting up local SQLite database..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py migrate --settings=FamilyHub.settings.development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database migrations completed!" -ForegroundColor Green
} else {
    Write-Host "❌ Database setup failed." -ForegroundColor Red
    exit 1
}

# Create superuser if needed
Write-Host "👤 Setting up admin user..." -ForegroundColor Blue
Write-Host "Create a superuser for admin access? (y/n): " -NoNewline -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "y" -or $response -eq "Y") {
    & .\venv\Scripts\python.exe manage.py createsuperuser --settings=FamilyHub.settings.development
}

Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  .\dev-start.ps1     - Start development server" -ForegroundColor White
Write-Host "  .\dev-migrate.ps1   - Run database migrations" -ForegroundColor White
Write-Host "  .\dev-test.ps1      - Run tests" -ForegroundColor White
