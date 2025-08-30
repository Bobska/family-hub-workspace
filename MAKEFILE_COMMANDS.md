# 📋 FamilyHub Makefile Commands Reference

## 🚀 Complete Operations Management System

This document provides a comprehensive reference for all available Makefile commands in the FamilyHub project, organized by category with detailed descriptions and usage examples.

---

## 🔧 Environment Setup Commands

### `make setup`
**Purpose**: Initial project setup (first-time use)  
**Description**: Sets up FamilyHub environment, creates `.env` from template, builds Docker containers  
**Usage**: 
```bash
make setup
```
**What it does**:
- Creates `.env` file from `.env.docker` template if it doesn't exist
- Builds Docker containers from scratch
- Prepares development environment for first use

---

## 🖥️ Development Commands

### `make dev-local`
**Purpose**: Run Django development server locally (without Docker)  
**Description**: Starts Django development server on local machine without Docker containers  
**Usage**: 
```bash
make dev-local
```
**Requirements**: Local Python environment, PostgreSQL installed locally

### `make dev-docker`
**Purpose**: Start Docker development environment  
**Description**: Starts complete Docker development environment with all services  
**Usage**: 
```bash
make dev-docker
```
**Services started**: Django web server, PostgreSQL database

### `make dev-detached`
**Purpose**: Start Docker development environment in background  
**Description**: Starts Docker development environment in detached mode  
**Usage**: 
```bash
make dev-detached
```
**Result**: Services run in background, terminal remains available

### `make build`
**Purpose**: Build Docker containers (no cache)  
**Description**: Builds Docker containers from scratch without using cache  
**Usage**: 
```bash
make build
```
**When to use**: After dependency changes, Dockerfile modifications

### `make rebuild`
**Purpose**: Rebuild and restart all services  
**Description**: Complete rebuild workflow - stops, rebuilds, and restarts all services  
**Usage**: 
```bash
make rebuild
```
**What it does**:
1. Stops all running containers
2. Rebuilds containers without cache
3. Starts containers in detached mode
4. Shows service status

---

## 🗄️ Database Commands

### `make migrate`
**Purpose**: Apply database migrations  
**Description**: Runs Django database migrations in web container  
**Usage**: 
```bash
make migrate
```
**When to use**: After model changes, initial setup, pulling migration updates

### `make makemigrations`
**Purpose**: Create new database migrations  
**Description**: Creates Django migration files for model changes  
**Usage**: 
```bash
make makemigrations
```
**When to use**: After modifying Django models

### `make dbshell`
**Purpose**: Open database shell (PostgreSQL)  
**Description**: Opens interactive PostgreSQL shell for direct database access  
**Usage**: 
```bash
make dbshell
```
**Access**: Direct SQL commands, database inspection

### `make reset-db`
**Purpose**: Reset database (WARNING: destroys all data)  
**Description**: Completely resets database with confirmation prompt  
**Usage**: 
```bash
make reset-db
```
**⚠️ Warning**: This destroys all database data!  
**What it does**:
1. Prompts for confirmation
2. Stops services and removes volumes
3. Recreates database
4. Runs migrations
5. Creates superuser

### `make init-superuser`
**Purpose**: Create superuser account  
**Description**: Creates Django admin superuser using environment variables  
**Usage**: 
```bash
make init-superuser
```
**Credentials**: Uses values from `.env` file

---

## 🚀 Production Commands

### `make prod-build`
**Purpose**: Build production containers  
**Description**: Builds production-optimized Docker containers  
**Usage**: 
```bash
make prod-build
```
**Configuration**: Uses `docker-compose.prod.yml`

### `make prod-up`
**Purpose**: Start production environment  
**Description**: Starts production environment with all services  
**Usage**: 
```bash
make prod-up
```
**Requirements**: `.env.prod` file must exist  
**Services**: Django (Gunicorn), PostgreSQL, Redis, Nginx

### `make prod-down`
**Purpose**: Stop production environment  
**Description**: Stops all production services  
**Usage**: 
```bash
make prod-down
```

### `make prod-logs`
**Purpose**: View production logs  
**Description**: Shows production service logs in follow mode  
**Usage**: 
```bash
make prod-logs
```

### `make prod-status`
**Purpose**: Check production service status  
**Description**: Shows status of all production services and health checks  
**Usage**: 
```bash
make prod-status
```

### `make prod-deploy`
**Purpose**: Full production deployment  
**Description**: Complete production deployment workflow  
**Usage**: 
```bash
make prod-deploy
```
**What it does**:
1. Builds production containers
2. Starts production environment
3. Waits for services to be ready
4. Confirms deployment success

---

## 💾 Backup & Restore Commands

### `make backup`
**Purpose**: Create database backup  
**Description**: Creates timestamped database backup  
**Usage**: 
```bash
make backup
```
**Output**: `backups/backup_YYYYMMDD_HHMMSS.sql`

### `make backup-prod`
**Purpose**: Create production database backup  
**Description**: Creates timestamped backup of production database  
**Usage**: 
```bash
make backup-prod
```
**Output**: `backups/backup_prod_YYYYMMDD_HHMMSS.sql`

### `make restore`
**Purpose**: Restore database from backup  
**Description**: Restores database from specified backup file  
**Usage**: 
```bash
make restore BACKUP_FILE=backups/backup_file.sql
```
**Parameter**: `BACKUP_FILE` - path to backup file

### `make list-backups`
**Purpose**: List all available backups  
**Description**: Shows all backup files in backups directory  
**Usage**: 
```bash
make list-backups
```

---

## 🧪 Testing & Quality Assurance Commands

### `make test`
**Purpose**: Run test suite  
**Description**: Runs Django test suite in web container  
**Usage**: 
```bash
make test
```

### `make check`
**Purpose**: Run Django system checks  
**Description**: Validates Django configuration and setup  
**Usage**: 
```bash
make check
```

### `make check-deploy`
**Purpose**: Run Django deployment checks  
**Description**: Validates production readiness and deployment configuration  
**Usage**: 
```bash
make check-deploy
```

---

## 🔧 Utility Commands

### `make shell`
**Purpose**: Open Django shell  
**Description**: Opens interactive Django shell in web container  
**Usage**: 
```bash
make shell
```

### `make collectstatic`
**Purpose**: Collect static files  
**Description**: Collects static files for production serving  
**Usage**: 
```bash
make collectstatic
```

### `make logs`
**Purpose**: View development logs (follow mode)  
**Description**: Shows logs from all development services  
**Usage**: 
```bash
make logs
```

### `make logs-web`
**Purpose**: View web service logs only  
**Description**: Shows logs from Django web service only  
**Usage**: 
```bash
make logs-web
```

### `make logs-db`
**Purpose**: View database logs only  
**Description**: Shows logs from PostgreSQL database service only  
**Usage**: 
```bash
make logs-db
```

### `make status`
**Purpose**: Show service status  
**Description**: Displays status of all running Docker services  
**Usage**: 
```bash
make status
```

### `make health`
**Purpose**: Check application health  
**Description**: Tests application health endpoints  
**Usage**: 
```bash
make health
```
**Tests**:
- Health endpoint: `http://localhost:8000/health/`
- Main page: `http://localhost:8000/`

---

## 🧹 Maintenance Commands

### `make stop`
**Purpose**: Stop all services  
**Description**: Stops all running Docker services  
**Usage**: 
```bash
make stop
```

### `make restart`
**Purpose**: Restart all services  
**Description**: Restarts all Docker services without rebuilding  
**Usage**: 
```bash
make restart
```

### `make restart-web`
**Purpose**: Restart web service only  
**Description**: Restarts only the Django web service  
**Usage**: 
```bash
make restart-web
```

### `make clean`
**Purpose**: Stop services and clean Docker resources  
**Description**: Stops services and removes unused Docker resources  
**Usage**: 
```bash
make clean
```

### `make clean-all`
**Purpose**: Remove all containers, volumes, and images (DESTRUCTIVE)  
**Description**: Complete Docker cleanup - removes everything  
**Usage**: 
```bash
make clean-all
```
**⚠️ Warning**: This removes ALL Docker resources!

---

## ℹ️ Information Commands

### `make info`
**Purpose**: Show project information  
**Description**: Displays project details, configuration, and status  
**Usage**: 
```bash
make info
```
**Shows**:
- Project details
- Current branch
- Environment file status
- Docker availability

### `make urls`
**Purpose**: Show application URLs  
**Description**: Lists all application URLs for development and production  
**Usage**: 
```bash
make urls
```
**URLs shown**:
- Development: `http://localhost:8000`
- Admin: `http://localhost:8000/admin/`
- Health: `http://localhost:8000/health/`
- Timesheet: `http://localhost:8000/timesheet/`

### `make version`
**Purpose**: Show version information  
**Description**: Displays version information for all system components  
**Usage**: 
```bash
make version
```
**Shows versions for**:
- Python
- Django
- PostgreSQL
- Git
- Docker
- Docker Compose

### `make help`
**Purpose**: Show help message with all available commands  
**Description**: Displays comprehensive help with all commands organized by category  
**Usage**: 
```bash
make help
```

---

## 🚀 Development Workflow Shortcuts

### `make fresh-start`
**Purpose**: Complete fresh start (build, migrate, create superuser)  
**Description**: Complete development environment setup from scratch  
**Usage**: 
```bash
make fresh-start
```
**What it does**:
1. Stops all services
2. Builds containers
3. Starts in detached mode
4. Runs migrations
5. Creates superuser
6. Shows status

### `make quick-restart`
**Purpose**: Quick restart without rebuild  
**Description**: Fast restart of all services without rebuilding  
**Usage**: 
```bash
make quick-restart
```

### `make deploy-dev`
**Purpose**: Deploy development environment  
**Description**: Complete development deployment workflow  
**Usage**: 
```bash
make deploy-dev
```
**What it does**:
1. Builds containers
2. Starts in detached mode
3. Runs migrations
4. Collects static files
5. Shows status

---

## 📝 Usage Examples

### First-Time Setup
```bash
# Initial project setup
make setup

# Start development environment
make dev-docker

# Access the application
# http://localhost:8000
```

### Daily Development Workflow
```bash
# Start development
make dev-detached

# Apply any new migrations
make migrate

# View logs
make logs

# Run tests
make test

# Stop when done
make stop
```

### Database Operations
```bash
# Create migrations after model changes
make makemigrations

# Apply migrations
make migrate

# Access database directly
make dbshell

# Create backup
make backup

# Reset database (if needed)
make reset-db
```

### Production Deployment
```bash
# Build production containers
make prod-build

# Deploy to production
make prod-deploy

# Check status
make prod-status

# View logs
make prod-logs
```

### Troubleshooting
```bash
# Check service status
make status

# Test application health
make health

# View logs
make logs

# Complete cleanup and rebuild
make clean
make build
```

---

## 🔧 Environment Files Reference

- **`.env`** - Your environment (copy from `.env.docker` or `.env.local`)
- **`.env.docker`** - Docker development template
- **`.env.local`** - Local development template  
- **`.env.prod`** - Production environment (copy from `.env.prod.example`)

---

## 🚀 Quick Start Commands

```bash
# 1. Initial setup
make setup

# 2. Start development
make dev-docker

# 3. Open application
# http://localhost:8000
```

---

## 📋 Troubleshooting Commands

```bash
# View application logs
make logs

# Check service status
make status

# Test application health
make health

# Complete rebuild
make clean && make build
```

---

**Last Updated**: August 31, 2025  
**Total Commands**: 40+  
**Categories**: 8 main categories covering complete project lifecycle
