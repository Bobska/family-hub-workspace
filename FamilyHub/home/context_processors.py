"""
Context processors for FamilyHub home app.
Provides global template context for environment and server information.
"""

import os
import socket
from django.conf import settings
from django.http import HttpRequest


def environment_context(request: HttpRequest) -> dict:
    """
    Add environment and server information to template context.
    
    Returns:
        dict: Context data including environment, server info, and host details
    """
    # Determine environment mode
    debug = getattr(settings, 'DEBUG', False)
    if debug:
        environment = 'Development'
        env_class = 'warning'
        env_icon = '🔧'
    else:
        environment = 'Production'
        env_class = 'danger'
        env_icon = '🚀'
    
    # Check if running in Docker
    in_docker = os.path.exists('/.dockerenv')
    
    # Get server information
    if in_docker:
        server_type = 'Django in Docker'
        environment_label = 'Docker'
    else:
        server_type = 'Native Django'
        environment_label = 'Local'
    # Determine database type
    database_engine = 'SQLite'
    if hasattr(settings, 'DATABASES'):
        db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
        if 'postgresql' in db_engine:
            database_engine = 'PostgreSQL'
        elif 'mysql' in db_engine:
            database_engine = 'MySQL'
        elif 'sqlite' in db_engine:
            database_engine = 'SQLite'
        elif 'mssql' in db_engine or 'sql_server' in db_engine:
            database_engine = 'SQL Server'
    
    # Get server host from request
    server_host = request.get_host() if hasattr(request, 'get_host') else 'localhost:8000'
    
    # Build server URL
    protocol = 'https' if request.is_secure() else 'http'
    server_url = f"{protocol}://{server_host}"
    
    return {
        'debug': debug,
        'database_engine': database_engine,
        'in_docker': in_docker,
        'server_host': server_host,
        'environment_label': environment_label,
        'environment_info': {
            'mode': environment,
            'mode_class': env_class,
            'mode_icon': env_icon,
            'debug': debug,
            'server_type': server_type,
            'server_host': server_host,
            'server_url': server_url,
            'database': database_engine,
            'docker_mode': in_docker,
            'environment_label': environment_label,
        }
    }
