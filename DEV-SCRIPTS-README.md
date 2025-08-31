# FamilyHub Development Scripts 🚀

This document outlines the available development scripts to make working with FamilyHub faster and easier.

## 📁 Script Locations

```
family-hub-workspace/
├── dev-new.ps1              # Main development workflow script
├── FamilyHub/
│   ├── dev-start.ps1        # Start local development server
│   ├── dev-setup-new.ps1    # Setup local development environment
│   ├── dev-migrate.ps1      # Database migrations
│   └── dev-test.ps1         # Run tests
└── scripts/
    └── quick.ps1            # Universal launcher (copied from production)
```

## 🎯 Quick Start

### First Time Setup
```powershell
# From workspace root
.\dev-new.ps1 setup
```

### Start Development Server
```powershell
# Local development (SQLite)
.\dev-new.ps1 start

# Docker development (PostgreSQL)
.\dev-new.ps1 docker
```

## 📋 Available Commands

### Main Development Script (`dev-new.ps1`)

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all available commands | `.\dev-new.ps1 help` |
| `setup` | First-time environment setup | `.\dev-new.ps1 setup` |
| `start` | Start local SQLite server | `.\dev-new.ps1 start` |
| `docker` | Start Docker PostgreSQL setup | `.\dev-new.ps1 docker` |
| `status` | Check environment status | `.\dev-new.ps1 status` |
| `migrate` | Run database migrations | `.\dev-new.ps1 migrate` |
| `test` | Run Django tests | `.\dev-new.ps1 test` |
| `shell` | Open Django shell | `.\dev-new.ps1 shell` |

### Docker Commands

| Command | Description | Example |
|---------|-------------|---------|
| `build` | Build Docker containers | `.\dev-new.ps1 build` |
| `up` | Start Docker services | `.\dev-new.ps1 up` |
| `down` | Stop Docker services | `.\dev-new.ps1 down` |
| `restart` | Restart Docker services | `.\dev-new.ps1 restart` |
| `logs` | Show container logs | `.\dev-new.ps1 logs` |

### Individual Scripts

#### `FamilyHub/dev-start.ps1`
- Starts local development server
- Uses SQLite database
- Includes debug widget
- Auto-reloads on file changes

#### `FamilyHub/dev-setup-new.ps1`
- Creates virtual environment
- Installs all required packages
- Sets up SQLite database
- Creates superuser (optional)

#### `FamilyHub/dev-migrate.ps1`
- Creates new migrations
- Applies migrations to database
- Shows migration status

#### `FamilyHub/dev-test.ps1`
- Runs Django test suite
- Shows test results
- Validates code quality

## 🔄 Development Workflows

### Local Development (Recommended for Speed)
```powershell
# First time setup
.\dev-new.ps1 setup

# Daily development
.\dev-new.ps1 start
# Server runs at http://127.0.0.1:8000/

# When you make model changes
.\dev-new.ps1 migrate

# Before committing
.\dev-new.ps1 test
```

### Docker Development (Recommended for Production Parity)
```powershell
# Build and start containers
.\dev-new.ps1 docker
# Server runs at http://localhost:8000/

# View logs
.\dev-new.ps1 logs

# Stop when done
.\dev-new.ps1 down
```

### Testing Workflow
```powershell
# Run all tests
.\dev-new.ps1 test

# Or run from FamilyHub directory
cd FamilyHub
.\dev-test.ps1
```

## 🎨 Features

### ✅ Local Development Benefits
- **Fast startup** - No container building
- **SQLite database** - Simple, file-based
- **Auto-reload** - Changes reflected immediately
- **Debug widget** - Environment info overlay
- **Lightweight** - Minimal resource usage

### ✅ Docker Development Benefits
- **Production parity** - Same environment as production
- **PostgreSQL** - Full-featured database
- **Isolated environment** - Consistent across machines
- **Full stack** - Includes Redis, Nginx (in production)

### ✅ Script Features
- **Color-coded output** - Easy to read status messages
- **Error handling** - Clear error messages and guidance
- **Environment validation** - Checks before running
- **Auto-setup** - Creates what's needed automatically

## 🐛 Troubleshooting

### Virtual Environment Issues
```powershell
# If venv is corrupted
Remove-Item -Recurse -Force FamilyHub/venv
.\dev-new.ps1 setup
```

### Docker Issues
```powershell
# If containers won't start
.\dev-new.ps1 down
.\dev-new.ps1 build
.\dev-new.ps1 up
```

### Permission Issues
```powershell
# If scripts won't run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database Issues
```powershell
# Reset local database
Remove-Item FamilyHub/db.sqlite3
.\dev-new.ps1 migrate
```

## 📊 Environment Comparison

| Feature | Local (SQLite) | Docker (PostgreSQL) |
|---------|----------------|---------------------|
| **Startup Time** | ~5 seconds | ~30 seconds |
| **Resource Usage** | Low | Medium |
| **Database** | SQLite | PostgreSQL 17 |
| **Debug Widget** | ✅ Yes | ✅ Yes |
| **Auto-reload** | ✅ Yes | ✅ Yes |
| **Production Parity** | ❌ No | ✅ Yes |
| **Timesheet Integration** | ❌ No | ✅ Yes |

## 🔧 Customization

You can modify the scripts to suit your needs:

- **Change ports**: Edit the `runserver` command in scripts
- **Add environment variables**: Modify the settings files
- **Custom commands**: Add new functions to `dev-new.ps1`
- **Different databases**: Update connection settings

## 📚 Next Steps

1. **Choose your workflow**: Local for speed, Docker for production parity
2. **Run setup**: `.\dev-new.ps1 setup`
3. **Start developing**: `.\dev-new.ps1 start`
4. **Make changes**: Edit code, templates, models
5. **Test changes**: `.\dev-new.ps1 test`
6. **Commit**: Follow the project's git workflow

Happy coding! 🎉
