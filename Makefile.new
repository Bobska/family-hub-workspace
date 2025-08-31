# =============================================================================
# FamilyHub Makefile - Complete Operations Management
# =============================================================================
# Comprehensive command collection for development, production, and maintenance
# Usage: make <command> or make help for all available commands

.PHONY: help dev-local dev-docker build migrate makemigrations dbshell reset-db prod-build prod-up prod-logs backup restore shell test collectstatic clean logs stop status health check

# Default target
.DEFAULT_GOAL := help

# =============================================================================
# Help and Documentation
# =============================================================================

help: ## 📋 Show this help message with all available commands
	@echo "🚀 FamilyHub Operations Management"
	@echo "=================================="
	@echo ""
	@echo "📚 Available Commands:"
	@echo ""
	@echo "🔧 Environment Setup:"
	@echo "  setup             - Initial project setup (first-time use)"
	@echo ""
	@echo "🖥️  Development Commands:"
	@echo "  dev-local         - Run Django development server locally"
	@echo "  dev-docker        - Start Docker development environment"
	@echo "  dev-detached      - Start Docker development (background)"
	@echo "  build             - Build Docker containers (no cache)"
	@echo "  rebuild           - Rebuild and restart all services"
	@echo ""
	@echo "🗄️  Database Commands:"
	@echo "  migrate           - Apply database migrations"
	@echo "  makemigrations    - Create new database migrations"
	@echo "  dbshell           - Open database shell (PostgreSQL)"
	@echo "  reset-db          - Reset database (destroys all data)"
	@echo "  init-superuser    - Create superuser account"
	@echo ""
	@echo "🚀 Production Commands:"
	@echo "  prod-build        - Build production containers"
	@echo "  prod-up           - Start production environment"
	@echo "  prod-down         - Stop production environment"
	@echo "  prod-logs         - View production logs"
	@echo "  prod-deploy       - Full production deployment"
	@echo ""
	@echo "💾 Backup Commands:"
	@echo "  backup            - Create database backup"
	@echo "  backup-prod       - Create production database backup"
	@echo "  restore           - Restore database from backup"
	@echo "  list-backups      - List all available backups"
	@echo ""
	@echo "🧪 Testing and QA:"
	@echo "  test              - Run test suite"
	@echo "  check             - Run Django system checks"
	@echo "  check-deploy      - Run Django deployment checks"
	@echo ""
	@echo "🔧 Utility Commands:"
	@echo "  shell             - Open Django shell"
	@echo "  collectstatic     - Collect static files"
	@echo "  logs              - View development logs"
	@echo "  status            - Show service status"
	@echo "  health            - Check application health"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  stop              - Stop all services"
	@echo "  restart           - Restart all services"
	@echo "  clean             - Clean Docker resources"
	@echo ""
	@echo "ℹ️  Information:"
	@echo "  info              - Show project information"
	@echo "  urls              - Show application URLs"
	@echo "  version           - Show version information"
	@echo ""

# =============================================================================
# Environment Setup and Initialization
# =============================================================================

setup: ## 🔧 Initial project setup (first-time use)
	@echo "🔧 Setting up FamilyHub environment..."
	@if not exist .env ( \
		echo "📝 Creating environment file from Docker template..." && \
		copy .env.docker .env && \
		echo "✅ Environment file created. Edit .env if needed." \
	) else ( \
		echo "✅ Environment file already exists." \
	)
	@echo "🏗️  Building Docker containers..."
	@docker-compose build
	@echo "🎉 Setup complete! Run 'make dev-docker' to start development."

# =============================================================================
# Development Commands
# =============================================================================

dev-local: ## 🖥️  Run Django development server locally (without Docker)
	@echo "🖥️  Starting local development server..."
	@cd FamilyHub && python manage.py runserver --settings=FamilyHub.settings.development

dev-docker: ## 🐳 Start Docker development environment
	@echo "🐳 Starting Docker development environment..."
	@docker-compose up

dev-detached: ## 🐳 Start Docker development environment in background
	@echo "🐳 Starting Docker development environment (detached)..."
	@docker-compose up -d
	@echo "✅ Services started in background"
	@$(MAKE) status

build: ## 🏗️  Build Docker containers (no cache)
	@echo "🏗️  Building Docker containers from scratch..."
	@docker-compose build --no-cache

rebuild: ## 🔄 Rebuild and restart all services
	@echo "🔄 Rebuilding and restarting all services..."
	@docker-compose down
	@docker-compose build --no-cache
	@docker-compose up -d
	@$(MAKE) status

# =============================================================================
# Database Commands
# =============================================================================

migrate: ## 🗄️  Apply database migrations
	@echo "🗄️  Applying database migrations..."
	@docker-compose exec web python manage.py migrate

makemigrations: ## 📝 Create new database migrations
	@echo "📝 Creating database migrations..."
	@docker-compose exec web python manage.py makemigrations

dbshell: ## 💾 Open database shell (PostgreSQL)
	@echo "💾 Opening database shell..."
	@docker-compose exec db psql -U familyhub_user -d familyhub_docker

reset-db: ## 🔄 Reset database (WARNING: destroys all data)
	@echo "⚠️  WARNING: This will destroy all database data!"
	@set /p confirm="Are you sure? Type 'yes' to continue: "
	@if not "%confirm%"=="yes" exit /b 1
	@echo "🗑️  Stopping services and removing volumes..."
	@docker-compose down -v
	@echo "🔄 Starting database service..."
	@docker-compose up -d db
	@echo "⏳ Waiting for database to be ready..."
	@timeout /t 10 /nobreak >nul
	@echo "🗄️  Running migrations..."
	@docker-compose exec web python manage.py migrate
	@echo "👤 Creating superuser..."
	@docker-compose exec web python manage.py init_superuser
	@echo "✅ Database reset complete"

init-superuser: ## 👤 Create superuser account
	@echo "👤 Creating superuser account..."
	@docker-compose exec web python manage.py init_superuser

# =============================================================================
# Production Commands
# =============================================================================

prod-build: ## 🚀 Build production containers
	@echo "🚀 Building production containers..."
	@docker-compose -f docker-compose.prod.yml build --no-cache

prod-up: ## 🌐 Start production environment
	@echo "🌐 Starting production environment..."
	@if not exist .env.prod ( \
		echo "❌ .env.prod file not found!" && \
		echo "📝 Copy .env.prod.example to .env.prod and configure it first." && \
		exit /b 1 \
	)
	@docker-compose -f docker-compose.prod.yml up -d
	@echo "⏳ Waiting for services to start..."
	@timeout /t 30 /nobreak >nul
	@$(MAKE) prod-status

prod-down: ## 🛑 Stop production environment
	@echo "🛑 Stopping production environment..."
	@docker-compose -f docker-compose.prod.yml down

prod-logs: ## 📋 View production logs
	@echo "📋 Viewing production logs..."
	@docker-compose -f docker-compose.prod.yml logs -f

prod-status: ## 📊 Check production service status
	@echo "📊 Production service status:"
	@docker-compose -f docker-compose.prod.yml ps

prod-deploy: ## 🚀 Full production deployment
	@echo "🚀 Starting full production deployment..."
	@$(MAKE) prod-build
	@$(MAKE) prod-up
	@echo "✅ Production deployment complete!"

# =============================================================================
# Backup and Restore Commands
# =============================================================================

backup: ## 💾 Create database backup
	@echo "💾 Creating database backup..."
	@if not exist backups mkdir backups
	@for /f "tokens=2 delims= " %%i in ('date /t') do set mydate=%%i
	@for /f "tokens=1-2 delims=/:" %%a in ('time /t') do set mytime=%%a%%b
	@docker-compose exec db pg_dump -U familyhub_user familyhub_docker > backups\backup_%mydate%_%mytime%.sql
	@echo "✅ Backup created in backups\ directory"

restore: ## 🔄 Restore database from backup (requires BACKUP_FILE=path)
	@if "%BACKUP_FILE%"=="" ( \
		echo "❌ Error: BACKUP_FILE not specified" && \
		echo "Usage: make restore BACKUP_FILE=backups\backup_file.sql" && \
		exit /b 1 \
	)
	@echo "🔄 Restoring database from %BACKUP_FILE%..."
	@type "%BACKUP_FILE%" | docker-compose exec -T db psql -U familyhub_user familyhub_docker
	@echo "✅ Database restored from %BACKUP_FILE%"

list-backups: ## 📋 List all available backups
	@echo "📋 Available backups:"
	@if exist backups ( dir /b backups\*.sql ) else ( echo "No backups found. Run 'make backup' to create one." )

# =============================================================================
# Testing and Quality Assurance
# =============================================================================

test: ## 🧪 Run test suite
	@echo "🧪 Running test suite..."
	@docker-compose exec web python manage.py test

check: ## ✅ Run Django system checks
	@echo "✅ Running Django system checks..."
	@docker-compose exec web python manage.py check

check-deploy: ## 🚀 Run Django deployment checks
	@echo "🚀 Running Django deployment checks..."
	@docker-compose exec web python manage.py check --deploy

# =============================================================================
# Utility Commands
# =============================================================================

shell: ## 🐚 Open Django shell
	@echo "🐚 Opening Django shell..."
	@docker-compose exec web python manage.py shell

collectstatic: ## 📁 Collect static files
	@echo "📁 Collecting static files..."
	@docker-compose exec web python manage.py collectstatic --noinput

logs: ## 📋 View development logs (follow mode)
	@echo "📋 Viewing development logs..."
	@docker-compose logs -f

logs-web: ## 📋 View web service logs only
	@echo "📋 Viewing web service logs..."
	@docker-compose logs -f web

logs-db: ## 📋 View database logs only
	@echo "📋 Viewing database logs..."
	@docker-compose logs -f db

status: ## 📊 Show service status
	@echo "📊 Service status:"
	@docker-compose ps

health: ## 🏥 Check application health
	@echo "🏥 Checking application health..."
	@echo "📡 Testing health endpoint..."
	@powershell -Command "try { Invoke-WebRequest -Uri http://localhost:8000/health/ -UseBasicParsing | Select-Object StatusCode } catch { Write-Host 'Health check failed' }"
	@echo "🌐 Testing main page..."
	@powershell -Command "try { Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing | Select-Object StatusCode } catch { Write-Host 'Main page failed' }"

# =============================================================================
# Maintenance Commands
# =============================================================================

stop: ## 🛑 Stop all services
	@echo "🛑 Stopping all services..."
	@docker-compose down

restart: ## 🔄 Restart all services
	@echo "🔄 Restarting all services..."
	@docker-compose restart

restart-web: ## 🔄 Restart web service only
	@echo "🔄 Restarting web service..."
	@docker-compose restart web

clean: ## 🧹 Stop services and clean Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	@docker-compose down
	@docker system prune -f
	@echo "✅ Cleanup complete"

clean-all: ## 🗑️  Remove all containers, volumes, and images (DESTRUCTIVE)
	@echo "⚠️  WARNING: This will remove ALL Docker containers, volumes, and images!"
	@set /p confirm="Are you sure? Type 'yes' to continue: "
	@if not "%confirm%"=="yes" exit /b 1
	@docker-compose down -v --rmi all
	@docker system prune -a -f --volumes
	@echo "✅ All Docker resources removed"

# =============================================================================
# Information Commands
# =============================================================================

info: ## ℹ️  Show project information
	@echo "ℹ️  FamilyHub Project Information"
	@echo "================================"
	@echo "📍 Project: FamilyHub Family Management Platform"
	@echo "🌍 Location: Auckland, New Zealand (Pacific/Auckland)"
	@echo "🐍 Python: 3.11+"
	@echo "🎯 Django: 5.1+"
	@echo "🐳 Docker: Required for development"
	@echo "🗄️  Database: PostgreSQL 17"
	@echo "⚡ Cache: Redis (production)"
	@echo ""
	@git branch --show-current
	@if exist .env ( echo "📦 Environment file: ✅ .env exists" ) else ( echo "📦 Environment file: ❌ .env missing" )
	@docker --version 2>nul || echo "🐳 Docker status: ❌ Docker not available"

urls: ## 🌐 Show application URLs
	@echo "🌐 Application URLs"
	@echo "==================="
	@echo "🏠 Development:     http://localhost:8000"
	@echo "🔧 Admin Panel:     http://localhost:8000/admin/"
	@echo "💊 Health Check:    http://localhost:8000/health/"
	@echo "⏰ Timesheet App:   http://localhost:8000/timesheet/"
	@echo ""
	@echo "🚀 Production URLs (if running):"
	@echo "🏠 Main:            http://localhost"
	@echo "🔧 Admin:           http://localhost/admin/"
	@echo "💊 Health:          http://localhost/health/"

version: ## 📌 Show version information
	@echo "📌 Version Information"
	@echo "====================="
	@docker-compose exec web python --version 2>nul || echo "❌ Web container not running"
	@docker-compose exec web python manage.py --version 2>nul || echo "❌ Django not accessible"
	@docker-compose exec db postgres --version 2>nul || echo "❌ Database container not running"
	@git --version
	@docker --version
	@docker-compose --version

# =============================================================================
# Development Workflow Shortcuts
# =============================================================================

fresh-start: ## 🆕 Complete fresh start (build, migrate, create superuser)
	@echo "🆕 Starting fresh development environment..."
	@$(MAKE) stop
	@$(MAKE) build
	@$(MAKE) dev-detached
	@timeout /t 15 /nobreak >nul
	@$(MAKE) migrate
	@$(MAKE) init-superuser
	@$(MAKE) status
	@echo "✅ Fresh start complete! Application ready at http://localhost:8000"

quick-restart: ## ⚡ Quick restart without rebuild
	@echo "⚡ Quick restart..."
	@docker-compose restart
	@$(MAKE) status

deploy-dev: ## 🚀 Deploy development environment
	@echo "🚀 Deploying development environment..."
	@$(MAKE) build
	@$(MAKE) dev-detached
	@$(MAKE) migrate
	@$(MAKE) collectstatic
	@$(MAKE) status
	@echo "✅ Development deployment complete!"

# =============================================================================
# Notes and Usage Examples
# =============================================================================

# 📝 Usage Examples:
# make setup              # First-time project setup
# make dev-docker         # Start development environment
# make migrate            # Apply database migrations
# make test               # Run test suite
# make backup             # Create database backup
# make prod-deploy        # Deploy to production
# make clean              # Clean up Docker resources
# make help               # Show all available commands

# 🔧 Environment Files:
# .env                    # Your environment (copy from .env.docker or .env.local)
# .env.docker             # Docker development template
# .env.local              # Local development template  
# .env.prod               # Production environment (copy from .env.prod.example)

# 🚀 Quick Start:
# 1. make setup           # Initial setup
# 2. make dev-docker      # Start development
# 3. Open http://localhost:8000

# 📋 Troubleshooting:
# make logs               # View application logs
# make status             # Check service status
# make health             # Test application health
# make clean && make build # Complete rebuild
