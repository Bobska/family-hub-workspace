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
	@echo "🔧 Local Development (PowerShell Scripts):"
	@echo "  local-setup       - Setup local environment (venv, dependencies)"
	@echo "  local-start       - Start local development server (basic)"
	@echo "  local-start-full  - Start with integrated apps (timesheet included)"
	@echo "  local-migrate     - Run local database migrations"
	@echo "  local-test        - Run tests in local environment"
	@echo "  local-shell       - Open Django shell in local environment"
	@echo "  local-superuser   - Create superuser in local environment"
	@echo "  local-check       - Run Django system checks locally"
	@echo "  local-clean       - Clean local development environment"
	@echo ""
	@echo "📱 Standalone Apps (Independent Development):"
	@echo "  local-start-timesheet      - Start timesheet app (port 8001)"
	@echo "  local-start-daycare        - Start daycare invoice app (port 8002)"
	@echo "  local-start-employment     - Start employment history app (port 8003)"
	@echo "  local-start-payments       - Start upcoming payments app (port 8004)"
	@echo "  local-start-credit         - Start credit card mgmt app (port 8005)"
	@echo "  local-start-budget         - Start household budget app (port 8006)"
	@echo "  local-setup-timesheet      - Setup timesheet standalone environment"
	@echo "  local-test-timesheet       - Test timesheet standalone app"
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

# =============================================================================
# Local Development Script Shortcuts (PowerShell-based)
# =============================================================================

local-setup: ## 🔧 Setup local development environment (virtual env, dependencies)
	@echo "🔧 Setting up local development environment..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -File dev-setup-new.ps1

local-start: ## 🚀 Start local development server (using PowerShell script)
	@echo "🚀 Starting local development server..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -File dev-start-simple.ps1

local-start-full: ## 🚀 Start local development server with all integrated apps
	@echo "🚀 Starting local development server with full integration..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py check --settings=FamilyHub.settings.development_full; python manage.py runserver --settings=FamilyHub.settings.development_full }"

local-migrate: ## 🗄️  Run local database migrations
	@echo "🗄️  Running local database migrations..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py makemigrations --settings=FamilyHub.settings.development; python manage.py migrate --settings=FamilyHub.settings.development }"

local-test: ## 🧪 Run tests in local environment
	@echo "🧪 Running tests in local environment..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py test --settings=FamilyHub.settings.development }"

local-shell: ## 🐚 Open Django shell in local environment
	@echo "🐚 Opening Django shell in local environment..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py shell --settings=FamilyHub.settings.development }"

local-superuser: ## 👤 Create superuser in local environment
	@echo "👤 Creating superuser in local environment..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py createsuperuser --settings=FamilyHub.settings.development }"

local-check: ## ✅ Run Django system checks in local environment
	@echo "✅ Running Django system checks in local environment..."
	@cd FamilyHub && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py check --settings=FamilyHub.settings.development }"

local-clean: ## 🧹 Clean local development environment
	@echo "🧹 Cleaning local development environment..."
	@cd FamilyHub && if exist "db.sqlite3" del "db.sqlite3"
	@cd FamilyHub && if exist "__pycache__" rmdir /s /q "__pycache__"
	@echo "✅ Local environment cleaned"

# =============================================================================
# Standalone Apps Development (Independent of FamilyHub)
# =============================================================================

local-start-timesheet: ## 📋 Start timesheet standalone app (port 8001)
	@echo "📋 Starting timesheet standalone app on port 8001..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8001 }"

# =============================================================================
# Docker Integration Testing (PROMPT 3)
# =============================================================================

docker-test: ## 🐳 Run Docker integration tests (PROMPT 3)
	@echo "🐳 Running Docker integration tests..."
	@python docker_test.py

docker-build-familyhub: ## 🏗️ Build FamilyHub Docker image only
	@echo "🏗️ Building FamilyHub Docker image..."
	@docker-compose build familyhub

docker-start-familyhub: ## 🚀 Start FamilyHub in Docker
	@echo "🚀 Starting FamilyHub in Docker..."
	@docker-compose up -d familyhub
	@echo "✅ FamilyHub started at http://localhost:8000"

docker-logs-familyhub: ## 📋 View FamilyHub Docker logs
	@echo "📋 Viewing FamilyHub Docker logs..."
	@docker-compose logs -f familyhub

docker-stop-familyhub: ## 🛑 Stop FamilyHub Docker containers
	@echo "🛑 Stopping FamilyHub Docker containers..."
	@docker-compose down

local-start-daycare: ## 🏠 Start daycare invoice standalone app (port 8002)
	@echo "🏠 Starting daycare invoice standalone app on port 8002..."
	@cd standalone-apps\daycare_invoice && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8002 }"

local-start-employment: ## 💼 Start employment history standalone app (port 8003)
	@echo "💼 Starting employment history standalone app on port 8003..."
	@cd standalone-apps\employment_history && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8003 }"

local-start-payments: ## 💰 Start upcoming payments standalone app (port 8004)
	@echo "💰 Starting upcoming payments standalone app on port 8004..."
	@cd standalone-apps\upcoming_payments && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8004 }"

local-start-credit: ## 💳 Start credit card mgmt standalone app (port 8005)
	@echo "💳 Starting credit card management standalone app on port 8005..."
	@cd standalone-apps\credit_card_mgmt && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8005 }"

local-start-budget: ## 🏦 Start household budget standalone app (port 8006)
	@echo "🏦 Starting household budget standalone app on port 8006..."
	@cd standalone-apps\household_budget && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py runserver 8006 }"

local-setup-timesheet: ## 🔧 Setup timesheet standalone environment
	@echo "🔧 Setting up timesheet standalone environment..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { if (!(Test-Path venv)) { python -m venv venv }; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; python manage.py migrate }"
	@echo "✅ Timesheet standalone environment ready"

local-test-timesheet: ## 🧪 Test timesheet standalone app
	@echo "🧪 Testing timesheet standalone app..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py test }"

local-check-timesheet: ## ✅ Check timesheet standalone app
	@echo "✅ Checking timesheet standalone app..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py check }"

local-migrate-timesheet: ## 🗄️ Migrate timesheet standalone app
	@echo "🗄️ Migrating timesheet standalone app..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py makemigrations; python manage.py migrate }"

local-shell-timesheet: ## 🐚 Open timesheet standalone Django shell
	@echo "🐚 Opening timesheet standalone Django shell..."
	@cd standalone-apps\timesheet && powershell -ExecutionPolicy Bypass -Command "& { .\venv\Scripts\Activate.ps1; python manage.py shell }"

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

local-fresh-start: ## 🆕 Complete fresh local start (setup, migrate, superuser, run)
	@echo "🆕 Starting fresh local development environment..."
	@$(MAKE) local-setup
	@$(MAKE) local-migrate
	@$(MAKE) local-superuser
	@$(MAKE) local-start
	@echo "✅ Local fresh start complete! Application ready at http://127.0.0.1:8000"

local-start-all-apps: ## 🚀 Start all standalone apps simultaneously (background)
	@echo "🚀 Starting all standalone apps..."
	@echo "📋 Timesheet: http://127.0.0.1:8001"
	@echo "🏠 Daycare: http://127.0.0.1:8002"
	@echo "💼 Employment: http://127.0.0.1:8003"
	@echo "💰 Payments: http://127.0.0.1:8004"
	@echo "💳 Credit: http://127.0.0.1:8005"
	@echo "🏦 Budget: http://127.0.0.1:8006"
	@start powershell -Command "cd standalone-apps\timesheet; .\venv\Scripts\Activate.ps1; python manage.py runserver 8001"
	@start powershell -Command "cd standalone-apps\daycare_invoice; .\venv\Scripts\Activate.ps1; python manage.py runserver 8002"
	@start powershell -Command "cd standalone-apps\employment_history; .\venv\Scripts\Activate.ps1; python manage.py runserver 8003"
	@start powershell -Command "cd standalone-apps\upcoming_payments; .\venv\Scripts\Activate.ps1; python manage.py runserver 8004"
	@start powershell -Command "cd standalone-apps\credit_card_mgmt; .\venv\Scripts\Activate.ps1; python manage.py runserver 8005"
	@start powershell -Command "cd standalone-apps\household_budget; .\venv\Scripts\Activate.ps1; python manage.py runserver 8006"
	@echo "✅ All apps starting in separate windows"

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
