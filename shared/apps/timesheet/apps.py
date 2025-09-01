from django.apps import AppConfig


class SharedTimesheetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared.apps.timesheet'  # Full dotted path from Python path
    verbose_name = 'Shared Timesheet Components'
