# PostgreSQL Database Restore Script for FamilyHub (Windows PowerShell)
# Author: FamilyHub Team
# Date: August 29, 2025

param(
    [Parameter(Position=0)]
    [string]$BackupFile,
    [switch]$Help
)

if ($Help -or !$BackupFile) {
    Write-Host "FamilyHub Database Restore Script" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\restore_database.ps1 <backup_file>" -ForegroundColor Yellow
    Write-Host "Example: .\restore_database.ps1 familyhub_backup_20250829_143000.sql" -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path ".\backups") {
        Write-Host "📋 Available backup files:" -ForegroundColor Yellow
        Get-ChildItem ".\backups" -Filter "familyhub_backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
            $size = [math]::Round($_.Length / 1MB, 2)
            Write-Host "  $($_.Name) ($size MB) - $($_.LastWriteTime)"
        }
    }
    exit 0
}

# Configuration
$ContainerName = "familyhub-postgres"
$DatabaseName = "familyhub"
$DatabaseUser = "django_user"
$BackupDir = ".\backups"

Write-Host "🔄 FamilyHub Database Restore Script" -ForegroundColor Blue
Write-Host "====================================" -ForegroundColor Blue
Write-Host ""

# Determine full path to backup file
$FullBackupPath = $null
if (Test-Path $BackupFile) {
    $FullBackupPath = $BackupFile
} elseif (Test-Path "$BackupDir\$BackupFile") {
    $FullBackupPath = "$BackupDir\$BackupFile"
}

if (!$FullBackupPath) {
    Write-Host "❌ Error: Backup file not found" -ForegroundColor Red
    Write-Host "Checked paths:"
    Write-Host "  - $BackupFile"
    Write-Host "  - $BackupDir\$BackupFile"
    exit 1
}

# Check if Docker container is running
$containerRunning = docker ps --filter "name=$ContainerName" --format "{{.Names}}" | Select-String $ContainerName
if (!$containerRunning) {
    Write-Host "❌ Error: PostgreSQL container '$ContainerName' is not running" -ForegroundColor Red
    Write-Host "💡 Start the container with: docker-compose up -d db" -ForegroundColor Yellow
    exit 1
}

Write-Host "📊 Database restore information:" -ForegroundColor Yellow
Write-Host "Container: $ContainerName"
Write-Host "Database: $DatabaseName"
Write-Host "Backup file: $FullBackupPath"
Write-Host ""

# Warning about data loss
Write-Host "⚠️  WARNING: This will REPLACE all existing data in the database!" -ForegroundColor Red
Write-Host "📋 Current database content will be lost." -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Are you sure you want to continue? (yes/NO)"
if ($confirmation -ne "yes") {
    Write-Host "❌ Restore cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🔄 Starting database restore..." -ForegroundColor Yellow

# Restore database
try {
    # Read the backup file and pipe it to docker exec
    Get-Content $FullBackupPath | docker exec -i $ContainerName psql -U $DatabaseUser -d $DatabaseName
    
    Write-Host "✅ Database restore completed successfully!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "📊 Database status:" -ForegroundColor Blue
    docker exec $ContainerName psql -U $DatabaseUser -d $DatabaseName -c "\dt"
    
} catch {
    Write-Host "❌ Database restore failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Check the backup file format and database connectivity" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎉 Database restore process completed successfully!" -ForegroundColor Green
Write-Host "💡 You may need to restart your Django application" -ForegroundColor Yellow
