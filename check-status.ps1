# Weekend Setup Complete - Environment Status
Write-Host "Development Environment Status" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check services
$familyhub = Test-NetConnection -ComputerName "127.0.0.1" -Port 8000 -WarningAction SilentlyContinue
$timesheet = Test-NetConnection -ComputerName "127.0.0.1" -Port 8001 -WarningAction SilentlyContinue
$postgres = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -WarningAction SilentlyContinue
$redis = Test-NetConnection -ComputerName "127.0.0.1" -Port 6379 -WarningAction SilentlyContinue

Write-Host "Django Applications:" -ForegroundColor Yellow
if ($familyhub.TcpTestSucceeded) {
    Write-Host "  [RUNNING] FamilyHub (8000): http://127.0.0.1:8000" -ForegroundColor Green
} else {
    Write-Host "  [STOPPED] FamilyHub (8000): Not running" -ForegroundColor Red
}

if ($timesheet.TcpTestSucceeded) {
    Write-Host "  [RUNNING] Timesheet (8001): http://127.0.0.1:8001" -ForegroundColor Green
} else {
    Write-Host "  [STOPPED] Timesheet (8001): Not running" -ForegroundColor Red
}

Write-Host ""
Write-Host "Database Services:" -ForegroundColor Yellow
if ($postgres.TcpTestSucceeded) {
    Write-Host "  [RUNNING] PostgreSQL (5432): Connected" -ForegroundColor Green
} else {
    Write-Host "  [STOPPED] PostgreSQL (5432): Not available" -ForegroundColor Red
}

if ($redis.TcpTestSucceeded) {
    Write-Host "  [RUNNING] Redis (6379): Connected" -ForegroundColor Green
} else {
    Write-Host "  [STOPPED] Redis (6379): Not available" -ForegroundColor Red
}

# Check pgAdmin
Write-Host ""
Write-Host "Web Interfaces:" -ForegroundColor Yellow
try {
    $pgAdminResponse = Invoke-WebRequest -Uri "http://localhost:5050" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "  [RUNNING] pgAdmin (5050): http://localhost:5050" -ForegroundColor Green
}
catch {
    Write-Host "  [STOPPED] pgAdmin (5050): Not accessible" -ForegroundColor Red
}

Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Green
Write-Host "  .\weekend-setup.ps1              # Complete environment setup"
Write-Host "  .\scripts\quick.ps1 familyhub    # Start FamilyHub"
Write-Host "  .\scripts\quick.ps1 timesheet    # Start Timesheet"

# Show summary
$runningServices = @()
if ($familyhub.TcpTestSucceeded) { $runningServices += "FamilyHub" }
if ($timesheet.TcpTestSucceeded) { $runningServices += "Timesheet" }
if ($postgres.TcpTestSucceeded) { $runningServices += "PostgreSQL" }
if ($redis.TcpTestSucceeded) { $runningServices += "Redis" }

Write-Host ""
Write-Host "Environment Summary:" -ForegroundColor Cyan
Write-Host "  Running Services: $($runningServices.Count)/4" -ForegroundColor White
if ($runningServices.Count -gt 0) {
    Write-Host "  Active: $($runningServices -join ', ')" -ForegroundColor Green
}

if ($runningServices.Count -eq 4) {
    Write-Host ""
    Write-Host "  All services are running! Your development environment is ready." -ForegroundColor Green
} elseif ($runningServices.Count -eq 0) {
    Write-Host ""
    Write-Host "  No services running. Use .\weekend-setup.ps1 to start the environment." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "  Partial setup. Consider running .\weekend-setup.ps1 for full environment." -ForegroundColor Yellow
}
