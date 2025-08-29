#!/bin/bash

# SQL Server to PostgreSQL Migration Quick Start Script

echo "🗄️  FamilyHub SQL Server Migration Setup"
echo "========================================"

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.10+"
    exit 1
fi

# Check pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip"
    exit 1
fi

echo "✅ Python and pip found"

# Install migration dependencies
echo "📦 Installing migration dependencies..."
pip install -r requirements/migration.txt

# Check ODBC driver
echo "🔌 Checking ODBC Driver..."
if python -c "import pyodbc; drivers = pyodbc.drivers(); print('ODBC drivers:', drivers)" 2>/dev/null; then
    echo "✅ ODBC drivers available"
else
    echo "⚠️  ODBC Driver 17 for SQL Server may not be installed"
    echo "   Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
fi

# Create migration directories
echo "📁 Creating migration directories..."
mkdir -p fixtures/sqlserver_export
mkdir -p logs/migration
mkdir -p backups/pre_migration

# Set up configuration template
echo "⚙️  Setting up configuration..."
if [ ! -f "config/migration_config.json" ]; then
    echo "📝 Creating migration configuration template..."
    echo "   Please edit config/migration_config.json with your SQL Server details"
else
    echo "✅ Migration configuration exists"
fi

# Test Django setup
echo "🔧 Testing Django setup..."
if python manage.py check --verbosity=0; then
    echo "✅ Django setup OK"
else
    echo "❌ Django setup issues detected"
    exit 1
fi

# Test PostgreSQL connection
echo "🐘 Testing PostgreSQL connection..."
if python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT version()'); print('PostgreSQL OK')" 2>/dev/null; then
    echo "✅ PostgreSQL connection OK"
else
    echo "⚠️  PostgreSQL connection issue"
    echo "   Please check DATABASE_URL or database settings"
fi

# Run migration pipeline test
echo "🧪 Running migration pipeline test..."
if python test_migration_pipeline.py --dry-run 2>/dev/null; then
    echo "✅ Migration pipeline test passed"
else
    echo "⚠️  Migration pipeline test had issues"
    echo "   Review configuration and connection settings"
fi

echo ""
echo "🎉 Migration setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit config/migration_config.json with your SQL Server details"
echo "2. Test connection: python manage.py export_from_sqlserver --config config/migration_config.json --dry-run"
echo "3. Run full test: python test_migration_pipeline.py --config config/migration_config.json"
echo "4. Execute migration: python manage.py import_from_sqlserver --config config/migration_config.json"
echo ""
echo "📖 Documentation: README.migration.md"
