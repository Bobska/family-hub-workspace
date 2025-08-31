#!/bin/bash
# Script to run a standalone app

if [ $# -eq 0 ]; then
    echo "Usage: ./run_standalone.sh <app_name> [port]"
    echo "Example: ./run_standalone.sh timesheet 8001"
    echo ""
    echo "Available apps:"
    echo "  - timesheet (default port: 8001)"  
    echo "  - daycare_invoice (default port: 8002)"
    echo "  - employment_history (default port: 8003)"
    echo "  - upcoming_payments (default port: 8004)"
    echo "  - credit_card_mgmt (default port: 8005)"
    echo "  - household_budget (default port: 8006)"
    exit 1
fi

APP_NAME=$1
PORT=${2:-8001}

# Set default ports based on app name
case $APP_NAME in
    "timesheet") PORT=${2:-8001} ;;
    "daycare_invoice") PORT=${2:-8002} ;;
    "employment_history") PORT=${2:-8003} ;;
    "upcoming_payments") PORT=${2:-8004} ;;
    "credit_card_mgmt") PORT=${2:-8005} ;;
    "household_budget") PORT=${2:-8006} ;;
esac

APP_DIR="../standalone-apps/$APP_NAME"

if [ ! -d "$APP_DIR" ]; then
    echo "❌ Error: Standalone app '$APP_NAME' not found at $APP_DIR"
    exit 1
fi

echo "🚀 Starting standalone app: $APP_NAME"
echo "📍 URL: http://127.0.0.1:$PORT/"
echo "📁 Directory: $APP_DIR"

cd "$APP_DIR"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run migrations if needed
echo "📄 Applying migrations..."
python manage.py migrate --verbosity 0

echo "🌐 Starting Django development server on port $PORT..."
echo "Press Ctrl+C to stop the server"

python manage.py runserver $PORT
