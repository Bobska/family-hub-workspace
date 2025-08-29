# FamilyHub Development Workflow Makefile
# Author: FamilyHub Team
# Date: August 29, 2025
# Version: 1.0.0

# ===================================================================
# QUICK REFERENCE
# ===================================================================
# make help          - Show all available commands
# make dev           - Start development environment  
# make prod          - Start production environment
# make quick         - Start quick PostgreSQL setup (5 minutes)
# make build         - Rebuild all containers
# make migrate       - Run Django migrations
# make shell         - Open Django shell
# make dbshell       - Open PostgreSQL shell
# make test          - Run tests
# make backup        - Backup database
# make restore       - Restore database
# make logs          - View logs
# make stop          - Stop all containers
# ===================================================================

# Default shell and colors for Windows PowerShell compatibility
SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

# Colors for output (PowerShell compatible)
CYAN = Write-Host -ForegroundColor Cyan
GREEN = Write-Host -ForegroundColor Green
YELLOW = Write-Host -ForegroundColor Yellow
RED = Write-Host -ForegroundColor Red
BLUE = Write-Host -ForegroundColor Blue

# Project configuration
PROJECT_NAME = familyhub
COMPOSE_DEV = docker-compose -f docker-compose.dev.yml
COMPOSE_PROD = docker-compose -f docker-compose.production.yml
COMPOSE_QUICK = docker-compose -f docker-compose.quick.yml --env-file .env.quick
DJANGO_SERVICE = django
POSTGRES_SERVICE = postgres-dev
BACKUP_DIR = backups
TIMESTAMP = $(shell Get-Date -Format "yyyyMMdd_HHmmss")

# Default target
.DEFAULT_GOAL := help

# ===================================================================
# HELP & INFORMATION
# ===================================================================

.PHONY: help
help: ## Show this help message
	@$(CYAN) "FamilyHub Development Workflow Commands"
	@$(CYAN) "=========================================="
	@echo ""
	@$(BLUE) "Quick Start:"
	@echo "  make quick         Start quick PostgreSQL setup (5 minutes)"
	@echo "  make dev           Start development environment"
	@echo "  make prod          Start production environment"
	@echo ""
	@$(BLUE) "Development:"
	@echo "  make build         Rebuild all containers"
	@echo "  make migrate       Run Django migrations"
	@echo "  make shell         Open Django shell"
	@echo "  make dbshell       Open PostgreSQL shell"
	@echo "  make test          Run tests"
	@echo ""
	@$(BLUE) "Database:"
	@echo "  make backup        Backup database"
	@echo "  make restore       Restore database from backup"
	@echo "  make reset-db      Reset database (WARNING: Deletes all data)"
	@echo ""
	@$(BLUE) "Monitoring:"
	@echo "  make logs          View all service logs"
	@echo "  make logs-django   View Django logs only"
	@echo "  make logs-postgres View PostgreSQL logs only"
	@echo "  make status        Show service status"
	@echo ""
	@$(BLUE) "Control:"
	@echo "  make stop          Stop all containers"
	@echo "  make restart       Restart all services"
	@echo "  make clean         Clean up containers and volumes"
	@echo ""
	@$(BLUE) "Utilities:"
	@echo "  make health        Check application health"
	@echo "  make setup         Initial project setup"
	@echo "  make update        Update dependencies"

# ===================================================================
# ENVIRONMENT STARTUP
# ===================================================================

.PHONY: quick
quick: ## Start quick PostgreSQL setup (5 minutes)
	@$(CYAN) "Starting Quick PostgreSQL Environment..."
	@powershell -Command "if (Test-Path 'quick-postgres-setup.ps1') { .\quick-postgres-setup.ps1 } else { docker-compose -f docker-compose.quick.yml up -d; Start-Sleep 10; Write-Host -ForegroundColor Green 'Quick PostgreSQL environment started!'; Write-Host -ForegroundColor Blue 'pgAdmin: http://localhost:5050'; Write-Host -ForegroundColor Blue 'PostgreSQL: localhost:5432' }"

.PHONY: dev
dev: ## Start development environment
	@$(CYAN) "Starting Development Environment..."
	@powershell -Command "if (Test-Path 'docker-compose.dev.yml') { docker-compose -f docker-compose.dev.yml up -d; Start-Sleep 15; Write-Host -ForegroundColor Green 'Development environment started!'; Write-Host -ForegroundColor Blue 'Django: http://localhost:8000'; Write-Host -ForegroundColor Blue 'pgAdmin: http://localhost:5050' } else { Write-Host -ForegroundColor Red 'docker-compose.dev.yml not found'; Write-Host -ForegroundColor Yellow 'Use make quick for immediate PostgreSQL setup' }"

.PHONY: prod
prod: ## Start production environment
	@$(CYAN) "Starting Production Environment..."
	@powershell -Command "if (Test-Path 'docker-compose.production.yml') { docker-compose -f docker-compose.production.yml up -d; Start-Sleep 30; Write-Host -ForegroundColor Green 'Production environment started!'; Write-Host -ForegroundColor Blue 'Application: https://localhost'; Write-Host -ForegroundColor Blue 'Monitoring: Check make logs for status' } else { Write-Host -ForegroundColor Red 'docker-compose.production.yml not found'; Write-Host -ForegroundColor Yellow 'Use make quick for immediate PostgreSQL setup' }"

# ===================================================================
# DEVELOPMENT COMMANDS
# ===================================================================

.PHONY: build
build: ## Rebuild all containers
	@$(CYAN) "Rebuilding All Containers..."
	@powershell -Command "if (Test-Path 'docker-compose.dev.yml') { docker-compose -f docker-compose.dev.yml build --no-cache; Write-Host -ForegroundColor Green 'Development containers rebuilt!' }"
	@powershell -Command "if (Test-Path 'docker-compose.production.yml') { docker-compose -f docker-compose.production.yml build --no-cache; Write-Host -ForegroundColor Green 'Production containers rebuilt!' }"
	@docker-compose -f docker-compose.quick.yml build --no-cache
	@$(GREEN) "All containers rebuilt successfully!"

.PHONY: migrate
migrate: ## Run Django migrations
	@$(CYAN) "Running Django Migrations..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*django').Count -gt 0) { docker-compose exec django python manage.py makemigrations; docker-compose exec django python manage.py migrate; Write-Host -ForegroundColor Green 'Migrations completed!' } else { Write-Host -ForegroundColor Yellow 'Django container not running. Starting quick environment...'; make quick; Start-Sleep 10; cd FamilyHub; python manage.py makemigrations; python manage.py migrate; Write-Host -ForegroundColor Green 'Migrations completed locally!' }"

.PHONY: shell
shell: ## Open Django shell
	@$(CYAN) "Opening Django Shell..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*django').Count -gt 0) { docker-compose exec django python manage.py shell } else { Write-Host -ForegroundColor Yellow 'Django container not running. Using local environment...'; cd FamilyHub; python manage.py shell }"

.PHONY: dbshell
dbshell: ## Open PostgreSQL shell
	@$(CYAN) "Opening PostgreSQL Shell..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*postgres').Count -gt 0) { docker-compose -f docker-compose.quick.yml exec postgres-dev psql -U django -d familyhub } else { Write-Host -ForegroundColor Yellow 'PostgreSQL container not running. Starting quick environment...'; make quick; Start-Sleep 10; docker-compose -f docker-compose.quick.yml exec postgres-dev psql -U django -d familyhub }"

.PHONY: test
test: ## Run tests
	@$(CYAN) "Running Tests..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*django').Count -gt 0) { docker-compose exec django python manage.py test } else { Write-Host -ForegroundColor Yellow 'Django container not running. Running tests locally...'; cd FamilyHub; python manage.py test }"
	@$(GREEN) "Tests completed!"

# ===================================================================
# DATABASE MANAGEMENT
# ===================================================================

.PHONY: backup
backup: ## Backup database
	@$(CYAN) "Creating Database Backup..."
	@powershell -Command "if (!(Test-Path 'backups')) { New-Item -ItemType Directory -Path 'backups' | Out-Null }"
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*postgres').Count -gt 0) { docker-compose exec -T postgres-dev pg_dump -U django -d familyhub > 'backups/backup_$(Get-Date -Format \"yyyyMMdd_HHmmss\").sql'; Write-Host -ForegroundColor Green 'Database backup created' } else { Write-Host -ForegroundColor Red 'PostgreSQL container not running'; Write-Host -ForegroundColor Yellow 'Start environment first: make quick' }"

.PHONY: restore
restore: ## Restore database from backup
	@$(CYAN) "Restoring Database from Backup..."
	@powershell -Command "if (!(Test-Path 'backups')) { Write-Host -ForegroundColor Red 'Backup directory not found'; exit 1 }"
	@powershell -Command "$$latest = Get-ChildItem 'backups' -Filter '*.sql' | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($$latest) { Write-Host -ForegroundColor Yellow \"Using latest backup: $$($latest.Name)\"; if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*postgres').Count -gt 0) { Get-Content \"backups/$$($latest.Name)\" | docker-compose exec -T postgres-dev psql -U django -d familyhub; Write-Host -ForegroundColor Green \"Database restored from: $$($latest.Name)\" } else { Write-Host -ForegroundColor Red 'PostgreSQL container not running' } } else { Write-Host -ForegroundColor Red 'No backup files found in backups directory' }"

.PHONY: reset-db
reset-db: ## Reset database (WARNING: Deletes all data)
	@$(RED) "WARNING: This will delete ALL database data!"
	@powershell -Command "$$confirm = Read-Host 'Type YES to confirm database reset'; if ($$confirm -eq 'YES') { Write-Host -ForegroundColor Cyan 'Resetting Database...'; docker-compose -f docker-compose.quick.yml down -v; docker-compose -f docker-compose.quick.yml up -d; Start-Sleep 15; make migrate; Write-Host -ForegroundColor Green 'Database reset completed!' } else { Write-Host -ForegroundColor Yellow 'Database reset cancelled' }"

# ===================================================================
# MONITORING & LOGS
# ===================================================================

.PHONY: logs
logs: ## View all service logs
	@$(CYAN) "Viewing All Service Logs..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub').Count -gt 0) { docker-compose logs -f } else { Write-Host -ForegroundColor Yellow 'No containers running'; Write-Host -ForegroundColor Blue 'Start environment: make quick | make dev | make prod' }"

.PHONY: logs-django
logs-django: ## View Django logs only
	@$(CYAN) "Viewing Django Logs..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*django').Count -gt 0) { docker-compose logs -f django } else { Write-Host -ForegroundColor Yellow 'Django container not running' }"

.PHONY: logs-postgres
logs-postgres: ## View PostgreSQL logs only
	@$(CYAN) "Viewing PostgreSQL Logs..."
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*postgres').Count -gt 0) { docker-compose -f docker-compose.quick.yml logs -f postgres-dev } else { Write-Host -ForegroundColor Yellow 'PostgreSQL container not running' }"

.PHONY: status
status: ## Show service status
	@$(CYAN) "Service Status:"
	@$(CYAN) "=================="
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=$(PROJECT_NAME)"
	@echo ""
	@$(BLUE) "PostgreSQL Connection Test:"
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String '$(PROJECT_NAME).*postgres').Count -gt 0) { if (docker-compose -f docker-compose.quick.yml exec -T postgres pg_isready -U django -d familyhub) { Write-Host -ForegroundColor Green 'PostgreSQL: Connected' } else { Write-Host -ForegroundColor Red 'PostgreSQL: Connection failed' } } else { Write-Host -ForegroundColor Yellow 'PostgreSQL: Not running' }"

# ===================================================================
# CONTROL COMMANDS
# ===================================================================

.PHONY: stop
stop: ## Stop all containers
	@$(CYAN) "Stopping All Containers..."
	@powershell -Command "if (Test-Path 'docker-compose.dev.yml') { docker-compose -f docker-compose.dev.yml down | Out-Null }"
	@powershell -Command "if (Test-Path 'docker-compose.production.yml') { docker-compose -f docker-compose.production.yml down | Out-Null }"
	@docker-compose -f docker-compose.quick.yml down | Out-Null
	@$(GREEN) "All containers stopped!"

.PHONY: restart
restart: ## Restart all services
	@$(CYAN) "Restarting All Services..."
	@$(MAKE) stop
	@powershell -Command "Start-Sleep 5"
	@$(MAKE) quick
	@$(GREEN) "Services restarted!"

.PHONY: clean
clean: ## Clean up containers and volumes
	@$(RED) "Cleaning Up Containers and Volumes..."
	@powershell -Command "$$confirm = Read-Host 'This will remove all containers and volumes. Type YES to confirm'; if ($$confirm -eq 'YES') { docker-compose down -v --remove-orphans; docker system prune -f; Write-Host -ForegroundColor Green 'Cleanup completed!' } else { Write-Host -ForegroundColor Yellow 'Cleanup cancelled' }"

# ===================================================================
# UTILITY COMMANDS
# ===================================================================

.PHONY: health
health: ## Check application health
	@$(CYAN) "Checking Application Health..."
	@$(CYAN) "=================================="
	@echo ""
	@$(BLUE) "PostgreSQL Health:"
	@powershell -Command "if ((docker ps --format '{{.Names}}' | Select-String 'familyhub.*postgres').Count -gt 0) { Write-Host -ForegroundColor Green 'PostgreSQL: Running' } else { Write-Host -ForegroundColor Yellow 'PostgreSQL: Not running' }"
	@echo ""
	@$(BLUE) "Web Services:"
	@powershell -Command "try { $$response = Invoke-WebRequest -Uri 'http://localhost:5050' -TimeoutSec 5 -UseBasicParsing; Write-Host -ForegroundColor Green 'pgAdmin: Healthy (http://localhost:5050)' } catch { Write-Host -ForegroundColor Yellow 'pgAdmin: Not accessible' }"
	@powershell -Command "try { $$response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 5 -UseBasicParsing; Write-Host -ForegroundColor Green 'Django: Healthy (http://localhost:8000)' } catch { Write-Host -ForegroundColor Yellow 'Django: Not accessible' }"

.PHONY: setup
setup: ## Initial project setup
	@$(CYAN) "Setting Up FamilyHub Project..."
	@$(CYAN) "=================================="
	@$(BLUE) "Checking Prerequisites..."
	@powershell -Command "if (!(Get-Command docker -ErrorAction SilentlyContinue)) { Write-Host -ForegroundColor Red 'Docker not found. Please install Docker first.'; exit 1 }"
	@powershell -Command "if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) { Write-Host -ForegroundColor Red 'Docker Compose not found. Please install Docker Compose first.'; exit 1 }"
	@$(GREEN) "Prerequisites check passed!"
	@echo ""
	@$(BLUE) "Starting Quick PostgreSQL Environment..."
	@$(MAKE) quick
	@echo ""
	@$(BLUE) "Running Initial Migrations..."
	@$(MAKE) migrate
	@echo ""
	@$(GREEN) "FamilyHub setup completed!"
	@$(CYAN) "Access pgAdmin: http://localhost:5050"
	@$(CYAN) "PostgreSQL: localhost:5432"

.PHONY: update
update: ## Update dependencies
	@$(CYAN) "Updating Dependencies..."
	@$(MAKE) build
	@powershell -Command "if (Test-Path 'requirements/development.txt') { cd FamilyHub; pip install -r ../requirements/development.txt; Write-Host -ForegroundColor Green 'Dependencies updated!' }"

# ===================================================================
# DEVELOPMENT SHORTCUTS
# ===================================================================

.PHONY: quick-dev
quick-dev: quick migrate ## Quick development setup (PostgreSQL + migrations)
	@$(GREEN) "Quick development environment ready!"
	@$(BLUE) "pgAdmin: http://localhost:5050"
	@$(BLUE) "PostgreSQL: localhost:5432"
	@$(BLUE) "DATABASE_URL: postgresql://django:secretpass@localhost:5432/familyhub"

.PHONY: fresh-start
fresh-start: clean setup ## Fresh project start (clean + setup)
	@$(GREEN) "Fresh FamilyHub environment ready!"

.PHONY: dev-tools
dev-tools: ## Show development tools and URLs
	@$(CYAN) "FamilyHub Development Tools"
	@$(CYAN) "=============================="
	@echo ""
	@$(BLUE) "Web Interfaces:"
	@echo "  pgAdmin:      http://localhost:5050"
	@echo "  Django:       http://localhost:8000"
	@echo "  Production:   https://localhost"
	@echo ""
	@$(BLUE) "Database Connection:"
	@echo "  Host:         localhost"
	@echo "  Port:         5432"
	@echo "  Database:     familyhub"
	@echo "  Username:     django"
	@echo "  Password:     secretpass"
	@echo "  URL:          postgresql://django:secretpass@localhost:5432/familyhub"
	@echo ""
	@$(BLUE) "pgAdmin Access:"
	@echo "  Email:        admin@familyhub.local"
	@echo "  Password:     admin123"

# ===================================================================
# DOCUMENTATION
# ===================================================================

.PHONY: docs
docs: ## Show documentation links
	@$(CYAN) "FamilyHub Documentation"
	@$(CYAN) "=========================="
	@echo ""
	@$(BLUE) "Available Documentation:"
	@echo "  README.md                    - Main project documentation"
	@echo "  README.production.md         - Production deployment guide"
	@echo "  README.migration.md          - Database migration guide"
	@echo "  README.quick-postgres.md     - Quick PostgreSQL setup"
	@echo ""
	@$(BLUE) "Configuration Files:"
	@echo "  docker-compose.quick.yml     - Quick PostgreSQL setup"
	@echo "  docker-compose.dev.yml       - Development environment"
	@echo "  docker-compose.production.yml - Production environment"
	@echo "  .env.quick                   - Quick environment variables"

# ===================================================================
# TROUBLESHOOTING
# ===================================================================

.PHONY: troubleshoot
troubleshoot: ## Troubleshooting guide
	@$(CYAN) "FamilyHub Troubleshooting Guide"
	@$(CYAN) "=================================="
	@echo ""
	@$(BLUE) "Common Issues & Solutions:"
	@echo ""
	@$(YELLOW) "Port 5432 already in use:"
	@echo "   - Check: netstat -an | findstr :5432"
	@echo "   - Solution: Stop other PostgreSQL services"
	@echo "   - Alternative: Use different port in docker-compose"
	@echo ""
	@$(YELLOW) "Permission denied (Windows):"
	@echo "   - Run PowerShell as Administrator"
	@echo "   - Set-ExecutionPolicy RemoteSigned"
	@echo ""
	@$(YELLOW) "Docker not found:"
	@echo "   - Install Docker Desktop for Windows"
	@echo "   - Ensure Docker service is running"
	@echo ""
	@$(YELLOW) "Database connection failed:"
	@echo "   - Run: make restart"
	@echo "   - Check: make health"
	@echo "   - Reset: make reset-db"
	@echo ""
	@$(BLUE) "Diagnostic Commands:"
	@echo "  make status      - Check service status"
	@echo "  make health      - Check application health"
	@echo "  make logs        - View all logs"
	@echo "  make restart     - Restart all services"
