# 🚀 FamilyHub Production Environment - Complete Setup Guide

Welcome to FamilyHub's production-ready environment! This repository contains a fully configured Django application with enterprise-grade infrastructure, instant development setup, and comprehensive migration tools.

## 🎯 Quick Start Options

### ⚡ Instant Development (5 minutes)
```powershell
# Option 1: PowerShell Script (Windows)
.\quick-postgres-setup.ps1

# Option 2: Manual Docker Compose
docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d
```

### 🏗️ Full Production Stack
```bash
# Production environment with Nginx, SSL, Redis, Celery
docker-compose -f docker-compose.production.yml up -d
```

### 🔄 SQL Server Migration
```bash
# Migrate existing data from SQL Server to PostgreSQL
python manage.py export_from_sqlserver
python manage.py import_from_sqlserver  
python manage.py verify_migration
```

---

## 📁 Project Architecture

```
FamilyHub/
├── 🚀 Quick Setup
│   ├── docker-compose.quick.yml      # 5-minute PostgreSQL + pgAdmin
│   ├── .env.quick                    # Development environment
│   ├── quick-postgres-setup.ps1      # Windows setup script
│   └── quick-postgres-setup.sh       # Linux/Mac setup script
│
├── 🏭 Production Environment  
│   ├── docker-compose.production.yml # Complete production stack
│   ├── docker-compose.dev.yml        # Development with hot reload
│   ├── nginx/                        # Reverse proxy with SSL
│   └── .env.production               # Production configuration
│
├── 🔄 Database Migration
│   ├── management/commands/           # SQL Server migration tools
│   ├── config/migration_config.json  # Migration mapping
│   └── requirements/migration.txt    # Migration dependencies
│
├── 🏠 FamilyHub Applications
│   ├── home/                         # Dashboard and main app
│   ├── apps/timesheet/              # Time tracking (active)
│   ├── apps/daycare_invoice/        # Invoice management
│   ├── apps/employment_history/     # Employment tracking
│   ├── apps/upcoming_payments/      # Payment scheduling
│   ├── apps/credit_card_mgmt/       # Credit card management
│   └── apps/household_budget/       # Budget planning
│
└── 📚 Documentation
    ├── README.production.md          # Production deployment guide  
    ├── README.migration.md           # Database migration guide
    └── README.quick-postgres.md      # Quick setup documentation
```

---

## 🎯 Environment Options

| Environment | Purpose | Setup Time | Use Case |
|-------------|---------|------------|----------|
| **Quick** | Instant PostgreSQL development | 5 minutes | Daily development, testing |
| **Development** | Full development stack | 10 minutes | Feature development, debugging |
| **Production** | Enterprise production | 30 minutes | Staging, production deployment |

### ⚡ Quick Environment (Recommended for Development)
```yaml
Services: PostgreSQL 17.6 + pgAdmin + Redis (optional)
Access: pgAdmin at http://localhost:5050
Database: postgresql://django:secretpass@localhost:5432/familyhub
```

### 🏗️ Development Environment  
```yaml
Services: Django + PostgreSQL + Redis + Hot Reload
Access: Django at http://localhost:8000
Features: Live code reloading, debug toolbar, development settings
```

### 🏭 Production Environment
```yaml
Services: Nginx + Django + PostgreSQL + Redis + Celery + Backup
Access: https://localhost (SSL enabled)
Features: SSL, rate limiting, monitoring, automated backups
```

---

## 🚀 Getting Started

### Prerequisites
- **Docker**: 24.0+ with Docker Compose
- **Python**: 3.10+ (for local development)  
- **Git**: For version control
- **Windows PowerShell** or **Bash** (for setup scripts)

### 1. ⚡ Quick PostgreSQL Setup (Recommended First Step)

For immediate database access and development:

```powershell
# Windows (PowerShell)
.\quick-postgres-setup.ps1
```

```bash
# Linux/Mac
chmod +x quick-postgres-setup.sh
./quick-postgres-setup.sh
```

**What you get:**
- PostgreSQL 17.6 running on `localhost:5432`
- pgAdmin web interface at `http://localhost:5050`
- Pre-configured database connection
- Ready-to-use Django DATABASE_URL

### 2. 🏗️ Development Environment

For full Django development with hot reload:

```bash
# Start development stack
docker-compose -f docker-compose.dev.yml up -d

# Access Django
http://localhost:8000

# View logs
docker-compose -f docker-compose.dev.yml logs -f django
```

### 3. 🏭 Production Environment

For production-grade deployment:

```bash
# Start production stack
docker-compose -f docker-compose.production.yml up -d

# Access application (HTTPS)
https://localhost

# Monitor services
docker-compose -f docker-compose.production.yml ps
```
docker-compose -f docker-compose.dev.yml up -d

# Access Django
http://localhost:8000

# View logs
docker-compose -f docker-compose.dev.yml logs -f django
```

### 3. 🏭 Production Environment

For production-grade deployment:

```bash
# Start production stack
docker-compose -f docker-compose.production.yml up -d

# Access application (HTTPS)
https://localhost

# Monitor services
docker-compose -f docker-compose.production.yml ps
```

---

## 🔄 Database Migration from SQL Server

If you have existing data in SQL Server:

### Setup Migration Environment
```bash
# Install migration dependencies
pip install -r requirements/migration.txt

# Configure connection in config/migration_config.json
```

### Run Migration
```bash
# Export from SQL Server
python manage.py export_from_sqlserver

# Import to PostgreSQL  
python manage.py import_from_sqlserver

# Verify data integrity
python manage.py verify_migration
```

**Migration Features:**
- ✅ Automatic data type conversion
- ✅ Batch processing for large datasets
- ✅ Foreign key relationship preservation  
- ✅ Data integrity verification
- ✅ Rollback capabilities

---

## 🛠️ Management Commands

### Quick Setup Commands
```bash
# Start quick PostgreSQL environment
docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d

# Stop and clean
docker-compose -f docker-compose.quick.yml down -v

# View PostgreSQL logs
docker-compose -f docker-compose.quick.yml logs postgres-dev
```

### Development Commands
```bash
# Django development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Health check
python manage.py check_health
```

### Production Commands
```bash
# Deploy production stack
make deploy-production

# View production logs
make logs-production

# Backup database
make backup-database

# SSL certificate renewal
make renew-ssl
```

---

## 🏗️ Application Architecture

### Core Applications Status

| Application | Status | Description | Integration |
|-------------|--------|-------------|-------------|
| **Home** | ✅ Active | Dashboard & navigation | Integrated |
| **Timesheet** | 🔥 In Development | Time tracking & reporting | Active branch |
| **Daycare Invoice** | ✅ Ready | Invoice management | Ready for integration |
| **Employment History** | 📋 Planning | Employment record tracking | Planned |
| **Upcoming Payments** | 📋 Planning | Payment scheduling | Planned |
| **Credit Card Management** | 📋 Planning | Credit card tracking | Planned |
| **Household Budget** | 📋 Planning | Budget planning & tracking | Planned |

### Integration Architecture
```
┌─────────────────────────────────────┐
│           FamilyHub Dashboard        │
├─────────────────────────────────────┤
│  Home (Navigation & User Management) │
├─────────────────────────────────────┤
│              Apps Layer             │
│  ┌─────────┬─────────┬─────────┐     │
│  │Timesheet│ Daycare │Employment│     │
│  │         │ Invoice │ History │     │  
│  ├─────────┼─────────┼─────────┤     │
│  │Payments │ Credit  │Household│     │
│  │         │ Cards   │ Budget  │     │
│  └─────────┴─────────┴─────────┘     │
├─────────────────────────────────────┤
│            Shared Services          │
│    Models • Utils • Templates      │
└─────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using port 5432
netstat -an | findstr :5432

# Use different port for PostgreSQL
docker-compose -f docker-compose.quick.yml up -d
```

#### Permission Issues (Windows)
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
docker-compose -f docker-compose.quick.yml exec postgres-dev pg_isready

# Reset database
docker-compose -f docker-compose.quick.yml down -v
docker-compose -f docker-compose.quick.yml up -d
```

### Quick Commands for Troubleshooting
```bash
# View all service logs
docker-compose logs

# Check service status
docker-compose ps

# Health check
curl http://localhost:8000/health/
```

---

## 🎉 Success! Your FamilyHub Environment is Ready

Choose your path:

1. **🚀 Quick Start**: Run `.\quick-postgres-setup.ps1` for immediate PostgreSQL access
2. **🏗️ Development**: Use `docker-compose -f docker-compose.dev.yml up -d` for full development stack  
3. **🏭 Production**: Deploy with `docker-compose -f docker-compose.production.yml up -d` for production environment

**Next Steps:**
- Access pgAdmin at `http://localhost:5050` (Quick setup)
- Start developing with your preferred environment
- Check the specific README files for detailed guides
- Begin integrating your FamilyHub applications

**📚 Additional Documentation:**
- **`README.production.md`**: Detailed production deployment guide
- **`README.migration.md`**: Comprehensive database migration documentation  
- **`README.quick-postgres.md`**: Quick PostgreSQL setup guide

Welcome to your production-ready FamilyHub environment! 🎯

### 🏗️ Development Environment  
```yaml
Services: Django + PostgreSQL + Redis + Hot Reload
Access: Django at http://localhost:8000
Features: Live code reloading, debug toolbar, development settings
```

### 🏭 Production Environment
```yaml
Services: Nginx + Django + PostgreSQL + Redis + Celery + Backup
Access: https://localhost (SSL enabled)
Features: SSL, rate limiting, monitoring, automated backups
```

---

## 🚀 Getting Started

### Prerequisites
- **Docker**: 24.0+ with Docker Compose
- **Python**: 3.10+ (for local development)  
- **Git**: For version control
- **Windows PowerShell** or **Bash** (for setup scripts)

### 1. ⚡ Quick PostgreSQL Setup (Recommended First Step)

For immediate database access and development:

```powershell
# Windows (PowerShell)
.\quick-postgres-setup.ps1
```

```bash
# Linux/Mac
chmod +x quick-postgres-setup.sh
./quick-postgres-setup.sh
```

**What you get:**
- PostgreSQL 17.6 running on `localhost:5432`
- pgAdmin web interface at `http://localhost:5050`
- Pre-configured database connection
- Ready-to-use Django DATABASE_URL

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Development

### Working on Individual Apps
```bash
cd standalone-apps/timesheet
python manage.py runserver 8001
```

### Working on FamilyHub (All Apps)
```bash
cd FamilyHub
python manage.py runserver
```

## Testing
```bash
python manage.py test
```

## License
Private Project - All Rights Reserved
