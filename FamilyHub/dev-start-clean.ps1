#!/usr/bin/env pwsh
# FamilyHub Local Development - Start Server
# Quick script to start the Django development server locally

Write-Host "Starting FamilyHub Local Development Server..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: manage.py not found. Please run this script from the FamilyHub directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Error: Virtual environment not found. Please create a virtual environment first." -ForegroundColor Red
    Write-Host "   Run: .\dev-setup-new.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment and run server
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

Write-Host "Running system checks..." -ForegroundColor Blue
& .\venv\Scripts\python.exe manage.py check --settings=FamilyHub.settings.development

if ($LASTEXITCODE -eq 0) {
    Write-Host "System checks passed!" -ForegroundColor Green
    Write-Host "Starting development server at http://127.0.0.1:8000/" -ForegroundColor Green
    Write-Host "Database: SQLite (local)" -ForegroundColor Cyan
    Write-Host "Debug Mode: ON" -ForegroundColor Cyan
    Write-Host "Auto-reload: ON" -ForegroundColor Cyan
    Write-Host "Debug Widget: Available (top-right corner)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host "===============================================" -ForegroundColor Cyan
    
    # Start the server
    & .\venv\Scripts\python.exe manage.py runserver --settings=FamilyHub.settings.development
} else {
    Write-Host "System checks failed. Please fix the errors before starting the server." -ForegroundColor Red
}
