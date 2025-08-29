# 🚀 FamilyHub Development Workflow Makefile
# Author: FamilyHub Team
# Date: August 29, 2025
# Version: 1.0.0

# ===================================================================
# 🎯 QUICK REFERENCE
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
# 📋 HELP & INFORMATION
# ===================================================================

.PHONY: help
help: ## 📋 Show this help message
	@$(CYAN) "🚀 FamilyHub Development Workflow Commands"
	@$(CYAN) "=========================================="
	@echo ""
	@$(BLUE) "🚀 Quick Start:"
	@echo "  make quick         ⚡ Start quick PostgreSQL setup (5 minutes)"
	@echo "  make dev           🏗️  Start development environment"
	@echo "  make prod          🏭 Start production environment"
	@echo ""
	@$(BLUE) "🔧 Development:"
	@echo "  make build         🔨 Rebuild all containers"
	@echo "  make migrate       📊 Run Django migrations"
	@echo "  make shell         🐍 Open Django shell"
	@echo "  make dbshell       🐘 Open PostgreSQL shell"
	@echo "  make test          🧪 Run tests"
	@echo ""
	@$(BLUE) "📊 Database:"
	@echo "  make backup        💾 Backup database"
	@echo "  make restore       📥 Restore database from backup"
	@echo "  make reset-db      🗑️  Reset database (WARNING: Deletes all data)"
	@echo ""
	@$(BLUE) "🔍 Monitoring:"
	@echo "  make logs          📋 View all service logs"
	@echo "  make logs-django   📋 View Django logs only"
	@echo "  make logs-postgres 📋 View PostgreSQL logs only"
	@echo "  make status        📊 Show service status"
	@echo ""
	@$(BLUE) "🛑 Control:"
	@echo "  make stop          🛑 Stop all containers"
	@echo "  make restart       🔄 Restart all services"
	@echo "  make clean         🧹 Clean up containers and volumes"
	@echo ""
	@$(BLUE) "🔧 Utilities:"
	@echo "  make health        💚 Check application health"
	@echo "  make setup         🎯 Initial project setup"
	@echo "  make update        📦 Update dependencies"

# ===================================================================
# 🚀 ENVIRONMENT STARTUP
# ===================================================================

.PHONY: quick
quick: ## ⚡ Start quick PostgreSQL setup (5 minutes)
	@$(CYAN) "⚡ Starting Quick PostgreSQL Environment..."
	@if (Test-Path "quick-postgres-setup.ps1") { \
		.\quick-postgres-setup.ps1; \
	} else { \
		$(COMPOSE_QUICK) up -d; \
		timeout 10; \
		$(GREEN) "✅ Quick PostgreSQL environment started!"; \
		$(BLUE) "🌐 pgAdmin: http://localhost:5050"; \
		$(BLUE) "🐘 PostgreSQL: localhost:5432"; \
	}

.PHONY: dev
dev: ## 🏗️ Start development environment
	@$(CYAN) "🏗️ Starting Development Environment..."
	@if (Test-Path "docker-compose.dev.yml") { \
		$(COMPOSE_DEV) up -d; \
		timeout 15; \
		$(GREEN) "✅ Development environment started!"; \
		$(BLUE) "🌐 Django: http://localhost:8000"; \
		$(BLUE) "📊 pgAdmin: http://localhost:5050"; \
	} else { \
		$(RED) "❌ docker-compose.dev.yml not found"; \
		$(YELLOW) "💡 Use 'make quick' for immediate PostgreSQL setup"; \
	}

.PHONY: prod
prod: ## 🏭 Start production environment
	@$(CYAN) "🏭 Starting Production Environment..."
	@if (Test-Path "docker-compose.production.yml") { \
		$(COMPOSE_PROD) up -d; \
		timeout 30; \
		$(GREEN) "✅ Production environment started!"; \
		$(BLUE) "🌐 Application: https://localhost"; \
		$(BLUE) "📊 Monitoring: Check 'make logs' for status"; \
	} else { \
		$(RED) "❌ docker-compose.production.yml not found"; \
		$(YELLOW) "💡 Use 'make quick' for immediate PostgreSQL setup"; \
	}

# ===================================================================
# 🔧 DEVELOPMENT COMMANDS
# ===================================================================

.PHONY: build
build: ## 🔨 Rebuild all containers
	@$(CYAN) "🔨 Rebuilding All Containers..."
	@if (Test-Path "docker-compose.dev.yml") { \
		$(COMPOSE_DEV) build --no-cache; \
		$(GREEN) "✅ Development containers rebuilt!"; \
	}
	@if (Test-Path "docker-compose.production.yml") { \
		$(COMPOSE_PROD) build --no-cache; \
		$(GREEN) "✅ Production containers rebuilt!"; \
	}
	@$(COMPOSE_QUICK) build --no-cache
	@$(GREEN) "✅ All containers rebuilt successfully!"

.PHONY: migrate
migrate: ## 📊 Run Django migrations
	@$(CYAN) "📊 Running Django Migrations..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*django").Count -gt 0) { \
		docker-compose exec $(DJANGO_SERVICE) python manage.py makemigrations; \
		docker-compose exec $(DJANGO_SERVICE) python manage.py migrate; \
		$(GREEN) "✅ Migrations completed!"; \
	} else { \
		$(YELLOW) "⚠️  Django container not running. Starting quick environment..."; \
		$(MAKE) quick; \
		timeout 10; \
		cd FamilyHub; \
		python manage.py makemigrations; \
		python manage.py migrate; \
		$(GREEN) "✅ Migrations completed locally!"; \
	}

.PHONY: shell
shell: ## 🐍 Open Django shell
	@$(CYAN) "🐍 Opening Django Shell..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*django").Count -gt 0) { \
		docker-compose exec $(DJANGO_SERVICE) python manage.py shell; \
	} else { \
		$(YELLOW) "⚠️  Django container not running. Using local environment..."; \
		cd FamilyHub; \
		python manage.py shell; \
	}

.PHONY: dbshell
dbshell: ## 🐘 Open PostgreSQL shell
	@$(CYAN) "🐘 Opening PostgreSQL Shell..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
		$(COMPOSE_QUICK) exec $(POSTGRES_SERVICE) psql -U django -d familyhub; \
	} else { \
		$(YELLOW) "⚠️  PostgreSQL container not running. Starting quick environment..."; \
		$(MAKE) quick; \
		timeout 10; \
		$(COMPOSE_QUICK) exec $(POSTGRES_SERVICE) psql -U django -d familyhub; \
	}

.PHONY: test
test: ## 🧪 Run tests
	@$(CYAN) "🧪 Running Tests..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*django").Count -gt 0) { \
		docker-compose exec $(DJANGO_SERVICE) python manage.py test; \
	} else { \
		$(YELLOW) "⚠️  Django container not running. Running tests locally..."; \
		cd FamilyHub; \
		python manage.py test; \
	}
	@$(GREEN) "✅ Tests completed!"

# ===================================================================
# 📊 DATABASE MANAGEMENT
# ===================================================================

.PHONY: backup
backup: ## 💾 Backup database
	@$(CYAN) "💾 Creating Database Backup..."
	@if (!(Test-Path "$(BACKUP_DIR)")) { New-Item -ItemType Directory -Path "$(BACKUP_DIR)" | Out-Null }
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
		docker-compose exec -T $(POSTGRES_SERVICE) pg_dump -U django -d familyhub > "$(BACKUP_DIR)/backup_$(TIMESTAMP).sql"; \
		$(GREEN) "✅ Database backup created: $(BACKUP_DIR)/backup_$(TIMESTAMP).sql"; \
	} else { \
		$(RED) "❌ PostgreSQL container not running"; \
		$(YELLOW) "💡 Start environment first: make quick"; \
	}

.PHONY: restore
restore: ## 📥 Restore database from backup
	@$(CYAN) "📥 Restoring Database from Backup..."
	@if (!(Test-Path "$(BACKUP_DIR)")) { \
		$(RED) "❌ Backup directory not found"; \
		exit 1; \
	}
	@$$latest = Get-ChildItem "$(BACKUP_DIR)" -Filter "*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
	@if ($$latest) { \
		$(YELLOW) "📂 Using latest backup: $$($latest.Name)"; \
		if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
			Get-Content "$(BACKUP_DIR)/$$($latest.Name)" | docker-compose exec -T $(POSTGRES_SERVICE) psql -U django -d familyhub; \
			$(GREEN) "✅ Database restored from: $$($latest.Name)"; \
		} else { \
			$(RED) "❌ PostgreSQL container not running"; \
		} \
	} else { \
		$(RED) "❌ No backup files found in $(BACKUP_DIR)"; \
	}

.PHONY: reset-db
reset-db: ## 🗑️ Reset database (WARNING: Deletes all data)
	@$(RED) "⚠️  WARNING: This will delete ALL database data!"
	@$$confirm = Read-Host "Type 'YES' to confirm database reset"
	@if ($$confirm -eq "YES") { \
		$(CYAN) "🗑️  Resetting Database..."; \
		$(COMPOSE_QUICK) down -v; \
		$(COMPOSE_QUICK) up -d; \
		timeout 15; \
		$(MAKE) migrate; \
		$(GREEN) "✅ Database reset completed!"; \
	} else { \
		$(YELLOW) "❌ Database reset cancelled"; \
	}

# ===================================================================
# 🔍 MONITORING & LOGS
# ===================================================================

.PHONY: logs
logs: ## 📋 View all service logs
	@$(CYAN) "📋 Viewing All Service Logs..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME)").Count -gt 0) { \
		docker-compose logs -f; \
	} else { \
		$(YELLOW) "⚠️  No containers running"; \
		$(BLUE) "💡 Start environment: make quick | make dev | make prod"; \
	}

.PHONY: logs-django
logs-django: ## 📋 View Django logs only
	@$(CYAN) "📋 Viewing Django Logs..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*django").Count -gt 0) { \
		docker-compose logs -f $(DJANGO_SERVICE); \
	} else { \
		$(YELLOW) "⚠️  Django container not running"; \
	}

.PHONY: logs-postgres
logs-postgres: ## 📋 View PostgreSQL logs only
	@$(CYAN) "📋 Viewing PostgreSQL Logs..."
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
		$(COMPOSE_QUICK) logs -f $(POSTGRES_SERVICE); \
	} else { \
		$(YELLOW) "⚠️  PostgreSQL container not running"; \
	}

.PHONY: status
status: ## 📊 Show service status
	@$(CYAN) "📊 Service Status:"
	@$(CYAN) "=================="
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=$(PROJECT_NAME)"
	@echo ""
	@$(BLUE) "🐘 PostgreSQL Connection Test:"
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
		if ($(COMPOSE_QUICK) exec -T $(POSTGRES_SERVICE) pg_isready -U django -d familyhub) { \
			$(GREEN) "✅ PostgreSQL: Connected"; \
		} else { \
			$(RED) "❌ PostgreSQL: Connection failed"; \
		} \
	} else { \
		$(YELLOW) "⚠️  PostgreSQL: Not running"; \
	}

# ===================================================================
# 🛑 CONTROL COMMANDS
# ===================================================================

.PHONY: stop
stop: ## 🛑 Stop all containers
	@$(CYAN) "🛑 Stopping All Containers..."
	@if (Test-Path "docker-compose.dev.yml") { $(COMPOSE_DEV) down | Out-Null }
	@if (Test-Path "docker-compose.production.yml") { $(COMPOSE_PROD) down | Out-Null }
	@$(COMPOSE_QUICK) down | Out-Null
	@$(GREEN) "✅ All containers stopped!"

.PHONY: restart
restart: ## 🔄 Restart all services
	@$(CYAN) "🔄 Restarting All Services..."
	@$(MAKE) stop
	@timeout 5
	@$(MAKE) quick
	@$(GREEN) "✅ Services restarted!"

.PHONY: clean
clean: ## 🧹 Clean up containers and volumes
	@$(RED) "🧹 Cleaning Up Containers and Volumes..."
	@$$confirm = Read-Host "This will remove all containers and volumes. Type 'YES' to confirm"
	@if ($$confirm -eq "YES") { \
		docker-compose down -v --remove-orphans; \
		docker system prune -f; \
		$(GREEN) "✅ Cleanup completed!"; \
	} else { \
		$(YELLOW) "❌ Cleanup cancelled"; \
	}

# ===================================================================
# 🔧 UTILITY COMMANDS
# ===================================================================

.PHONY: health
health: ## 💚 Check application health
	@$(CYAN) "💚 Checking Application Health..."
	@$(CYAN) "=================================="
	@echo ""
	@$(BLUE) "🐘 PostgreSQL Health:"
	@if ((docker ps --format "{{.Names}}" | Select-String "$(PROJECT_NAME).*postgres").Count -gt 0) { \
		if ($(COMPOSE_QUICK) exec -T $(POSTGRES_SERVICE) pg_isready -U django -d familyhub) { \
			$(GREEN) "✅ PostgreSQL: Healthy"; \
		} else { \
			$(RED) "❌ PostgreSQL: Unhealthy"; \
		} \
	} else { \
		$(YELLOW) "⚠️  PostgreSQL: Not running"; \
	}
	@echo ""
	@$(BLUE) "🌐 Web Services:"
	@try { \
		$$response = Invoke-WebRequest -Uri "http://localhost:5050" -TimeoutSec 5 -UseBasicParsing; \
		$(GREEN) "✅ pgAdmin: Healthy (http://localhost:5050)"; \
	} catch { \
		$(YELLOW) "⚠️  pgAdmin: Not accessible"; \
	}
	@try { \
		$$response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -UseBasicParsing; \
		$(GREEN) "✅ Django: Healthy (http://localhost:8000)"; \
	} catch { \
		$(YELLOW) "⚠️  Django: Not accessible"; \
	}

.PHONY: setup
setup: ## 🎯 Initial project setup
	@$(CYAN) "🎯 Setting Up FamilyHub Project..."
	@$(CYAN) "=================================="
	@$(BLUE) "📋 Checking Prerequisites..."
	@if (!(Get-Command docker -ErrorAction SilentlyContinue)) { \
		$(RED) "❌ Docker not found. Please install Docker first."; \
		exit 1; \
	}
	@if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) { \
		$(RED) "❌ Docker Compose not found. Please install Docker Compose first."; \
		exit 1; \
	}
	@$(GREEN) "✅ Prerequisites check passed!"
	@echo ""
	@$(BLUE) "🚀 Starting Quick PostgreSQL Environment..."
	@$(MAKE) quick
	@echo ""
	@$(BLUE) "📊 Running Initial Migrations..."
	@$(MAKE) migrate
	@echo ""
	@$(GREEN) "🎉 FamilyHub setup completed!"
	@$(CYAN) "🌐 Access pgAdmin: http://localhost:5050"
	@$(CYAN) "🐘 PostgreSQL: localhost:5432"

.PHONY: update
update: ## 📦 Update dependencies
	@$(CYAN) "📦 Updating Dependencies..."
	@$(MAKE) build
	@if (Test-Path "requirements/development.txt") { \
		cd FamilyHub; \
		pip install -r ../requirements/development.txt; \
		$(GREEN) "✅ Dependencies updated!"; \
	}

# ===================================================================
# 🎯 DEVELOPMENT SHORTCUTS
# ===================================================================

.PHONY: quick-dev
quick-dev: quick migrate ## ⚡ Quick development setup (PostgreSQL + migrations)
	@$(GREEN) "🎉 Quick development environment ready!"
	@$(BLUE) "🌐 pgAdmin: http://localhost:5050"
	@$(BLUE) "🐘 PostgreSQL: localhost:5432"
	@$(BLUE) "🔗 DATABASE_URL: postgresql://django:secretpass@localhost:5432/familyhub"

.PHONY: fresh-start
fresh-start: clean setup ## 🔄 Fresh project start (clean + setup)
	@$(GREEN) "🎉 Fresh FamilyHub environment ready!"

.PHONY: dev-tools
dev-tools: ## 🛠️ Show development tools and URLs
	@$(CYAN) "🛠️  FamilyHub Development Tools"
	@$(CYAN) "=============================="
	@echo ""
	@$(BLUE) "🌐 Web Interfaces:"
	@echo "  pgAdmin:      http://localhost:5050"
	@echo "  Django:       http://localhost:8000"
	@echo "  Production:   https://localhost"
	@echo ""
	@$(BLUE) "🔗 Database Connection:"
	@echo "  Host:         localhost"
	@echo "  Port:         5432"
	@echo "  Database:     familyhub"
	@echo "  Username:     django"
	@echo "  Password:     secretpass"
	@echo "  URL:          postgresql://django:secretpass@localhost:5432/familyhub"
	@echo ""
	@$(BLUE) "🐘 pgAdmin Access:"
	@echo "  Email:        admin@familyhub.local"
	@echo "  Password:     admin123"

# ===================================================================
# 📚 DOCUMENTATION
# ===================================================================

.PHONY: docs
docs: ## 📚 Show documentation links
	@$(CYAN) "📚 FamilyHub Documentation"
	@$(CYAN) "=========================="
	@echo ""
	@$(BLUE) "📖 Available Documentation:"
	@echo "  README.md                    - Main project documentation"
	@echo "  README.production.md         - Production deployment guide"
	@echo "  README.migration.md          - Database migration guide"
	@echo "  README.quick-postgres.md     - Quick PostgreSQL setup"
	@echo ""
	@$(BLUE) "🔧 Configuration Files:"
	@echo "  docker-compose.quick.yml     - Quick PostgreSQL setup"
	@echo "  docker-compose.dev.yml       - Development environment"
	@echo "  docker-compose.production.yml - Production environment"
	@echo "  .env.quick                   - Quick environment variables"

# ===================================================================
# 🔍 TROUBLESHOOTING
# ===================================================================

.PHONY: troubleshoot
troubleshoot: ## 🔍 Troubleshooting guide
	@$(CYAN) "🔍 FamilyHub Troubleshooting Guide"
	@$(CYAN) "=================================="
	@echo ""
	@$(BLUE) "🚨 Common Issues & Solutions:"
	@echo ""
	@$(YELLOW) "❓ Port 5432 already in use:"
	@echo "   • Check: netstat -an | findstr :5432"
	@echo "   • Solution: Stop other PostgreSQL services"
	@echo "   • Alternative: Use different port in docker-compose"
	@echo ""
	@$(YELLOW) "❓ Permission denied (Windows):"
	@echo "   • Run PowerShell as Administrator"
	@echo "   • Set-ExecutionPolicy RemoteSigned"
	@echo ""
	@$(YELLOW) "❓ Docker not found:"
	@echo "   • Install Docker Desktop for Windows"
	@echo "   • Ensure Docker service is running"
	@echo ""
	@$(YELLOW) "❓ Database connection failed:"
	@echo "   • Run: make restart"
	@echo "   • Check: make health"
	@echo "   • Reset: make reset-db"
	@echo ""
	@$(BLUE) "🛠️  Diagnostic Commands:"
	@echo "  make status      - Check service status"
	@echo "  make health      - Check application health"
	@echo "  make logs        - View all logs"
	@echo "  make restart     - Restart all services"
