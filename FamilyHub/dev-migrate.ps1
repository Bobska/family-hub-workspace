#!/usr/bin/env pwsh
# FamilyHub Local Development - Database Migration
# Quick script to handle migrations for local development

Write-Host "🗄️  FamilyHub Database Migration Manager" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from the FamilyHub directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "❌ Error: Virtual environment not found. Please create a virtual environment first." -ForegroundColor Red
    Write-Host "   Run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

# Check for pending migrations
Write-Host "🔍 Checking for model changes..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py makemigrations --settings=FamilyHub.settings.development --check --dry-run

if ($LASTEXITCODE -ne 0) {
    Write-Host "📝 Creating new migrations..." -ForegroundColor Yellow
    & .\venv\Scripts\python.exe manage.py makemigrations --settings=FamilyHub.settings.development
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Migrations created successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create migrations." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ No model changes detected." -ForegroundColor Green
}

# Apply migrations
Write-Host "🚀 Applying migrations to SQLite database..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py migrate --settings=FamilyHub.settings.development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database migrations completed successfully!" -ForegroundColor Green
    
    # Show migration status
    Write-Host ""
    Write-Host "📊 Current migration status:" -ForegroundColor Cyan
    & .\venv\Scripts\python.exe manage.py showmigrations --settings=FamilyHub.settings.development
} else {
    Write-Host "❌ Migration failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
