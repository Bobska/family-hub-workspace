# Simple status checker
Write-Host "🔍 Development Environment Status" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check services
$familyhub = Test-NetConnection -ComputerName "127.0.0.1" -Port 8000 -WarningAction SilentlyContinue
$timesheet = Test-NetConnection -ComputerName "127.0.0.1" -Port 8001 -WarningAction SilentlyContinue
$postgres = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -WarningAction SilentlyContinue

Write-Host "🚀 Django Applications:" -ForegroundColor Yellow
if ($familyhub.TcpTestSucceeded) {
    Write-Host "  ✅ FamilyHub (8000): Running" -ForegroundColor Green
} else {
    Write-Host "  ❌ FamilyHub (8000): Stopped" -ForegroundColor Red
}

if ($timesheet.TcpTestSucceeded) {
    Write-Host "  ✅ Timesheet (8001): Running" -ForegroundColor Green
} else {
    Write-Host "  ❌ Timesheet (8001): Stopped" -ForegroundColor Red
}

Write-Host ""
Write-Host "🗄️ Database:" -ForegroundColor Yellow
if ($postgres.TcpTestSucceeded) {
    Write-Host "  ✅ PostgreSQL (5432): Running" -ForegroundColor Green
} else {
    Write-Host "  ❌ PostgreSQL (5432): Stopped" -ForegroundColor Red
}

Write-Host ""
Write-Host "🛠️ Quick Commands:" -ForegroundColor Green
Write-Host "  .\scripts\quick.ps1 familyhub    # Start FamilyHub"
Write-Host "  .\scripts\quick.ps1 timesheet    # Start Timesheet"
Write-Host "  .\weekend-setup.ps1              # Complete environment setup"
