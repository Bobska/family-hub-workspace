-- FamilyHub PostgreSQL Initialization Script
-- This script runs when PostgreSQL container starts for the first time

-- Create the familyhub database if it doesn't exist
SELECT 'CREATE DATABASE familyhub' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'familyhub')\gexec

-- Create the familyhub user with appropriate permissions
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles 
      WHERE  rolname = 'familyhub_user') THEN
      
      CREATE ROLE familyhub_user LOGIN PASSWORD 'changeme123';
   END IF;
END
$$;

-- Grant privileges to familyhub_user
GRANT ALL PRIVILEGES ON DATABASE familyhub TO familyhub_user;

-- Connect to familyhub database
\c familyhub;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO familyhub_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO familyhub_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO familyhub_user;

-- Create extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set up performance optimizations
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET max_connections = '200';
ALTER SYSTEM SET effective_cache_size = '4GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
ALTER SYSTEM SET checkpoint_completion_target = '0.9';
ALTER SYSTEM SET wal_buffers = '64MB';
ALTER SYSTEM SET default_statistics_target = '100';
ALTER SYSTEM SET random_page_cost = '1.1';

-- Log configuration for better monitoring
ALTER SYSTEM SET log_min_duration_statement = '1000';
ALTER SYSTEM SET log_checkpoints = 'on';
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_lock_waits = 'on';

SELECT pg_reload_conf();
