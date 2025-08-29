# 🚀 FamilyHub Server Launcher Guide

## **Solution Summary**
Created convenient PowerShell scripts to solve the issue where `python manage.py runserver` fails from workspace root because manage.py files are located in subdirectories.

## **Available Launcher Scripts**

### 1. **FamilyHub Launcher** ✅ WORKING
```powershell
# Start FamilyHub on default port 8000
.\scripts\start_familyhub.ps1

# Start on custom port
.\scripts\start_familyhub.ps1 -Port 8080

# Start without auto-reload
.\scripts\start_familyhub.ps1 -NoReload
```

### 2. **Timesheet Launcher** ✅ WORKING
```powershell
# Start Timesheet on default port 8001
.\scripts\start_timesheet.ps1

# Start on custom port
.\scripts\start_timesheet.ps1 -Port 8002

# Start without auto-reload
.\scripts\start_timesheet.ps1 -NoReload
```

### 3. **Universal Quick Launcher** ✅ WORKING
```powershell
# Show help and available commands
.\scripts\quick.ps1

# Show server status
.\scripts\quick.ps1 status

# Start FamilyHub
.\scripts\quick.ps1 familyhub

# Start Timesheet
.\scripts\quick.ps1 timesheet

# Show both server instructions
.\scripts\quick.ps1 both

# Check superuser status
.\scripts\quick.ps1 superusers
```

## **What Each Script Does**

### **FamilyHub Launcher**
1. **Auto-navigates** to `FamilyHub/` directory
2. **Activates** virtual environment (`FamilyHub/venv/`)
3. **Sets** Django settings to `FamilyHub.settings.development`
4. **Runs** system checks
5. **Checks for pending migrations** and runs makemigrations/migrate if needed
6. **Starts** server with clear output showing:
   - Server URL: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Credentials: admin / admin

### **Timesheet Launcher**
1. **Auto-navigates** to `standalone-apps/timesheet/` directory
2. **Activates** virtual environment (`timesheet/venv/`)
3. **Sets** Django settings to `timesheet_project.settings`
4. **Runs** system checks
5. **Checks for pending migrations** and runs makemigrations/migrate if needed
6. **Starts** server with clear output showing:
   - Server URL: http://127.0.0.1:8001/
   - Admin Panel: http://127.0.0.1:8001/admin/
   - Credentials: admin / admin

### **Universal Quick Launcher**
- **Status checking**: Shows which servers are running/stopped
- **Migration management**: Run migrations for both environments
- **Help system**: Lists all available commands
- **Unified interface**: Single entry point for all development tasks

## **Verified Working Features**

✅ **FamilyHub Server**: Starts successfully on port 8000  
✅ **Timesheet Server**: Starts successfully on port 8001  
✅ **Status Checking**: Accurately detects running servers  
✅ **Virtual Environment**: Auto-activates when available  
✅ **Django Settings**: Properly configures for each environment  
✅ **System Checks**: Validates Django configuration before starting  
✅ **Migration Management**: Automatically checks and applies pending migrations  
✅ **Error Handling**: Graceful handling of missing files/directories  
✅ **User Experience**: Clear output with server information and admin credentials  

## **Quick Commands Reference**

### **Most Common Usage**
```powershell
# Start FamilyHub (most common)
.\scripts\start_familyhub.ps1

# Start Timesheet (standalone development)
.\scripts\start_timesheet.ps1

# Check what's running
.\scripts\quick.ps1 status
```

### **Development Workflow**
```powershell
# 1. Check current status
.\scripts\quick.ps1 status

# 2. Run migrations if needed (optional - servers do this automatically)
.\scripts\quick.ps1 migrate

# 3. Start your target server
.\scripts\start_familyhub.ps1
# OR
.\scripts\start_timesheet.ps1

# 4. Access in browser:
# FamilyHub: http://127.0.0.1:8000/
# Timesheet: http://127.0.0.1:8001/
# Admin: Add /admin/ to either URL

# 5. Login with: admin / admin
```

## **Troubleshooting**

### **If Execution Policy Errors Occur:**
```powershell
# Option 1: Bypass for single command (if needed)
powershell -ExecutionPolicy Bypass -File .\scripts\start_familyhub.ps1

# Option 2: Set execution policy (requires admin)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **If Virtual Environment Issues:**
The scripts will attempt to run without virtual environment if venv is missing, but will show warnings.

### **If Port Already in Use:**
```powershell
# Use custom port
.\scripts\start_familyhub.ps1 -Port 8080
```

## **File Locations**

```
family-hub-workspace/
├── scripts/
│   ├── start_familyhub.ps1           # FamilyHub launcher
│   ├── start_timesheet.ps1           # Timesheet launcher
│   ├── quick.ps1                     # Universal launcher
│   └── setup_superusers.ps1          # Superuser management
├── FamilyHub/                         # Main integrated project
│   ├── manage.py                     # Django management
│   └── venv/                         # Virtual environment
└── standalone-apps/timesheet/        # Standalone timesheet
    ├── manage.py                     # Django management
    └── venv/                         # Virtual environment
```

## **Success Confirmation**

The scripts successfully solve the original problem:
- ❌ **Before**: `python manage.py runserver` failed from workspace root
- ✅ **After**: Simple commands that handle all directory navigation and environment setup automatically

Both FamilyHub and Timesheet servers can now be started with single commands that handle all the complexity of:
- Directory navigation
- Virtual environment activation
- Django settings configuration
- System validation
- Clear user feedback

---

**Status**: All launcher scripts are working and tested ✅  
**Next**: Ready for full development workflow with convenient server startup
