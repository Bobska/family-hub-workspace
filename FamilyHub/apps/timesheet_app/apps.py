from django.apps import AppConfig


class TimesheetAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timesheet_app'  # Just the app name, since apps/ is in Python path
