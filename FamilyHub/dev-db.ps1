#!/usr/bin/env pwsh
# FamilyHub Local Development - Database Management
# Quick script for database operations

param(
    [string]$Action = ""
)

Write-Host "🗄️  FamilyHub Database Manager" -ForegroundColor Green
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
& .\venv\Scripts\Activate.ps1

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  reset    - Reset database (delete and recreate)" -ForegroundColor Cyan
    Write-Host "  backup   - Create database backup" -ForegroundColor Cyan
    Write-Host "  restore  - Restore database from backup" -ForegroundColor Cyan
    Write-Host "  shell    - Open Django database shell" -ForegroundColor Cyan
    Write-Host "  status   - Show migration status" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: ./dev-db.ps1 <command>" -ForegroundColor Yellow
}

function Reset-Database {
    Write-Host "⚠️  This will delete all data in your local database!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (yes/no)"
    
    if ($confirm -eq "yes") {
        Write-Host "🗑️  Deleting database file..." -ForegroundColor Yellow
        if (Test-Path "db.sqlite3") {
            Remove-Item "db.sqlite3"
            Write-Host "✅ Database deleted!" -ForegroundColor Green
        }
        
        Write-Host "🔄 Running migrations..." -ForegroundColor Blue
        & .\venv\Scripts\python.exe manage.py migrate --settings=FamilyHub.settings.development
        
        Write-Host "👤 Creating superuser..." -ForegroundColor Blue
        $env:DJANGO_SUPERUSER_USERNAME = "admin"
        $env:DJANGO_SUPERUSER_EMAIL = "admin@familyhub.local" 
        $env:DJANGO_SUPERUSER_PASSWORD = "admin123"
        
        & .\venv\Scripts\python.exe manage.py createsuperuser --noinput --settings=FamilyHub.settings.development
        
        Write-Host "✅ Database reset complete! Admin: admin/admin123" -ForegroundColor Green
    } else {
        Write-Host "❌ Database reset cancelled." -ForegroundColor Yellow
    }
}

function Backup-Database {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = "db_backup_$timestamp.sqlite3"
    
    if (Test-Path "db.sqlite3") {
        Copy-Item "db.sqlite3" $backupFile
        Write-Host "✅ Database backed up to: $backupFile" -ForegroundColor Green
    } else {
        Write-Host "❌ No database file found to backup." -ForegroundColor Red
    }
}

function Restore-Database {
    $backupFiles = Get-ChildItem "db_backup_*.sqlite3" | Sort-Object LastWriteTime -Descending
    
    if ($backupFiles.Count -eq 0) {
        Write-Host "❌ No backup files found." -ForegroundColor Red
        return
    }
    
    Write-Host "Available backups:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $backupFiles.Count; $i++) {
        Write-Host "  $($i + 1). $($backupFiles[$i].Name) ($(Get-Date $backupFiles[$i].LastWriteTime -Format 'yyyy-MM-dd HH:mm'))" -ForegroundColor Cyan
    }
    
    $choice = Read-Host "Select backup to restore (1-$($backupFiles.Count)) or 'cancel'"
    
    if ($choice -match '^\d+$' -and [int]$choice -ge 1 -and [int]$choice -le $backupFiles.Count) {
        $selectedBackup = $backupFiles[[int]$choice - 1]
        Copy-Item $selectedBackup.FullName "db.sqlite3"
        Write-Host "✅ Database restored from: $($selectedBackup.Name)" -ForegroundColor Green
    } else {
        Write-Host "❌ Restore cancelled." -ForegroundColor Yellow
    }
}

function Show-Status {
    Write-Host "📊 Migration Status:" -ForegroundColor Cyan
    & .\venv\Scripts\python.exe manage.py showmigrations --settings=FamilyHub.settings.development
    
    if (Test-Path "db.sqlite3") {
        $dbSize = (Get-Item "db.sqlite3").Length
        Write-Host ""
        Write-Host "💾 Database file: db.sqlite3 ($([math]::Round($dbSize/1KB, 2)) KB)" -ForegroundColor Cyan
    }
}

function Open-Shell {
    Write-Host "🐚 Opening Django database shell..." -ForegroundColor Blue
    Write-Host "Type 'exit' to quit the shell." -ForegroundColor Yellow
    & .\venv\Scripts\python.exe manage.py dbshell --settings=FamilyHub.settings.development
}

switch ($Action.ToLower()) {
    "reset" { Reset-Database }
    "backup" { Backup-Database }
    "restore" { Restore-Database }
    "shell" { Open-Shell }
    "status" { Show-Status }
    default { Show-Help }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
