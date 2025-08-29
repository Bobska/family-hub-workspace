"""
Context processors for Timesheet app.
Provides global template context for environment and server information.
"""

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
    if hasattr(settings, 'DEBUG') and settings.DEBUG:
        environment = 'Development'
        env_class = 'warning'
        env_icon = '🔧'
    else:
        environment = 'Production'
        env_class = 'danger'
        env_icon = '🚀'
    
    # Get server information
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    if allowed_hosts and allowed_hosts[0] not in ['*', '0.0.0.0']:
        server_host = allowed_hosts[0]
    else:
        server_host = 'localhost'
    
    if server_host in ['*', '0.0.0.0']:
        server_host = 'All Interfaces'
    
    # Determine server type and database
    server_type = 'Django Development Server'
    database_engine = 'SQLite'
    
    if hasattr(settings, 'DATABASES'):
        db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
        if 'postgresql' in db_engine:
            database_engine = 'PostgreSQL'
        elif 'mysql' in db_engine:
            database_engine = 'MySQL'
        elif 'sqlite' in db_engine:
            database_engine = 'SQLite'
        elif 'sqlserver' in db_engine:
            database_engine = 'SQL Server'
    
    # Get current port from request
    port = request.get_port() if hasattr(request, 'get_port') else '8001'
    
    # Build server URL
    protocol = 'https' if request.is_secure() else 'http'
    current_host = request.get_host() if hasattr(request, 'get_host') else f'localhost:{port}'
    server_url = f"{protocol}://{current_host}"
    
    return {
        'environment_info': {
            'mode': environment,
            'mode_class': env_class,
            'mode_icon': env_icon,
            'debug': getattr(settings, 'DEBUG', False),
            'server_type': server_type,
            'server_host': server_host,
            'server_url': server_url,
            'port': port,
            'database': database_engine,
            'app_name': 'Timesheet',
            'settings_module': getattr(settings, 'SETTINGS_MODULE', 'Unknown'),
        }
    }
