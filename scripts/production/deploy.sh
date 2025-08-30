#!/bin/bash
# Production deployment script for FamilyHub

set -e

echo "🚀 Starting FamilyHub Production Deployment..."

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ Error: .env.prod file not found!"
    echo "Please copy .env.prod.example to .env.prod and configure your production settings."
    exit 1
fi

# Build production images
echo "📦 Building production Docker images..."
docker-compose -f docker-compose.prod.yml build

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose -f docker-compose.prod.yml down

# Start services
echo "🔄 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to become healthy..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Test application
echo "🧪 Testing application..."
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    echo "✅ Application is healthy and responding!"
else
    echo "❌ Application health check failed!"
    echo "📋 Checking logs..."
    docker-compose -f docker-compose.prod.yml logs web
    exit 1
fi

echo ""
echo "🎉 Production deployment completed successfully!"
echo ""
echo "📋 Service URLs:"
echo "   🌐 Application: http://localhost"
echo "   🔧 Admin Panel: http://localhost/admin/"
echo "   💊 Health Check: http://localhost/health/"
echo ""
echo "📊 To view logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose -f docker-compose.prod.yml down"
