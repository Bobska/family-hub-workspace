# FamilyHub Celery Configuration
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.production')

app = Celery('FamilyHub')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configure broker and result backend
app.conf.update(
    # Broker settings
    broker_url=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1'),
    
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Result settings
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Performance settings
    task_compression='gzip',
    result_compression='gzip',
    
    # Task routing
    task_routes={
        'FamilyHub.home.tasks.*': {'queue': 'default'},
        'FamilyHub.timesheet.tasks.*': {'queue': 'timesheet'},
        'FamilyHub.*.tasks.backup_*': {'queue': 'backup'},
        'FamilyHub.*.tasks.email_*': {'queue': 'email'},
    },
    
    # Queue configuration
    task_default_queue='default',
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
        'timesheet': {
            'exchange': 'timesheet',
            'routing_key': 'timesheet',
        },
        'backup': {
            'exchange': 'backup',
            'routing_key': 'backup',
        },
        'email': {
            'exchange': 'email',
            'routing_key': 'email',
        },
    },
)

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# Debug task for testing
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Health check task
@app.task
def health_check():
    """Basic health check task for monitoring"""
    return "Celery is working!"

# Example tasks for demonstration
@app.task
def cleanup_old_sessions():
    """Cleanup expired sessions"""
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    from datetime import timedelta
    
    expired_sessions = Session.objects.filter(
        expire_date__lt=timezone.now() - timedelta(days=7)
    )
    count = expired_sessions.count()
    expired_sessions.delete()
    return f"Cleaned up {count} expired sessions"

@app.task
def generate_reports():
    """Generate scheduled reports"""
    from django.core.management import call_command
    
    # Example: Generate timesheet reports
    try:
        call_command('generate_timesheet_reports')
        return "Reports generated successfully"
    except Exception as e:
        return f"Report generation failed: {str(e)}"

@app.task
def backup_database():
    """Backup database task"""
    import subprocess
    import os
    from datetime import datetime
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"/app/backups/familyhub_backup_{timestamp}.sql"
        
        # Create backup using pg_dump
        cmd = [
            'pg_dump',
            '-h', os.environ.get('POSTGRES_HOST', 'postgres'),
            '-U', os.environ.get('POSTGRES_USER', 'familyhub_user'),
            '-d', os.environ.get('POSTGRES_DB', 'familyhub'),
            '-f', backup_file
        ]
        
        subprocess.run(cmd, check=True, env={
            **os.environ,
            'PGPASSWORD': os.environ.get('POSTGRES_PASSWORD', '')
        })
        
        return f"Database backup created: {backup_file}"
    except Exception as e:
        return f"Database backup failed: {str(e)}"
