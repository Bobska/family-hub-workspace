# 🚀 FamilyHub - Complete Development Setup Guide

**FamilyHub** is a comprehensive family management platform built with Django, featuring multiple integrated applications for managing timesheets, daycare invoices, employment history, and more.

## ✅ WHAT'S WORKING RIGHT NOW

### 1. **FamilyHub SQLite** - FULLY FUNCTIONAL ✅
```powershell
cd FamilyHub
venv\Scripts\activate
$env:DJANGO_SETTINGS_MODULE="FamilyHub.settings.development"
python manage.py runserver
# Visit: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```
**Status**: ✅ **READY FOR DEVELOPMENT**  
**Database**: SQLite (automatic setup)  
**Features**: Integrated dashboard with timesheet app  
**Admin Access**: ✅ Superuser configured  
**Setup Time**: 2 minutes

### 2. **Standalone Timesheet App** - FULLY FUNCTIONAL ✅
```powershell
cd standalone-apps\timesheet
venv\Scripts\activate
$env:DJANGO_SETTINGS_MODULE="timesheet_project.settings"
python manage.py runserver 8001
# Visit: http://127.0.0.1:8001/
# Admin: http://127.0.0.1:8001/admin/
```
**Status**: ✅ **READY FOR DEVELOPMENT**  
**Database**: SQLite (independent setup)  
**Features**: Complete time tracking system  
**Admin Access**: ✅ Superuser configured  
**Setup Time**: 2 minutes

### 3. **PostgreSQL Docker Setup** - INFRASTRUCTURE READY �
```powershell
docker ps  # Check: familyhub-postgres should be running
```
**Status**: 🔧 Infrastructure complete, Django integration in progress  
**Database**: PostgreSQL 17.6 in Docker  
**Features**: Production-like environment ready

## 🛠️ Available Commands

### PowerShell Development Script
```powershell
# Show help
PowerShell -File dev.ps1 help

# Quick SQLite setup (3 minutes)
PowerShell -File dev.ps1 quick

# Full Docker setup (10 minutes)
PowerShell -File dev.ps1 docker

# Health checks
PowerShell -File dev.ps1 health

# Container status
PowerShell -File dev.ps1 status

# Run migrations
PowerShell -File dev.ps1 migrate

# Database backup
PowerShell -File dev.ps1 backup

# Database restore
PowerShell -File dev.ps1 restore
```

## 📁 Project Structure

```
family-hub-workspace/
├── 🎯 WORKING NOW/
│   ├── standalone-apps/timesheet/     # ✅ Fully functional
│   └── FamilyHub/                     # ✅ SQLite version working
│
├── 🐳 Docker Setup/
│   ├── docker-compose.yml            # PostgreSQL + Redis + Django
│   ├── .env                          # Environment configuration  
│   └── docker/                       # Container configurations
│
├── 📋 Utilities/
│   ├── dev.ps1                       # Main development script
│   ├── scripts/backup_database.ps1   # Backup utilities
│   └── scripts/restore_database.ps1  # Restore utilities
│
└── 📊 Configuration/
    ├── requirements/                  # Python dependencies
    ├── FamilyHub/settings_docker.py  # PostgreSQL settings
    └── README_SETUP.md              # This file
```

## 🚀 Quick Start Guide

### For Immediate Integrated Development (2 minutes):
1. Open PowerShell in project root
2. `cd FamilyHub`
3. `venv\Scripts\activate`
4. `$env:DJANGO_SETTINGS_MODULE="FamilyHub.settings.development"`
5. `python manage.py runserver`
6. Visit: http://127.0.0.1:8000/
7. Admin: http://127.0.0.1:8000/admin/ (admin/admin)

### For Standalone Timesheet Development (2 minutes):
1. Open PowerShell in project root  
2. `cd standalone-apps\timesheet`
3. `venv\Scripts\activate`
4. `$env:DJANGO_SETTINGS_MODULE="timesheet_project.settings"`
5. `python manage.py runserver 8001`
6. Visit: http://127.0.0.1:8001/
7. Admin: http://127.0.0.1:8001/admin/ (admin/admin)

### For PostgreSQL Testing (Infrastructure Ready):
1. Check Docker containers: `docker ps`
2. Verify PostgreSQL is running: `familyhub-postgres`
3. Django integration: In progress

## � Admin Access & Superusers

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin`  
- **Email**: `admin@familyhub.local`

### Admin URLs
- **FamilyHub**: http://127.0.0.1:8000/admin/
- **Standalone Timesheet**: http://127.0.0.1:8001/admin/

### Superuser Management
```powershell
# Check superuser status for all environments
.\scripts\setup_superusers.ps1 status

# Setup superusers for all environments  
.\scripts\setup_superusers.ps1 all

# Setup specific environment
.\scripts\setup_superusers.ps1 familyhub
.\scripts\setup_superusers.ps1 timesheet
.\scripts\setup_superusers.ps1 docker
```

### Creating Custom Superuser
```powershell
# FamilyHub environment
cd FamilyHub; venv\Scripts\activate
$env:DJANGO_SETTINGS_MODULE="FamilyHub.settings.development"
python manage.py createsuperuser

# Standalone timesheet
cd standalone-apps\timesheet; venv\Scripts\activate  
$env:DJANGO_SETTINGS_MODULE="timesheet_project.settings"
python manage.py createsuperuser
```

## �💾 Database Options

### SQLite (Default)
- **Setup Time**: Instant
- **Use Case**: Development, testing
- **Location**: `FamilyHub/db.sqlite3`
- **Backup**: Copy file

### PostgreSQL (Docker)
- **Setup Time**: 10 minutes
- **Use Case**: Production-like testing
- **Location**: Docker container
- **Backup**: `PowerShell -File dev.ps1 backup`

## 🔧 Environment Configuration

### SQLite Setup (No configuration needed)
Just run the commands above!

### PostgreSQL Setup
1. Ensure Docker Desktop is running
2. Environment is configured in `.env`:
```env
DATABASE_URL=postgresql://django_user:your_secure_password@localhost:5432/familyhub
POSTGRES_DB=familyhub
POSTGRES_USER=django_user
POSTGRES_PASSWORD=your_secure_password
```

## 🏥 Health Monitoring

### Check System Status
```powershell
# Quick health check
PowerShell -File dev.ps1 health

# Container status
PowerShell -File dev.ps1 status

# Django health endpoint
# Visit: http://localhost:8000/health/
```

## 🔄 Backup & Restore

### Backup Database
```powershell
# Create timestamped backup
PowerShell -File dev.ps1 backup

# Or use script directly
PowerShell -File scripts\backup_database.ps1
```

### Restore Database
```powershell
# Show available backups and restore
PowerShell -File dev.ps1 restore

# Or use script directly
PowerShell -File scripts\restore_database.ps1 backup_file.sql
```

## 🎯 Next Steps

### ✅ What's Ready Now:
1. **Timesheet app**: Full time tracking functionality
2. **FamilyHub dashboard**: Integrated view
3. **SQLite development**: Zero-config setup
4. **PostgreSQL option**: Docker-based advanced setup

### 🔄 What's Being Developed:
1. Additional family management apps
2. Enhanced dashboard features
3. Production deployment automation
4. User authentication system

### 🚀 Production Readiness:
- Docker containerization: ✅ Complete
- Database migrations: ✅ Working
- Static file handling: ✅ Configured
- Health monitoring: ✅ Implemented
- Backup/restore: ✅ Automated

## 🆘 Troubleshooting

### Common Issues:

**1. "Command not recognized"**
```powershell
# Solution: Run from project root directory
cd c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace
```

**2. Docker not starting**
```powershell
# Solution: Start Docker Desktop first
# Then run: docker version
```

**3. Port already in use**
```powershell
# Solution: Use different port
python manage.py runserver 8002
```

**4. PowerShell execution policy**
```powershell
# Solution: Allow script execution
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🎉 Success Indicators

### ✅ FamilyHub Setup Complete When:
- Django server starts without errors: ✅ **CONFIRMED**
- Browser loads at http://127.0.0.1:8000/: ✅ **CONFIRMED** 
- Dashboard shows timesheet integration: ✅ **CONFIRMED**
- Admin access works at /admin/: ✅ **CONFIRMED**
- Can login with admin/admin: ✅ **CONFIRMED**
- Database operations work: ✅ **CONFIRMED**
- Console shows "Starting development server": ✅ **CONFIRMED**

### ✅ Standalone Timesheet Complete When:
- Django server starts on port 8001: ✅ **CONFIRMED**
- Browser loads at http://127.0.0.1:8001/: ✅ **CONFIRMED**
- Admin access works at /admin/: ✅ **CONFIRMED** 
- Can login with admin/admin: ✅ **CONFIRMED**
- Independent timesheet functionality: ✅ **CONFIRMED**

### 🚀 Ready for Development:
- ✅ FamilyHub dashboard accessible with admin access
- ✅ Standalone timesheet fully functional with admin access
- ✅ Timesheet app integrated in FamilyHub
- ✅ SQLite databases ready in both environments
- ✅ Django 5.2.5 running successfully in both setups
- ✅ All superusers configured and tested
- 🐳 PostgreSQL infrastructure ready
- 🔧 Docker containers healthy

---

**FamilyHub** - Your complete family management solution! 🏠

**Status**: Ready for Development  
**Version**: 1.0.0  
**Last Updated**: August 29, 2025
