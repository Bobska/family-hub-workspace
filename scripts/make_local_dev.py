#!/usr/bin/env python3
"""
Local PostgreSQL 17 development setup script for FamilyHub.

This script sets up PostgreSQL 17 connection for local development
without Docker by creating the database, user, and configuring
Django settings.
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path


def run_command(command, capture_output=True, shell=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=capture_output, 
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"Error running command '{command}': {e.stderr}")
        return None


def check_postgresql_installed():
    """Check if PostgreSQL 17 is installed locally."""
    print("Checking PostgreSQL installation...")
    
    version_output = run_command("psql --version")
    if not version_output:
        print("✗ PostgreSQL is not installed or not in PATH")
        print("Please install PostgreSQL 17 and add it to your PATH")
        return False
    
    print(f"✓ Found PostgreSQL: {version_output}")
    
    # Check if it's version 17 or compatible
    if "17" in version_output or any(v in version_output for v in ["15", "16", "17", "18"]):
        return True
    else:
        print("⚠ Warning: PostgreSQL version might not be compatible")
        return True  # Continue anyway


def get_admin_credentials():
    """Prompt user for PostgreSQL admin credentials."""
    print("\nPostgreSQL Admin Credentials")
    print("=" * 35)
    
    username = input("PostgreSQL admin username (default: postgres): ").strip()
    if not username:
        username = "postgres"
    
    password = getpass.getpass("PostgreSQL admin password: ")
    
    host = input("PostgreSQL host (default: localhost): ").strip()
    if not host:
        host = "localhost"
    
    port = input("PostgreSQL port (default: 5432): ").strip()
    if not port:
        port = "5432"
    
    return {
        'username': username,
        'password': password,
        'host': host,
        'port': port
    }


def create_database_and_user(admin_creds):
    """Create the FamilyHub database and user."""
    print("\nCreating database and user...")
    
    # Set PGPASSWORD for non-interactive psql
    env = os.environ.copy()
    env['PGPASSWORD'] = admin_creds['password']
    
    db_name = 'familyhub_db'
    db_user = 'familyhub_user'
    db_password = input(f"Enter password for new user '{db_user}': ").strip()
    if not db_password:
        db_password = 'familyhub_dev_pass'
        print(f"Using default password: {db_password}")
    
    # Check if database exists
    check_db_cmd = f"psql -h {admin_creds['host']} -p {admin_creds['port']} -U {admin_creds['username']} -lqt"
    db_list = run_command(check_db_cmd, capture_output=True)
    
    if db_list and db_name in db_list:
        print(f"✓ Database '{db_name}' already exists")
    else:
        # Create database
        create_db_cmd = f"psql -h {admin_creds['host']} -p {admin_creds['port']} -U {admin_creds['username']} -c \"CREATE DATABASE {db_name};\""
        if run_command(create_db_cmd, capture_output=False) is not None:
            print(f"✓ Database '{db_name}' created successfully")
        else:
            print(f"✗ Failed to create database '{db_name}'")
            return None
    
    # Check if user exists
    check_user_cmd = f"psql -h {admin_creds['host']} -p {admin_creds['port']} -U {admin_creds['username']} -tc \"SELECT 1 FROM pg_user WHERE usename = '{db_user}'\""
    user_exists = run_command(check_user_cmd, capture_output=True)
    
    if user_exists and '1' in user_exists:
        print(f"✓ User '{db_user}' already exists")
    else:
        # Create user
        create_user_cmd = f"psql -h {admin_creds['host']} -p {admin_creds['port']} -U {admin_creds['username']} -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\""
        if run_command(create_user_cmd, capture_output=False) is not None:
            print(f"✓ User '{db_user}' created successfully")
        else:
            print(f"✗ Failed to create user '{db_user}'")
            return None
    
    # Grant privileges
    grant_cmd = f"psql -h {admin_creds['host']} -p {admin_creds['port']} -U {admin_creds['username']} -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}; ALTER USER {db_user} CREATEDB;\""
    if run_command(grant_cmd, capture_output=False) is not None:
        print(f"✓ Privileges granted to '{db_user}'")
    else:
        print(f"✗ Failed to grant privileges to '{db_user}'")
        return None
    
    return {
        'database': db_name,
        'user': db_user,
        'password': db_password,
        'host': admin_creds['host'],
        'port': admin_creds['port']
    }


def create_env_file(db_config):
    """Create .env file with local PostgreSQL connection details."""
    print("\nCreating .env file...")
    
    env_content = f"""# Django Settings for Local Development
DEBUG=True
SECRET_KEY=django-local-dev-secret-key-change-in-production
DJANGO_SETTINGS_MODULE=FamilyHub.settings.docker

# Local Development Environment
IS_DOCKER=False

# Local PostgreSQL Connection Settings
POSTGRES_DB={db_config['database']}
POSTGRES_USER={db_config['user']}
POSTGRES_PASSWORD={db_config['password']}
POSTGRES_HOST={db_config['host']}
POSTGRES_PORT={db_config['port']}

# Database URL for Django
DATABASE_URL=postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Superuser Settings
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@familyhub.local
DJANGO_SUPERUSER_PASSWORD=admin123
"""
    
    env_file = Path('.env')
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✓ Created {env_file.absolute()}")
    return env_file


def test_django_connection():
    """Test Django database connection."""
    print("\nTesting Django database connection...")
    
    # Change to FamilyHub directory
    familyhub_dir = Path('FamilyHub')
    if not familyhub_dir.exists():
        print("✗ FamilyHub directory not found")
        return False
    
    os.chdir(familyhub_dir)
    
    # Test database connection
    test_cmd = "python manage.py check --database default"
    if run_command(test_cmd, capture_output=False) is not None:
        print("✓ Django database connection successful")
        return True
    else:
        print("✗ Django database connection failed")
        return False


def run_migrations():
    """Run Django migrations."""
    print("\nRunning Django migrations...")
    
    migrate_cmd = "python manage.py migrate"
    if run_command(migrate_cmd, capture_output=False) is not None:
        print("✓ Django migrations completed successfully")
        return True
    else:
        print("✗ Django migrations failed")
        return False


def create_superuser():
    """Create Django superuser."""
    print("\nCreating Django superuser...")
    
    superuser_cmd = "python manage.py init_superuser"
    if run_command(superuser_cmd, capture_output=False) is not None:
        print("✓ Django superuser created successfully")
        return True
    else:
        print("✗ Django superuser creation failed")
        return False


def main():
    """Main function to set up local PostgreSQL development."""
    print("=" * 60)
    print("FamilyHub Local PostgreSQL 17 Development Setup")
    print("=" * 60)
    
    # Check if PostgreSQL is installed
    if not check_postgresql_installed():
        sys.exit(1)
    
    # Get admin credentials
    admin_creds = get_admin_credentials()
    
    # Create database and user
    db_config = create_database_and_user(admin_creds)
    if not db_config:
        print("\n✗ Failed to set up database and user")
        sys.exit(1)
    
    # Create .env file
    env_file = create_env_file(db_config)
    
    # Test Django connection
    if not test_django_connection():
        print("\n✗ Failed to establish Django database connection")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("\n✗ Failed to run Django migrations")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("\n⚠ Warning: Failed to create superuser automatically")
        print("You can create one manually using: python manage.py createsuperuser")
    
    print("\n" + "=" * 60)
    print("✓ Local PostgreSQL development setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. cd FamilyHub")
    print("2. python manage.py runserver")
    print("3. Open http://localhost:8000 in your browser")
    print(f"\nDatabase connection details saved to: {env_file.absolute()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
