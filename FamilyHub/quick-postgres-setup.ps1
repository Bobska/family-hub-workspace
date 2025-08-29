# ⚡ FamilyHub Quick PostgreSQL Setup Script (PowerShell)
# 🚀 Get PostgreSQL 17.6 + pgAdmin running in 5 minutes!

Write-Host "⚡ FamilyHub Quick PostgreSQL Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Blue

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found. Please install Docker first." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose not found. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker and Docker Compose found" -ForegroundColor Green

# Check if services are already running
$runningContainer = docker ps --format "{{.Names}}" | Select-String "familyhub_postgres_dev_quick"
if ($runningContainer) {
    Write-Host "⚠️  PostgreSQL container already running" -ForegroundColor Yellow
    Write-Host "Choose an option:" -ForegroundColor Blue
    Write-Host "1) Stop and restart"
    Write-Host "2) Keep running and exit"  
    Write-Host "3) Stop and clean everything"
    
    $choice = Read-Host "Enter choice [1-3]"
    
    switch ($choice) {
        "1" {
            Write-Host "🔄 Restarting services..." -ForegroundColor Yellow
            docker-compose -f docker-compose.quick.yml --env-file .env.quick down
        }
        "2" {
            Write-Host "✅ Services already running!" -ForegroundColor Green
            Write-Host "🌐 pgAdmin: http://localhost:5050" -ForegroundColor Blue
            Write-Host "📊 PostgreSQL: localhost:5432" -ForegroundColor Blue
            exit 0
        }
        "3" {
            Write-Host "🗑️  Cleaning everything..." -ForegroundColor Red
            docker-compose -f docker-compose.quick.yml --env-file .env.quick down -v
        }
        default {
            Write-Host "❌ Invalid choice" -ForegroundColor Red
            exit 1
        }
    }
}

# Start services
Write-Host "🚀 Starting PostgreSQL 17.6 + pgAdmin..." -ForegroundColor Blue
docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "🔍 Checking service status..." -ForegroundColor Blue

# Check PostgreSQL
try {
    $null = docker-compose -f docker-compose.quick.yml --env-file .env.quick exec -T postgres-dev pg_isready -U django -d familyhub 2>$null
    Write-Host "✅ PostgreSQL 17.6: Running" -ForegroundColor Green
    $postgresStatus = "OK"
} catch {
    Write-Host "❌ PostgreSQL 17.6: Not ready" -ForegroundColor Red
    $postgresStatus = "FAIL"
}

# Check pgAdmin
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5050" -TimeoutSec 5 -UseBasicParsing 2>$null
    Write-Host "✅ pgAdmin 4: Running" -ForegroundColor Green
    $pgadminStatus = "OK"
} catch {
    Write-Host "❌ pgAdmin 4: Not ready" -ForegroundColor Red
    $pgadminStatus = "FAIL"
}

# Show results
Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "===================="

if ($postgresStatus -eq "OK" -and $pgadminStatus -eq "OK") {
    Write-Host "✅ All services running successfully!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🌐 Access Points:" -ForegroundColor Blue
    Write-Host "📊 pgAdmin Web: " -NoNewline -ForegroundColor White
    Write-Host "http://localhost:5050" -ForegroundColor Yellow
    Write-Host "   └─ Email: " -NoNewline -ForegroundColor White
    Write-Host "admin@familyhub.local" -ForegroundColor Yellow
    Write-Host "   └─ Password: " -NoNewline -ForegroundColor White
    Write-Host "admin123" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🐘 PostgreSQL Direct: " -NoNewline -ForegroundColor White
    Write-Host "localhost:5432" -ForegroundColor Yellow
    Write-Host "   └─ Database: " -NoNewline -ForegroundColor White
    Write-Host "familyhub" -ForegroundColor Yellow
    Write-Host "   └─ Username: " -NoNewline -ForegroundColor White
    Write-Host "django" -ForegroundColor Yellow
    Write-Host "   └─ Password: " -NoNewline -ForegroundColor White
    Write-Host "secretpass" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔗 Django Database URL:" -ForegroundColor White
    Write-Host "   " -NoNewline
    Write-Host "postgresql://django:secretpass@localhost:5432/familyhub" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "🛠️  Quick Commands:" -ForegroundColor Blue
    Write-Host "📊 View logs: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml logs -f" -ForegroundColor Yellow
    Write-Host "🔄 Restart: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml restart" -ForegroundColor Yellow
    Write-Host "🛑 Stop: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml down" -ForegroundColor Yellow
    Write-Host "🗑️  Clean: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml down -v" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "📖 Documentation: README.quick-postgres.md" -ForegroundColor Blue
    
    exit 0
} else {
    Write-Host "❌ Some services failed to start" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Troubleshooting:" -ForegroundColor Blue
    Write-Host "📊 View logs: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml logs" -ForegroundColor Yellow
    Write-Host "🔄 Restart: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml restart" -ForegroundColor Yellow
    Write-Host "🛑 Stop: " -NoNewline -ForegroundColor White
    Write-Host "docker-compose -f docker-compose.quick.yml down" -ForegroundColor Yellow
    
    exit 1
}
