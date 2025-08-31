# FamilyHub Local Development Scripts

This directory contains PowerShell scripts to make local Django development faster and easier.

## 🚀 Quick Start

```powershell
# First time setup
./dev-setup.ps1

# Start development server
./dev-start.ps1

# Run migrations
./dev-migrate.ps1

# Run tests
./dev-test.ps1

# Database management
./dev-db.ps1 <command>
```

## 📜 Available Scripts

### `dev-setup.ps1`
**Initial environment setup** - Run this once when starting development
- Creates virtual environment
- Installs all required packages
- Sets up SQLite database
- Creates default admin user (admin/admin123)

### `dev-start.ps1`
**Start development server** - Your daily driver for running the local server
- Activates virtual environment
- Runs system checks
- Starts Django development server on http://127.0.0.1:8000/
- Shows server status and configuration

### `dev-migrate.ps1`
**Database migrations** - Run when you change models
- Checks for model changes
- Creates new migrations if needed
- Applies migrations to database
- Shows migration status

### `dev-test.ps1`
**Testing suite** - Run before committing code
- Django system checks
- Migration status check
- Unit tests
- Static files validation
- Comprehensive test summary

### `dev-db.ps1`
**Database management** - Advanced database operations
- `reset` - Delete and recreate database
- `backup` - Create timestamped backup
- `restore` - Restore from backup
- `shell` - Open Django database shell
- `status` - Show migration status

## 🔧 Environment Details

- **Database**: SQLite (local file: `db.sqlite3`)
- **Settings**: `FamilyHub.settings.development`
- **Virtual Environment**: `venv/` directory
- **Debug Mode**: Enabled
- **Auto-reload**: Enabled for file changes

## 📂 Apps Included (Local Development)

- **Core FamilyHub**: Dashboard and base functionality
- **Admin Panel**: Django admin interface
- **Authentication**: Login/logout system

*Note: Timesheet and other apps are only available in Docker/production mode*

## 🔑 Default Credentials

- **Admin User**: admin
- **Password**: admin123
- **Email**: admin@familyhub.local

## 🆚 Local vs Docker Development

| Feature | Local (SQLite) | Docker (PostgreSQL) |
|---------|----------------|---------------------|
| Setup Speed | ⚡ Fast | 🐌 Slower |
| Database | SQLite | PostgreSQL 17 |
| Apps | Core only | Full integration |
| Debug Widget | ✅ | ✅ |
| Hot Reload | ✅ | ✅ |
| Production-like | ❌ | ✅ |

## 🐛 Troubleshooting

### Virtual Environment Issues
```powershell
# Delete and recreate
Remove-Item -Recurse venv
./dev-setup.ps1
```

### Permission Issues
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database Issues
```powershell
# Reset database
./dev-db.ps1 reset
```

### Package Issues
```powershell
# Reinstall packages
./dev-setup.ps1
```

## 📝 Development Workflow

1. **First time setup**: `./dev-setup.ps1`
2. **Daily development**: `./dev-start.ps1`
3. **After model changes**: `./dev-migrate.ps1`
4. **Before committing**: `./dev-test.ps1`
5. **Database management**: `./dev-db.ps1 <command>`

## 🔄 Switching Between Local and Docker

### To Docker:
```powershell
# Stop local server (Ctrl+C)
cd ..
make rebuild
```

### To Local:
```powershell
# Stop Docker
docker-compose down
cd FamilyHub
./dev-start.ps1
```

---

💡 **Tip**: Keep the local server running while developing. It will automatically reload when you save files!
