@echo off
REM 🚀 FamilyHub Development Workflow - Windows Batch File
REM Author: FamilyHub Team
REM Date: August 29, 2025
REM Version: 1.0.0

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="quick" goto quick
if "%1"=="status" goto status
if "%1"=="health" goto health
if "%1"=="migrate" goto migrate
if "%1"=="shell" goto shell
if "%1"=="test" goto test
if "%1"=="logs" goto logs
if "%1"=="stop" goto stop
if "%1"=="dev-tools" goto dev-tools
goto unknown

:help
echo.
echo 🚀 FamilyHub Development Workflow Commands
echo ==========================================
echo.
echo 🚀 Quick Start:
echo   dev.bat quick         ⚡ Start quick PostgreSQL setup (5 minutes)
echo   dev.bat status        📊 Show service status
echo   dev.bat health        💚 Check application health
echo.
echo 🔧 Development:
echo   dev.bat migrate       📊 Run Django migrations
echo   dev.bat shell         🐍 Open Django shell (local)
echo   dev.bat test          🧪 Run tests (local)
echo.
echo 🔍 Monitoring:
echo   dev.bat logs          📋 View PostgreSQL logs
echo.
echo 🛑 Control:
echo   dev.bat stop          🛑 Stop all containers
echo.
echo 🔧 Utilities:
echo   dev.bat dev-tools     🛠️  Show development tools and URLs
echo.
echo 💡 For more features, use: PowerShell -File dev.ps1
goto end

:quick
echo ⚡ Starting Quick PostgreSQL Environment...
if exist "quick-postgres-setup.ps1" (
    PowerShell -File quick-postgres-setup.ps1
) else (
    echo Starting PostgreSQL with Docker Compose...
    docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d
    timeout /t 10 /nobreak >nul
    echo ✅ Quick PostgreSQL environment started!
    echo 🌐 pgAdmin: http://localhost:5050
    echo 🐘 PostgreSQL: localhost:5432
)
goto end

:status
echo 📊 Service Status:
echo ==================
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=familyhub"
goto end

:health
echo 💚 Checking Application Health...
echo ==================================
echo.
docker --version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Docker: Available
) else (
    echo ❌ Docker: Not available
)
echo.
echo 🌐 Web Services:
curl -s http://localhost:5050 >nul 2>&1
if %errorlevel%==0 (
    echo ✅ pgAdmin: Healthy (http://localhost:5050)
) else (
    echo ⚠️  pgAdmin: Not accessible (http://localhost:5050)
)
goto end

:migrate
echo 📊 Running Django Migrations...
cd FamilyHub
python manage.py makemigrations
python manage.py migrate
echo ✅ Migrations completed!
cd ..
goto end

:shell
echo 🐍 Opening Django Shell...
cd FamilyHub
python manage.py shell
cd ..
goto end

:test
echo 🧪 Running Tests...
cd FamilyHub
python manage.py test
echo ✅ Tests completed!
cd ..
goto end

:logs
echo 📋 Viewing PostgreSQL Logs...
docker-compose -f docker-compose.quick.yml --env-file .env.quick logs -f postgres-dev
goto end

:stop
echo 🛑 Stopping All Containers...
docker-compose -f docker-compose.quick.yml --env-file .env.quick down
echo ✅ All containers stopped!
goto end

:dev-tools
echo 🛠️  FamilyHub Development Tools
echo ==============================
echo.
echo 🌐 Web Interfaces:
echo   pgAdmin:      http://localhost:5050
echo   Django:       http://localhost:8000 (when running locally)
echo.
echo 🔗 Database Connection:
echo   Host:         localhost
echo   Port:         5432
echo   Database:     familyhub
echo   Username:     django
echo   Password:     secretpass
echo   URL:          postgresql://django:secretpass@localhost:5432/familyhub
echo.
echo 🐘 pgAdmin Access:
echo   Email:        admin@familyhub.local
echo   Password:     admin123
goto end

:unknown
echo ❌ Unknown command: %1
echo.
goto help

:end
