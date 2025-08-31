#!/usr/bin/env pwsh
# FamilyHub Local Development - Testing Suite
# Quick script to run tests and checks

Write-Host "🧪 FamilyHub Testing Suite" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from the FamilyHub directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "❌ Error: Virtual environment not found. Run './dev-setup.ps1' first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

# Run Django system checks
Write-Host "🔍 Running Django system checks..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py check --settings=FamilyHub.settings.development

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ System checks passed!" -ForegroundColor Green
} else {
    Write-Host "❌ System checks failed!" -ForegroundColor Red
    $checksFailed = $true
}

# Check for migration issues
Write-Host "🗄️  Checking migration status..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py makemigrations --settings=FamilyHub.settings.development --check --dry-run

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ No pending migrations!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Pending migrations detected. Run './dev-migrate.ps1'" -ForegroundColor Yellow
}

# Run tests
Write-Host "🧪 Running unit tests..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py test --settings=FamilyHub.settings.development --verbosity=2

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Some tests failed!" -ForegroundColor Red
    $testsFailed = $true
}

# Check static files
Write-Host "📁 Checking static files collection..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py collectstatic --settings=FamilyHub.settings.development --dry-run --noinput

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Static files check passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Static files issues detected!" -ForegroundColor Red
    $staticFailed = $true
}

# Summary
Write-Host ""
Write-Host "📊 Test Summary:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (-not $checksFailed -and -not $testsFailed -and -not $staticFailed) {
    Write-Host "🎉 All checks passed! Your code is ready for commit." -ForegroundColor Green
} else {
    Write-Host "⚠️  Some issues found. Please fix before committing:" -ForegroundColor Yellow
    if ($checksFailed) { Write-Host "   • Fix Django system check errors" -ForegroundColor Red }
    if ($testsFailed) { Write-Host "   • Fix failing unit tests" -ForegroundColor Red }
    if ($staticFailed) { Write-Host "   • Fix static files issues" -ForegroundColor Red }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
