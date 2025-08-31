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
    Write-Host "  Installing $package..." -ForegroundColor Cyan
    & .\venv\Scripts\python.exe -m pip install $package
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Package installation failed." -ForegroundColor Red
    exit 1
}

# Run migrations
Write-Host "🗄️  Setting up database..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py migrate --settings=FamilyHub.settings.development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database setup complete!" -ForegroundColor Green
} else {
    Write-Host "❌ Database setup failed." -ForegroundColor Red
    exit 1
}

# Create superuser if it doesn't exist
Write-Host "👤 Creating superuser..." -ForegroundColor Blue
Write-Host "   Default username: admin" -ForegroundColor Yellow
Write-Host "   Default email: admin@familyhub.local" -ForegroundColor Yellow

$env:DJANGO_SUPERUSER_USERNAME = "admin"
$env:DJANGO_SUPERUSER_EMAIL = "admin@familyhub.local" 
$env:DJANGO_SUPERUSER_PASSWORD = "admin123"

& .\venv\Scripts\python.exe manage.py createsuperuser --noinput --settings=FamilyHub.settings.development 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Superuser 'admin' created! (Password: admin123)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Superuser 'admin' already exists or creation skipped." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup complete! You can now:" -ForegroundColor Green
Write-Host "   • Run './dev-start.ps1' to start the development server" -ForegroundColor Cyan
Write-Host "   • Run './dev-migrate.ps1' to handle database migrations" -ForegroundColor Cyan
Write-Host "   • Visit http://127.0.0.1:8000/ for the main site" -ForegroundColor Cyan
Write-Host "   • Visit http://127.0.0.1:8000/admin/ for admin panel" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔑 Admin credentials: admin / admin123" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
