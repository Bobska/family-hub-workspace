# FamilyHub Production Makefile
# Convenient commands for Docker development and deployment

.PHONY: help dev prod build migrate test clean logs shell backup restore

# Default target
help:
	@echo "FamilyHub Docker Commands:"
	@echo "  make dev        - Start development environment"
	@echo "  make prod       - Start production environment"
	@echo "  make build      - Build all Docker images"
	@echo "  make migrate    - Run database migrations"
	@echo "  make test       - Run tests in Docker"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make logs       - View application logs"
	@echo "  make shell      - Open Django shell in container"
	@echo "  make backup     - Create database backup"
	@echo "  make restore    - Restore database from backup"
	@echo "  make setup      - Initial setup (copy env, build, migrate)"

# Development environment
dev:
	@echo "Starting FamilyHub development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev-d:
	@echo "Starting FamilyHub development environment in background..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# Production environment  
prod:
	@echo "Starting FamilyHub production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build

prod-d:
	@echo "Starting FamilyHub production environment in background..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Build all images
build:
	@echo "Building all Docker images..."
	docker-compose build --no-cache

build-dev:
	@echo "Building development images..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache

build-prod:
	@echo "Building production images..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

# Database migrations
migrate:
	@echo "Running database migrations..."
	docker-compose exec web python manage.py migrate

migrate-dev:
	@echo "Running database migrations in development..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

makemigrations:
	@echo "Creating new migrations..."
	docker-compose exec web python manage.py makemigrations

# Testing
test:
	@echo "Running tests in Docker..."
	docker-compose exec web python manage.py test

test-coverage:
	@echo "Running tests with coverage..."
	docker-compose exec web coverage run --source='.' manage.py test
	docker-compose exec web coverage report

# Utility commands
shell:
	@echo "Opening Django shell..."
	docker-compose exec web python manage.py shell

dbshell:
	@echo "Opening database shell..."
	docker-compose exec web python manage.py dbshell

logs:
	@echo "Viewing application logs..."
	docker-compose logs -f web

logs-all:
	@echo "Viewing all container logs..."
	docker-compose logs -f

# Cleanup
clean:
	@echo "Stopping and removing containers..."
	docker-compose down
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

clean-all:
	@echo "Removing containers, volumes, and images..."
	docker-compose down -v --rmi all
	docker system prune -f

# Backup and restore
backup:
	@echo "Creating database backup..."
	docker-compose exec postgres pg_dump -U familyhub_user familyhub > ./backups/familyhub_backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@echo "Restoring database from backup..."
	@read -p "Enter backup filename: " filename; \
	docker-compose exec -T postgres psql -U familyhub_user familyhub < ./backups/$$filename

# Initial setup
setup:
	@echo "Setting up FamilyHub for the first time..."
	@if [ ! -f .env ]; then \
		echo "Copying .env.example to .env..."; \
		cp .env.example .env; \
		echo "Please edit .env file with your settings"; \
	fi
	@echo "Building and starting development environment..."
	make build-dev
	@echo "Running initial migrations..."
	make migrate-dev
	@echo "Creating superuser..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Stop services
stop:
	@echo "Stopping all services..."
	docker-compose stop

stop-dev:
	@echo "Stopping development services..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml stop

stop-prod:
	@echo "Stopping production services..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml stop

# Restart services
restart:
	@echo "Restarting services..."
	docker-compose restart

restart-web:
	@echo "Restarting web service..."
	docker-compose restart web

# Check service status
status:
	@echo "Service status:"
	docker-compose ps

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	docker-compose exec web python manage.py collectstatic --noinput
