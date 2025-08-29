-- FamilyHub PostgreSQL Initialization Script
-- Quick setup for development environment

-- Create additional user if needed
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'familyhub_user') THEN
        CREATE USER familyhub_user WITH PASSWORD 'familyhub123';
    END IF;
END $$;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE familyhub TO familyhub_user;
GRANT ALL PRIVILEGES ON DATABASE familyhub TO django;

-- Create extensions commonly used in Django projects
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set timezone
SET timezone = 'Pacific/Auckland';

-- Create initial schema (Django will handle this with migrations)
-- This is just for reference

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'FamilyHub PostgreSQL 17.6 initialized successfully!';
    RAISE NOTICE 'Database: familyhub';
    RAISE NOTICE 'Primary user: django';
    RAISE NOTICE 'Additional user: familyhub_user';
    RAISE NOTICE 'Extensions: uuid-ossp, pgcrypto';
    RAISE NOTICE 'Timezone: Pacific/Auckland';
END $$;
