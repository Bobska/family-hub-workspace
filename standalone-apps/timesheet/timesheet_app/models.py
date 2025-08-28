from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from decimal import Decimal


class Job(models.Model):
    """Model representing a job/work location for timesheet entries."""
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, help_text="Job description or notes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'address']
        unique_together = ['user', 'name', 'address']

    def clean(self):
        """Validate that either name or address is provided."""
        if not self.name and not self.address:
            raise ValidationError("Either job name or address must be provided")

    def display_name(self):
        """Return name if exists, otherwise return address."""
        if self.name:
            return self.name
        return self.address if self.address else "Unnamed Job"

    @property
    def total_entries(self):
        """Return total number of time entries for this job."""
        return self.time_entries.count()

    def total_hours(self):
        """Calculate total hours worked for this job."""
        return sum(entry.total_hours() for entry in self.time_entries.all())

    def __str__(self):
        return self.display_name()


class TimeEntry(models.Model):
    """Model representing a time entry for work tracking."""
    
    BREAK_CHOICES = [
        (0, 'No break'),
        (30, '30 minutes'),
        (60, '1 hour'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_entries')
    job = models.ForeignKey(
        Job, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='time_entries'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.IntegerField(choices=BREAK_CHOICES, default=0, help_text="Break duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        unique_together = ['user', 'date', 'start_time']

    def clean(self):
        """Validate time entry for overlaps and logical consistency."""
        super().clean()
        
        # Ensure end time is after start time
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')
        
        # Check for overlapping entries only if all required fields are present
        if hasattr(self, 'user') and self.user and self.date and self.start_time and self.end_time:
            overlapping_entries = TimeEntry.objects.filter(
                user=self.user,
                date=self.date
            ).exclude(pk=self.pk)
            
            for entry in overlapping_entries:
                # Check if this entry overlaps with existing entries
                if (self.start_time < entry.end_time and self.end_time > entry.start_time):
                    raise ValidationError(
                        f"Time overlaps with: {entry.start_time.strftime('%H:%M')} - {entry.end_time.strftime('%H:%M')} at {entry.job}"
                    )

    def total_hours(self):
        """Calculate total hours worked minus break duration."""
        if not self.start_time or not self.end_time:
            return Decimal('0.00')
        
        # Calculate total time worked
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time)
        
        # Handle overnight shifts
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)
        
        total_time = end_datetime - start_datetime
        total_minutes = total_time.total_seconds() / 60
        
        # Subtract break duration
        work_minutes = total_minutes - self.break_duration
        
        # Convert to hours (decimal)
        hours = Decimal(str(work_minutes / 60)).quantize(Decimal('0.01'))
        return max(hours, Decimal('0.00'))

    def total_hours_timedelta(self):
        """Return total hours as timedelta for calculations"""
        from datetime import datetime, timedelta
        
        # Create datetime objects for time calculation
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        
        # Handle overnight shifts
        if end < start:
            end += timedelta(days=1)
        
        # Calculate total time and subtract break
        total = end - start
        break_time = timedelta(minutes=self.break_duration)
        
        return total - break_time

    def __str__(self):
        job_name = self.job.display_name() if self.job else "No Job Assigned"
        return f"{self.user.username} - {job_name} - {self.date} ({self.total_hours()}h)"
