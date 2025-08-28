from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date, time
from timesheet_app.models import Job, TimeEntry


class Command(BaseCommand):
    help = 'Test timesheet model methods and optimizations'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=== Timesheet Model Testing ===\n'))
        
        # Test total_hours_timedelta method if we have entries
        entries = TimeEntry.objects.all()[:3]  # Get a few entries to test
        
        if entries.exists():
            self.stdout.write('Testing total_hours_timedelta() method:')
            for entry in entries:
                decimal_hours = entry.total_hours()
                timedelta_result = entry.total_hours_timedelta()
                hours_from_timedelta = timedelta_result.total_seconds() / 3600
                
                self.stdout.write(f'  Entry: {entry.start_time} - {entry.end_time}')
                self.stdout.write(f'    Decimal hours: {decimal_hours}')
                self.stdout.write(f'    Timedelta: {timedelta_result}')
                self.stdout.write(f'    Hours from timedelta: {hours_from_timedelta:.2f}')
                self.stdout.write('')
        else:
            self.stdout.write(self.style.WARNING('No time entries found to test.'))
        
        # Test job query optimization
        self.stdout.write('Testing Job query optimization:')
        jobs_with_counts = Job.objects.annotate(
            entry_count=Count('time_entries')
        )[:3]
        
        for job in jobs_with_counts:
            self.stdout.write(f'  Job: {job.display_name()}')
            self.stdout.write(f'    Annotated entry count: {job.entry_count}')
            self.stdout.write(f'    Property entry count: {job.total_entries}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('=== Testing Complete ==='))
