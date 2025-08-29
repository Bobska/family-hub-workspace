from django.shortcuts import render
from datetime import datetime
import subprocess
import socket

def check_port_status(host, port):
    """Check if a port is accessible"""
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (socket.timeout, socket.error):
        return False

def get_environment_status():
    """Get development environment status"""
    services = {
        'familyhub': check_port_status('127.0.0.1', 8000),
        'timesheet_app': check_port_status('127.0.0.1', 8001),
        'postgresql': check_port_status('127.0.0.1', 5432),
        'redis': check_port_status('127.0.0.1', 6379),
        'pgadmin': check_port_status('127.0.0.1', 5050)
    }
    
    # Overall health metrics
    running_services = sum(1 for service in services.values() if service)
    total_services = len(services)
    health_score = (running_services / total_services) * 100
    
    status = {
        'services': services,
        'health_score': health_score,
        'running_count': running_services,
        'total_count': total_services,
        'database': 'PostgreSQL' if services['postgresql'] else 'SQLite',
        'cache': 'Redis' if services['redis'] else 'File-based'
    }
    
    return status

def home_dashboard(request):
    """Main dashboard view showing all apps overview"""
    
    # Get environment status
    env_status = get_environment_status()
    
    # Prepare app cards with their information
    apps = [
        {
            'name': 'Timesheet Tracker',
            'icon': '⏰',
            'description': 'Track work hours, jobs, and calculate pay',
            'url': 'http://127.0.0.1:8001/' if env_status['services']['timesheet_app'] else '#',
            'admin_url': 'http://127.0.0.1:8001/admin/',
            'color': 'primary',
            'status': 'running' if env_status['services']['timesheet_app'] else 'stopped',
            'features': [
                'Job management',
                'Time entry tracking',
                'Break time calculation',
                'Pay rate calculations',
                'Daily summaries'
            ]
        },
        {
            'name': 'Daycare Invoice Tracker',
            'icon': '🧸',
            'description': 'Manage daycare payments and invoicing',
            'url': '/daycare/',
            'admin_url': '/admin/',
            'color': 'success',
            'status': 'development',
            'features': [
                'Invoice management',
                'Payment tracking',
                'Due date reminders',
                'Financial reports'
            ]
        },
        {
            'name': 'Employment History',
            'icon': '📋',
            'description': 'Track career history and employment records',
            'url': '/employment/',
            'admin_url': '/admin/',
            'color': 'info',
            'status': 'planned',
            'features': [
                'Job history',
                'Resume building',
                'Skills tracking',
                'Achievement records'
            ]
        },
        {
            'name': 'Upcoming Payments',
            'icon': '�',
            'description': 'Track bills, subscriptions, and payment due dates',
            'url': '/payments/',
            'admin_url': '/admin/',
            'color': 'warning',
            'status': 'planned',
            'features': [
                'Bill reminders',
                'Payment scheduling',
                'Budget planning',
                'Expense categorization'
            ]
        },
        {
            'name': 'Credit Card Management',
            'icon': '�',
            'description': 'Monitor credit card usage and payments',
            'url': '/creditcards/',
            'admin_url': '/admin/',
            'color': 'danger',
            'status': 'planned',
            'features': [
                'Balance tracking',
                'Payment reminders',
                'Interest calculations',
                'Spending analysis'
            ]
        },
        {
            'name': 'Household Budget',
            'icon': '🏠',
            'description': 'Comprehensive family budget management',
            'url': '/budget/',
            'admin_url': '/admin/',
            'color': 'secondary',
            'status': 'planned',
            'features': [
                'Income tracking',
                'Expense management',
                'Savings goals',
                'Financial reports'
            ]
        }
    ]
    
    # Development info for status display
    development_info = {
        'mode': 'Development',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'environment': env_status,
    }
    
    context = {
        'title': 'FamilyHub Dashboard',
        'apps': apps,
        'user': request.user,
        'today': datetime.now(),
        'environment_status': env_status,
        'development_info': development_info,
    }
    
    return render(request, 'home/dashboard.html', context)
