# Production Deployment Script for FamilyHub (Windows PowerShell)

Write-Host "🚀 Starting FamilyHub Production Deployment..." -ForegroundColor Green

# Check if .env.prod exists
if (-not (Test-Path ".env.prod")) {
    Write-Host "❌ Error: .env.prod file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.prod.example to .env.prod and configure your production settings." -ForegroundColor Yellow
    exit 1
}

# Build production images
Write-Host "📦 Building production Docker images..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml build

# Stop existing services
Write-Host "🛑 Stopping existing services..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml down

# Start services
Write-Host "🔄 Starting production services..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to become healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml ps

# Test application
Write-Host "🧪 Testing application..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost/health/" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Application is healthy and responding!" -ForegroundColor Green
    } else {
        throw "Health check returned status code: $($response.StatusCode)"
    }
} catch {
    Write-Host "❌ Application health check failed!" -ForegroundColor Red
    Write-Host "📋 Checking logs..." -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml logs web
    exit 1
}

Write-Host ""
Write-Host "🎉 Production deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service URLs:" -ForegroundColor Cyan
Write-Host "   🌐 Application: http://localhost" -ForegroundColor White
Write-Host "   🔧 Admin Panel: http://localhost/admin/" -ForegroundColor White
Write-Host "   💊 Health Check: http://localhost/health/" -ForegroundColor White
Write-Host ""
Write-Host "📊 To view logs:" -ForegroundColor Cyan
Write-Host "   docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop services:" -ForegroundColor Cyan
Write-Host "   docker-compose -f docker-compose.prod.yml down" -ForegroundColor White
