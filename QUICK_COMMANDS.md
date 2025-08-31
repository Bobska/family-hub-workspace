# 🚀 FamilyHub Quick Commands Reference

## Local Development Made Easy! 

You can now use simple `make` commands to run all your development tasks quickly:

### 🏁 Quick Start Commands

```bash
# Complete fresh setup (first time only)
make local-fresh-start

# Just start the main FamilyHub (most common)
make local-start

# Start specific standalone app
make local-start-timesheet

# Check if everything is working
make local-check
```

### 🔧 FamilyHub Local Development Commands

| Command | What it does |
|---------|-------------|
| `make local-setup` | Setup virtual environment and install dependencies |
| `make local-start` | Start Django development server at http://127.0.0.1:8000 |
| `make local-migrate` | Run database migrations (makemigrations + migrate) |
| `make local-test` | Run all tests in local environment |
| `make local-shell` | Open Django shell |
| `make local-superuser` | Create admin user |
| `make local-check` | Run Django system checks |
| `make local-clean` | Clean local database and cache files |

### � Standalone Apps (Independent Development)

| Command | App | Port | URL |
|---------|-----|------|-----|
| `make local-start-timesheet` | Timesheet | 8001 | http://127.0.0.1:8001 |
| `make local-start-daycare` | Daycare Invoice | 8002 | http://127.0.0.1:8002 |
| `make local-start-employment` | Employment History | 8003 | http://127.0.0.1:8003 |
| `make local-start-payments` | Upcoming Payments | 8004 | http://127.0.0.1:8004 |
| `make local-start-credit` | Credit Card Mgmt | 8005 | http://127.0.0.1:8005 |
| `make local-start-budget` | Household Budget | 8006 | http://127.0.0.1:8006 |

### 🔧 Standalone App Management (Timesheet Example)

```bash
# Setup timesheet for first time
make local-setup-timesheet

# Daily timesheet development
make local-start-timesheet      # Start on port 8001
make local-check-timesheet      # System checks
make local-test-timesheet       # Run tests
make local-migrate-timesheet    # Database migrations
make local-shell-timesheet      # Django shell
```

### 🚀 Special Commands

```bash
# Start all standalone apps at once (in separate windows)
make local-start-all-apps

# Fresh start with everything
make local-fresh-start    # Setup → Migrate → Create superuser → Start server
```

### 🔄 Development Workflows

#### Daily FamilyHub Development
```bash
# Start main hub
make local-start          # FamilyHub at http://127.0.0.1:8000

# After pulling changes
make local-migrate
make local-start
```

#### Standalone App Development
```bash
# Work on timesheet independently
make local-start-timesheet    # http://127.0.0.1:8001

# Work on multiple apps
make local-start-all-apps     # All apps in separate windows
```

#### Testing Both Together
```bash
# Terminal 1: FamilyHub
make local-start              # http://127.0.0.1:8000

# Terminal 2: Timesheet standalone
make local-start-timesheet    # http://127.0.0.1:8001

# Compare integration vs standalone
```

### 🐳 Docker Commands (for comparison)

```bash
# Docker development (existing)
make dev-docker          # Start with Docker
make dev-detached        # Start Docker in background
make migrate             # Docker migrations
make test                # Docker tests
```

### 💡 Pro Tips

1. **Use `make local-start` for FamilyHub development** - fastest startup
2. **Use `make local-start-timesheet` for standalone timesheet work** - port 8001
3. **Use `make local-start-all-apps` to compare all apps** - separate windows
4. **Use `make dev-docker` when you need PostgreSQL** - full production simulation
5. **Use `make help` anytime** - see all available commands

### 🎯 Most Common Workflows

#### Integrated Development (FamilyHub)
```bash
# Morning routine:
make local-start                 # http://127.0.0.1:8000

# After pulling changes:
make local-migrate
make local-start
```

#### Standalone Development (Individual Apps)
```bash
# Work on timesheet only:
make local-start-timesheet       # http://127.0.0.1:8001

# Setup new app environment:
make local-setup-timesheet       # One-time setup
make local-migrate-timesheet     # Database setup
make local-start-timesheet       # Start development
```

#### Comparison Testing
```bash
# Compare integrated vs standalone:
make local-start                 # FamilyHub (integrated)
make local-start-timesheet       # Timesheet (standalone)
# Now you have both running simultaneously
```

### 📍 Command Locations & Ports

- **Workspace Root**: `C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\`
- **All make commands run from workspace root**
- **FamilyHub**: http://127.0.0.1:8000 (integrated apps)
- **Timesheet**: http://127.0.0.1:8001 (standalone)
- **Other Apps**: Ports 8002-8006 (standalone)

### 🔧 Behind the Scenes

Each `make local-*` command:
- Activates the correct virtual environment automatically
- Uses the appropriate Django settings
- Handles PowerShell execution policies
- Runs from the correct directory
- Provides clear feedback about what's happening

### 🚨 Troubleshooting

#### FamilyHub Issues
```bash
make local-check         # Django system checks
make local-migrate       # Apply any pending migrations
make local-clean         # Clean database if needed
make local-fresh-start   # Complete reset
```

#### Standalone App Issues  
```bash
make local-check-timesheet      # Check timesheet app
make local-setup-timesheet      # Reinstall dependencies
make local-migrate-timesheet    # Fix database issues
```

### 🆚 When to Use What

| Use Case | Command | Why |
|----------|---------|-----|
| **Daily FamilyHub development** | `make local-start` | Fastest, integrated view |
| **Timesheet-only work** | `make local-start-timesheet` | Isolated, no dependencies |
| **Comparing integration** | Both commands | Side-by-side comparison |
| **Production testing** | `make dev-docker` | PostgreSQL, full stack |
| **First time setup** | `make local-fresh-start` | Complete environment |

---

**Happy coding! 🎉** You now have both integrated and standalone development options!
