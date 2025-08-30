#!/bin/bash

# Database initialization script for FamilyHub
# Handles database setup for both Docker and local PostgreSQL 17

set -e

echo "=== FamilyHub Database Initialization ==="

# Default values
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-familyhub_db}
POSTGRES_USER=${POSTGRES_USER:-familyhub_user}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-TempPass123!ChangeMe}
POSTGRES_ADMIN_USER=${POSTGRES_ADMIN_USER:-postgres}

echo "Using PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}"

# Function to check if PostgreSQL is running
check_postgres() {
    echo "Checking if PostgreSQL is accessible..."
    if pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" > /dev/null 2>&1; then
        echo "✓ PostgreSQL is running and accessible"
        return 0
    else
        echo "✗ PostgreSQL is not accessible"
        return 1
    fi
}

# Function to create database if it doesn't exist
create_database() {
    echo "Checking if database '$POSTGRES_DB' exists..."
    
    # Check if database exists
    if psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"; then
        echo "✓ Database '$POSTGRES_DB' already exists"
    else
        echo "Creating database '$POSTGRES_DB'..."
        psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -c "CREATE DATABASE $POSTGRES_DB;"
        echo "✓ Database '$POSTGRES_DB' created successfully"
    fi
}

# Function to create user if it doesn't exist
create_user() {
    echo "Checking if user '$POSTGRES_USER' exists..."
    
    # Check if user exists
    if psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -tc "SELECT 1 FROM pg_user WHERE usename = '$POSTGRES_USER'" | grep -q 1; then
        echo "✓ User '$POSTGRES_USER' already exists"
    else
        echo "Creating user '$POSTGRES_USER'..."
        psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
        echo "✓ User '$POSTGRES_USER' created successfully"
    fi
}

# Function to grant privileges
grant_privileges() {
    echo "Granting privileges to user '$POSTGRES_USER' on database '$POSTGRES_DB'..."
    psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"
    psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_ADMIN_USER" -c "ALTER USER $POSTGRES_USER CREATEDB;"
    echo "✓ Privileges granted successfully"
}

# Function to run Django migrations
run_migrations() {
    echo "Running Django migrations..."
    
    # Change to Django project directory
    cd /app/FamilyHub 2>/dev/null || cd FamilyHub 2>/dev/null || echo "Warning: Could not change to FamilyHub directory"
    
    # Run migrations for all apps
    python manage.py migrate --noinput
    echo "✓ Django migrations completed successfully"
}

# Main execution
main() {
    echo "Starting database initialization process..."
    
    # Wait for PostgreSQL to be ready
    if ! check_postgres; then
        echo "Waiting for PostgreSQL to become available..."
        sleep 5
        if ! check_postgres; then
            echo "✗ PostgreSQL is still not accessible. Exiting."
            exit 1
        fi
    fi
    
    # Create database and user
    create_database
    create_user
    grant_privileges
    
    # Run Django migrations
    run_migrations
    
    echo "=== Database initialization completed successfully ==="
}

# Execute main function
main "$@"
