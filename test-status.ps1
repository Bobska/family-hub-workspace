# Temporary status function to test syntax
function Show-Status {
    Write-Host "🔍 Development Environment Status" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check if servers are running by testing ports
    try {
        $familyHubTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 8000 -WarningAction SilentlyContinue
        $timesheetTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 8001 -WarningAction SilentlyContinue
        $postgresTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -WarningAction SilentlyContinue
        $redisTest = Test-NetConnection -ComputerName "127.0.0.1" -Port 6379 -WarningAction SilentlyContinue
        
        Write-Host "🚀 Django Applications:" -ForegroundColor Yellow
        if ($familyHubTest.TcpTestSucceeded) {
            Write-Host "  ✅ FamilyHub (8000): Running" -ForegroundColor Green
            Write-Host "     📍 http://127.0.0.1:8000/" -ForegroundColor White
        } else {
            Write-Host "  ❌ FamilyHub (8000): Stopped" -ForegroundColor Red
        }
        
        if ($timesheetTest.TcpTestSucceeded) {
            Write-Host "  ✅ Timesheet (8001): Running" -ForegroundColor Green
            Write-Host "     📍 http://127.0.0.1:8001/" -ForegroundColor White
        } else {
            Write-Host "  ❌ Timesheet (8001): Stopped" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "🗄️ Database Services:" -ForegroundColor Yellow
        if ($postgresTest.TcpTestSucceeded) {
            Write-Host "  ✅ PostgreSQL (5432): Running" -ForegroundColor Green
        } else {
            Write-Host "  ❌ PostgreSQL (5432): Stopped" -ForegroundColor Red
        }
        
        if ($redisTest.TcpTestSucceeded) {
            Write-Host "  ✅ Redis (6379): Running" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Redis (6379): Stopped" -ForegroundColor Red
        }
        
        # Check pgAdmin
        Write-Host ""
        Write-Host "🌐 Web Interfaces:" -ForegroundColor Yellow
        try {
            $pgAdminResponse = Invoke-WebRequest -Uri "http://localhost:5050" -TimeoutSec 3 -UseBasicParsing
            Write-Host "  ✅ pgAdmin (5050): Running" -ForegroundColor Green
            Write-Host "     📍 http://localhost:5050/" -ForegroundColor White
        }
        catch {
            Write-Host "  ❌ pgAdmin (5050): Not accessible" -ForegroundColor Red
        }
        
    }
    catch {
        Write-Host "Could not check server status" -ForegroundColor Yellow
    }
    
    # Docker status
    Write-Host ""
    Write-Host "🐳 Docker Status:" -ForegroundColor Yellow
    try {
        $dockerContainers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null | Where-Object { $_ -match "familyhub|postgres|redis|pgadmin" }
        if ($dockerContainers) {
            $dockerContainers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
        } else {
            Write-Host "  ℹ️ No FamilyHub containers running" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ❌ Docker not available" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "🛠️ Quick Commands:" -ForegroundColor Green
    Write-Host "  .\scripts\quick.ps1 familyhub    # Start FamilyHub"
    Write-Host "  .\scripts\quick.ps1 timesheet    # Start Timesheet"
    Write-Host "  .\weekend-setup.ps1              # Complete environment setup"
    if (Get-Command make -ErrorAction SilentlyContinue) {
        Write-Host "  make dev                         # Start Docker environment"
        Write-Host "  make quick                       # Start PostgreSQL only"
    }
}

# Test the function
Show-Status
