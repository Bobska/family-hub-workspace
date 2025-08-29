# PostgreSQL Database Backup Script for FamilyHub (Windows PowerShell)
# Author: FamilyHub Team
# Date: August 29, 2025

param(
    [switch]$Help
)

if ($Help) {
    Write-Host "FamilyHub Database Backup Script" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\backup_database.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This script creates a backup of the FamilyHub PostgreSQL database"
    Write-Host "running in a Docker container."
    exit 0
}

# Configuration
$ContainerName = "familyhub-postgres"
$DatabaseName = "familyhub"
$DatabaseUser = "django_user"
$BackupDir = ".\backups"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = "familyhub_backup_$Timestamp.sql"

Write-Host "🔄 FamilyHub Database Backup Script" -ForegroundColor Blue
Write-Host "====================================" -ForegroundColor Blue
Write-Host ""

# Create backup directory if it doesn't exist
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
    Write-Host "📁 Created backup directory: $BackupDir" -ForegroundColor Green
}

# Check if Docker container is running
$containerRunning = docker ps --filter "name=$ContainerName" --format "{{.Names}}" | Select-String $ContainerName
if (!$containerRunning) {
    Write-Host "❌ Error: PostgreSQL container '$ContainerName' is not running" -ForegroundColor Red
    Write-Host "💡 Start the container with: docker-compose up -d db" -ForegroundColor Yellow
    exit 1
}

Write-Host "📊 Creating database backup..." -ForegroundColor Yellow
Write-Host "Container: $ContainerName"
Write-Host "Database: $DatabaseName"
Write-Host "Backup file: $BackupDir\$BackupFile"
Write-Host ""

# Create database backup
try {
    $backupPath = "$BackupDir\$BackupFile"
    docker exec $ContainerName pg_dump -U $DatabaseUser -d $DatabaseName --verbose --clean --no-acl --no-owner | Out-File -FilePath $backupPath -Encoding UTF8
    
    if (Test-Path $backupPath) {
        $backupSize = [math]::Round((Get-Item $backupPath).Length / 1MB, 2)
        Write-Host ""
        Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
        Write-Host "📁 File: $backupPath" -ForegroundColor Green
        Write-Host "📏 Size: $backupSize MB" -ForegroundColor Green
        
        # List recent backups
        Write-Host ""
        Write-Host "📋 Recent backups:" -ForegroundColor Blue
        Get-ChildItem $BackupDir -Filter "familyhub_backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
            $size = [math]::Round($_.Length / 1MB, 2)
            Write-Host "  $($_.Name) ($size MB) - $($_.LastWriteTime)"
        }
        
        # Clean up old backups (keep last 10)
        Write-Host ""
        Write-Host "🧹 Cleaning up old backups (keeping last 10)..." -ForegroundColor Yellow
        $oldBackups = Get-ChildItem $BackupDir -Filter "familyhub_backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 10
        if ($oldBackups) {
            $oldBackups | Remove-Item -Force
            Write-Host "✅ Removed $($oldBackups.Count) old backup(s)" -ForegroundColor Green
        } else {
            Write-Host "✅ No old backups to remove" -ForegroundColor Green
        }
    } else {
        throw "Backup file was not created"
    }
} catch {
    Write-Host "❌ Backup failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Check Docker container status and database connectivity" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎉 Database backup process completed successfully!" -ForegroundColor Green
