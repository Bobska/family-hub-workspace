#!/usr/bin/env python3
"""
PostgreSQL connection wait script for FamilyHub.

This script attempts to connect to PostgreSQL using psycopg2,
retries every 2 seconds for up to 30 seconds, and exits with
appropriate status codes.
"""

import os
import sys
import time
import psycopg2
from psycopg2 import OperationalError


def get_db_config():
    """Get database configuration from environment variables."""
    return {
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': os.environ.get('POSTGRES_PORT', '5432'),
        'database': os.environ.get('POSTGRES_DB', 'familyhub_db'),
        'user': os.environ.get('POSTGRES_USER', 'familyhub_user'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'TempPass123!ChangeMe'),
    }


def test_connection(config):
    """Test PostgreSQL connection with given configuration."""
    try:
        conn = psycopg2.connect(**config)
        conn.close()
        return True
    except OperationalError:
        return False


def wait_for_postgres(max_attempts=15, retry_interval=2):
    """
    Wait for PostgreSQL to become available.
    
    Args:
        max_attempts (int): Maximum number of connection attempts (default: 15)
        retry_interval (int): Seconds to wait between attempts (default: 2)
    
    Returns:
        bool: True if connection successful, False if timeout
    """
    config = get_db_config()
    
    print(f"Waiting for PostgreSQL at {config['host']}:{config['port']}...")
    print(f"Database: {config['database']}, User: {config['user']}")
    
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}: Testing connection...")
        
        if test_connection(config):
            print("✓ PostgreSQL is ready and accepting connections!")
            return True
        
        if attempt < max_attempts:
            print(f"✗ Connection failed. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            print("✗ Connection failed. No more retries.")
    
    print(f"✗ Timeout: PostgreSQL not available after {max_attempts * retry_interval} seconds")
    return False


def main():
    """Main function to wait for PostgreSQL."""
    try:
        if wait_for_postgres():
            print("PostgreSQL connection successful!")
            sys.exit(0)
        else:
            print("Failed to connect to PostgreSQL within timeout period.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
