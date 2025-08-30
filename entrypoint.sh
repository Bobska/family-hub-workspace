#!/bin/sh

# Wait for PostgreSQL to be ready using our Python script
echo "Waiting for PostgreSQL to be ready..."
python /app/scripts/wait-for-postgres.py

echo "PostgreSQL is up - executing commands"

# Change to Django project directory
cd /app/FamilyHub

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser using management command
echo "Initializing superuser..."
python manage.py init_superuser

# Start Gunicorn
echo "Starting Gunicorn server..."
gunicorn FamilyHub.wsgi:application --bind 0.0.0.0:8000
