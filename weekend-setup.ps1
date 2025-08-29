#!/usr/bin/env pwsh
# FamilyHub Weekend Setup - Complete Development Environment
# Comprehensive setup for all development modes

param(
    [string]$Mode = "hybrid",  # Options: native, hybrid, docker
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "FamilyHub Weekend Setup - Complete Development Environment" -ForegroundColor Cyan
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\weekend-setup.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Modes:"
    Write-Host "  native   - SQLite database, fastest startup"
    Write-Host "  hybrid   - PostgreSQL + native Django (recommended)"
    Write-Host "  docker   - Full containerized environment"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\weekend-setup.ps1                    # Start hybrid mode"
    Write-Host "  .\weekend-setup.ps1 -Mode docker       # Start full Docker"
    Write-Host "  .\weekend-setup.ps1 -Mode native       # Start native mode"
    exit 0
}

Write-Host "🏠 FamilyHub Weekend Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host "Mode: $Mode" -ForegroundColor Yellow
Write-Host ""

# Add make to PATH if available
$makePath = "$env:USERPROFILE\AppData\Local\Microsoft\WinGet\Packages\ezwinports.make_Microsoft.Winget.Source_8wekyb3d8bbwe\bin"
if (Test-Path $makePath) {
    $env:PATH += ";$makePath"
    Write-Host "✅ GNU Make available" -ForegroundColor Green
}

switch ($Mode) {
    "native" {
        Write-Host "🚀 Starting Native Development Mode..." -ForegroundColor Yellow
        Write-Host "  Database: SQLite"
        Write-Host "  Speed: ⚡⚡⚡ Fastest"
        Write-Host ""
        
        # Start FamilyHub only
        Write-Host "Starting FamilyHub (port 8000)..."
        Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '.\scripts\start_familyhub.ps1'"
        
        Write-Host "✅ Native mode started!"
        Write-Host "🌐 FamilyHub: http://localhost:8000"
    }
    
    "hybrid" {
        Write-Host "🔄 Starting Hybrid Development Mode..." -ForegroundColor Yellow
        Write-Host "  Database: PostgreSQL (Docker)"
        Write-Host "  Django: Native Python"
        Write-Host "  Speed: ⚡⚡ Balanced"
        Write-Host ""
        
        # Start PostgreSQL + pgAdmin via Docker
        Write-Host "Starting PostgreSQL + pgAdmin..."
        if (Get-Command make -ErrorAction SilentlyContinue) {
            make quick
        } else {
            docker-compose -f docker-compose.quick.yml up -d
        }
        
        Start-Sleep 5
        
        # Start both FamilyHub and Timesheet
        Write-Host "Starting FamilyHub (port 8000)..."
        Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '.\scripts\start_familyhub.ps1'"
        
        Start-Sleep 2
        
        Write-Host "Starting Timesheet (port 8001)..."
        Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '.\scripts\start_timesheet.ps1'"
        
        Write-Host "✅ Hybrid mode started!"
        Write-Host "🌐 FamilyHub: http://localhost:8000"
        Write-Host "🌐 Timesheet: http://localhost:8001"
        Write-Host "🌐 pgAdmin: http://localhost:5050"
    }
    
    "docker" {
        Write-Host "🐳 Starting Full Docker Development Mode..." -ForegroundColor Yellow
        Write-Host "  Database: PostgreSQL (Docker)"
        Write-Host "  Django: Docker Container"
        Write-Host "  Speed: ⚡ Production-like"
        Write-Host ""
        
        # Start full Docker environment
        Write-Host "Starting full Docker environment..."
        if (Get-Command make -ErrorAction SilentlyContinue) {
            make dev
        } else {
            docker-compose -f docker-compose.dev.yml up -d
        }
        
        Start-Sleep 10
        
        # Start standalone timesheet
        Write-Host "Starting Timesheet (port 8001)..."
        Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "& '.\scripts\start_timesheet.ps1'"
        
        Write-Host "✅ Docker mode started!"
        Write-Host "🌐 FamilyHub: http://localhost:8000 (Docker)"
        Write-Host "🌐 Timesheet: http://localhost:8001 (Native)"
        Write-Host "🌐 pgAdmin: http://localhost:5050"
    }
    
    default {
        Write-Host "❌ Unknown mode: $Mode" -ForegroundColor Red
        Write-Host "Available modes: native, hybrid, docker"
        exit 1
    }
}

Write-Host ""
Write-Host "🎯 Weekend Setup Complete!" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""
Write-Host "Quick Commands:"
Write-Host "  .\scripts\quick.ps1 status              # Check all servers"
Write-Host "  .\scripts\quick.ps1 familyhub           # Start/restart FamilyHub"
Write-Host "  .\scripts\quick.ps1 timesheet           # Start/restart Timesheet"
if (Get-Command make -ErrorAction SilentlyContinue) {
    Write-Host "  make status                             # Docker status"
    Write-Host "  make health                             # Health check"
    Write-Host "  make backup                             # Database backup"
}
Write-Host ""
Write-Host "🚀 Happy coding! Your FamilyHub development environment is ready."
