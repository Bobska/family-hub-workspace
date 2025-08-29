#!/bin/bash
# PostgreSQL Initialization Script
# This script runs when the PostgreSQL container is first created

set -e

echo "🚀 Initializing FamilyHub PostgreSQL Database..."

# Create additional databases if needed
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    
    -- Create additional schemas
    CREATE SCHEMA IF NOT EXISTS timesheet;
    CREATE SCHEMA IF NOT EXISTS daycare_invoice;
    CREATE SCHEMA IF NOT EXISTS employment_history;
    CREATE SCHEMA IF NOT EXISTS upcoming_payments;
    CREATE SCHEMA IF NOT EXISTS credit_card_mgmt;
    CREATE SCHEMA IF NOT EXISTS household_budget;
    
    -- Grant permissions
    GRANT ALL PRIVILEGES ON SCHEMA timesheet TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON SCHEMA daycare_invoice TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON SCHEMA employment_history TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON SCHEMA upcoming_payments TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON SCHEMA credit_card_mgmt TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON SCHEMA household_budget TO $POSTGRES_USER;
    
    -- Create indexes for performance
    -- These will be used by Django models
EOSQL

echo "✅ FamilyHub PostgreSQL Database initialized successfully!"
