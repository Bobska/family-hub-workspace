# FamilyHub - PostgreSQL 17 + Docker Deployment Makefile
# Created: August 31, 2025
# Purpose: Deployment automation for FamilyHub with PostgreSQL 17 and Docker

.PHONY: help test setup clean dev build up down logs shell migrate collectstatic superuser

# Default target
help:
	@echo "FamilyHub PostgreSQL 17 + Docker Deployment"
	@echo "============================================="
	@echo ""
	@echo "Available commands:"
	@echo "  help          - Show this help message"
	@echo "  test          - Test Make installation and basic commands"
	@echo "  setup         - Initial project setup"
	@echo "  clean         - Clean up containers and volumes"
	@echo ""
	@echo "Development:"
	@echo "  dev           - Start development environment"
	@echo "  build         - Build Docker containers"
	@echo "  up            - Start all services"
	@echo "  down          - Stop all services"
	@echo "  logs          - Show container logs"
	@echo "  shell         - Open Django shell in container"
	@echo ""
	@echo "Django:"
	@echo "  migrate       - Run Django migrations"
	@echo "  collectstatic - Collect static files"
	@echo "  superuser     - Create Django superuser"
	@echo ""
	@echo "Usage: make <command>"

# Test Make installation and basic functionality
test:
	@echo "✅ Testing Make installation..."
	@make --version | findstr "GNU"
	@echo "Current directory: %CD%"
	@git branch --show-current
	@python --version
	@docker --version || echo "❌ Docker not available"
	@docker-compose --version || echo "❌ Docker Compose not available"
	@echo ""
	@echo "✅ Make installation test complete!"
	@echo "🚀 Ready for PostgreSQL 17 + Docker deployment setup"

# Initial project setup
setup:
	@echo "🔧 Setting up FamilyHub PostgreSQL 17 + Docker environment..."
	@echo "Creating necessary directories..."
	@if not exist "docker" mkdir docker
	@if not exist "docker\\postgres" mkdir docker\\postgres
	@if not exist "docker\\postgres\\data" mkdir docker\\postgres\\data
	@if not exist "docker\\postgres\\init" mkdir docker\\postgres\\init
	@if not exist "logs" mkdir logs
	@if not exist "media" mkdir media
	@if not exist "staticfiles" mkdir staticfiles
	@echo "✅ Directory structure created"
	@echo "🎯 Next: Create Docker configuration files"

# Clean up Docker containers and volumes
clean:
	@echo "🧹 Cleaning up Docker environment..."
	@docker-compose down -v --remove-orphans 2>/dev/null || echo "No containers to stop"
	@docker system prune -f
	@echo "✅ Docker cleanup complete"

# Development environment commands (placeholders for now)
dev:
	@echo "🚀 Starting development environment..."
	@echo "TODO: Implement development Docker Compose setup"

build:
	@echo "🔨 Building Docker containers..."
	@echo "TODO: Implement Docker build process"

up:
	@echo "⬆️  Starting all services..."
	@echo "TODO: Implement docker-compose up"

down:
	@echo "⬇️  Stopping all services..."
	@echo "TODO: Implement docker-compose down"

logs:
	@echo "📜 Showing container logs..."
	@echo "TODO: Implement docker-compose logs"

shell:
	@echo "🐚 Opening Django shell..."
	@echo "TODO: Implement Docker shell access"

# Django management commands (placeholders for now)
migrate:
	@echo "🔄 Running Django migrations..."
	@echo "TODO: Implement Django migrate in container"

collectstatic:
	@echo "📦 Collecting static files..."
	@echo "TODO: Implement collectstatic in container"

superuser:
	@echo "👤 Creating Django superuser..."
	@echo "TODO: Implement createsuperuser in container"
