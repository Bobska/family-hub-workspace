#!/bin/bash
# Script to run FamilyHub with integrated apps

echo "🚀 Starting FamilyHub with integrated apps..."

cd "$(dirname "$0")"

# Activate virtual environment if exists (Linux/Mac)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Use development_full settings for integrated mode
export DJANGO_SETTINGS_MODULE="FamilyHub.settings.development_full"
echo "🔧 Using integrated settings: $DJANGO_SETTINGS_MODULE"

# Ensure migrations are up to date
echo "📄 Checking migrations..."
python manage.py makemigrations --check --verbosity 0 || {
    echo "⚠️  New migrations needed. Creating..."
    python manage.py makemigrations
}

python manage.py migrate --verbosity 1

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --verbosity 0

echo "🌐 Starting Django development server..."
echo "📍 Dashboard: http://127.0.0.1:8000/"
echo "📍 Timesheet: http://127.0.0.1:8000/timesheet/"
echo "📍 Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"

# Run server
python manage.py runserver
