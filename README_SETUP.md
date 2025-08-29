# 🚀 FamilyHub - Complete Development Setup Guide

**FamilyHub** is a comprehensive family management platform built with Django, featuring multiple integrated applications for managing timesheets, daycare invoices, employment history, and more.

## ✅ WHAT'S WORKING RIGHT NOW

### 1. **Standalone Timesheet App** - FULLY FUNCTIONAL
```powershell
cd standalone-apps\timesheet
python manage.py runserver 8001
# Visit: http://127.0.0.1:8001/
```
**Status**: ✅ Ready for immediate development  
**Database**: SQLite (no setup required)  
**Features**: Complete time tracking system

### 2. **FamilyHub SQLite** - FUNCTIONAL
```powershell
PowerShell -File dev.ps1 quick
# Visit: http://localhost:8000/
```
**Status**: ✅ Ready for integrated development  
**Database**: SQLite (automatic)  
**Features**: Integrated dashboard with timesheet

### 3. **PostgreSQL Docker Setup** - ADVANCED
```powershell
PowerShell -File dev.ps1 docker
# Visit: http://localhost:8000/
```
**Status**: 🔧 Advanced setup (requires Docker)  
**Database**: PostgreSQL 17.6 in Docker  
**Features**: Production-like environment

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

### For Immediate Development (2 minutes):
1. Open PowerShell in project root
2. `cd standalone-apps\timesheet`
3. `python manage.py runserver 8001`
4. Visit: http://127.0.0.1:8001/

### For Integrated Development (5 minutes):
1. Open PowerShell in project root
2. `PowerShell -File dev.ps1 quick`
3. Visit: http://localhost:8000/

### For PostgreSQL Testing (10+ minutes):
1. Ensure Docker Desktop is running
2. `PowerShell -File dev.ps1 docker`
3. Wait for containers to start
4. Visit: http://localhost:8000/

## 💾 Database Options

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

### ✅ Setup Complete When:
- Django server starts without errors
- Browser loads the application
- Database operations work
- No error messages in console

### 🚀 Ready for Development:
- Application accessible at specified URL
- Dashboard shows timesheet integration
- Database queries execute successfully
- All health checks pass

---

**FamilyHub** - Your complete family management solution! 🏠

**Status**: Ready for Development  
**Version**: 1.0.0  
**Last Updated**: August 29, 2025
