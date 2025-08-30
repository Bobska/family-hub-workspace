#!/usr/bin/env python3
"""
Switch to Docker deployment script for FamilyHub.

This script switches from local development to Docker-based deployment
by backing up current settings and configuring for Docker Compose.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def backup_current_env():
    """Backup current .env file as .env.local with timestamp."""
    print("Backing up current environment configuration...")
    
    env_file = Path('.env')
    if env_file.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'.env.local.backup_{timestamp}'
        backup_file = Path(backup_name)
        
        shutil.copy2(env_file, backup_file)
        print(f"✓ Current .env backed up as: {backup_file.absolute()}")
        
        # Also create a standard .env.local backup
        env_local = Path('.env.local')
        shutil.copy2(env_file, env_local)
        print(f"✓ Current .env also saved as: {env_local.absolute()}")
        
        return backup_file
    else:
        print("ℹ No existing .env file found to backup")
        return None


def copy_docker_env():
    """Copy .env.docker to .env for Docker deployment."""
    print("\nConfiguring Docker environment...")
    
    docker_env = Path('.env.docker')
    if not docker_env.exists():
        print("✗ .env.docker file not found!")
        print("Please ensure .env.docker exists with Docker configuration")
        return False
    
    env_file = Path('.env')
    shutil.copy2(docker_env, env_file)
    print(f"✓ Copied {docker_env.name} to {env_file.name}")
    
    return True


def update_settings_module():
    """Update DJANGO_SETTINGS_MODULE in .env for Docker."""
    print("\nUpdating Django settings module...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("✗ .env file not found!")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Update DJANGO_SETTINGS_MODULE
    lines = content.split('\n')
    updated_lines = []
    settings_updated = False
    
    for line in lines:
        if line.startswith('DJANGO_SETTINGS_MODULE='):
            updated_lines.append('DJANGO_SETTINGS_MODULE=FamilyHub.settings.docker')
            settings_updated = True
        else:
            updated_lines.append(line)
    
    # Add if not found
    if not settings_updated:
        updated_lines.append('DJANGO_SETTINGS_MODULE=FamilyHub.settings.docker')
    
    # Write back
    with open(env_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print("✓ Updated DJANGO_SETTINGS_MODULE to use docker settings")
    return True


def check_docker_files():
    """Check if required Docker files exist."""
    print("\nChecking Docker configuration files...")
    
    required_files = [
        'docker-compose.yml',
        'Dockerfile',
        '.env.docker'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✓ Found {file}")
    
    if missing_files:
        print(f"\n✗ Missing required files: {', '.join(missing_files)}")
        return False
    
    return True


def display_instructions():
    """Display instructions for running Docker deployment."""
    print("\n" + "=" * 60)
    print("✓ Switch to Docker deployment completed successfully!")
    print("=" * 60)
    print("""
Docker Deployment Instructions:
==============================

1. Build and start the services:
   docker-compose up --build

2. Or run in background:
   docker-compose up -d --build

3. View logs:
   docker-compose logs -f

4. Stop services:
   docker-compose down

5. Stop and remove volumes (careful - removes database data):
   docker-compose down -v

6. Access the application:
   - FamilyHub: http://localhost:8000
   - PostgreSQL: localhost:5432
   - Default admin credentials: admin / admin123

Database Information:
====================
- Host: localhost (from host machine) or db (from containers)
- Port: 5432
- Database: familyhub_db
- Username: familyhub_user
- Password: TempPass123!ChangeMe

Useful Commands:
===============
- Execute Django commands in container:
  docker-compose exec web python manage.py <command>

- Access PostgreSQL shell:
  docker-compose exec db psql -U familyhub_user -d familyhub_db

- View container status:
  docker-compose ps

- Rebuild specific service:
  docker-compose build web

Switch Back to Local Development:
=================================
If you want to switch back to local development:
1. Copy .env.local back to .env
2. Ensure PostgreSQL is running locally
3. Update DJANGO_SETTINGS_MODULE if needed

Environment Backup:
==================
Your previous environment settings have been backed up.
Check for .env.local and .env.local.backup_* files.
""")


def main():
    """Main function to switch to Docker deployment."""
    print("=" * 60)
    print("FamilyHub - Switch to Docker Deployment")
    print("=" * 60)
    
    # Check if Docker files exist
    if not check_docker_files():
        print("\n✗ Missing required Docker files. Cannot proceed.")
        return False
    
    # Backup current environment
    backup_file = backup_current_env()
    
    # Copy Docker environment
    if not copy_docker_env():
        print("\n✗ Failed to configure Docker environment")
        return False
    
    # Update settings module
    if not update_settings_module():
        print("\n✗ Failed to update Django settings module")
        return False
    
    # Display instructions
    display_instructions()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n✗ Failed to switch to Docker deployment")
            exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        exit(1)
