# 🚀 FamilyHub Quick Commands Reference

## Local Development Made Easy! 

You can now use simple `make` commands to run all your development tasks quickly:

### 🏁 Quick Start Commands

```bash
# Complete fresh setup (first time only)
make local-fresh-start

# Just start the server (most common)
make local-start

# Check if everything is working
make local-check
```

### 🔧 Local Development Commands

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

### 🔄 Workflow Commands

```bash
# Fresh start with everything
make local-fresh-start    # Setup → Migrate → Create superuser → Start server

# Daily development
make local-start          # Start server
make local-migrate        # Apply any new migrations
make local-test           # Run tests after changes
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

1. **Use `make local-start` for daily development** - fastest startup
2. **Use `make dev-docker` when you need PostgreSQL** - full production simulation
3. **Use `make local-fresh-start` after pulling changes** - ensures clean state
4. **Use `make help` anytime** - see all available commands

### 🎯 Most Common Workflow

```bash
# Morning routine:
make local-start

# After pulling changes:
make local-migrate
make local-start

# Before committing:
make local-test
make local-check
```

### 📍 Command Locations

- **Workspace Root**: `C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\`
- **All make commands run from workspace root**
- **Scripts are located in**: `FamilyHub/` directory
- **Local server runs on**: http://127.0.0.1:8000

### 🔧 Behind the Scenes

Each `make local-*` command:
- Activates the virtual environment automatically
- Uses the correct Django settings (`FamilyHub.settings.development`)
- Handles PowerShell execution policies
- Provides clear feedback about what's happening

### 🚨 Remember

- Run `make` commands from the **workspace root** (not from FamilyHub/ folder)
- Local commands use SQLite database
- Docker commands use PostgreSQL database
- Local is faster for development, Docker for production testing

---

**Happy coding! 🎉** Your development workflow just got much simpler.
