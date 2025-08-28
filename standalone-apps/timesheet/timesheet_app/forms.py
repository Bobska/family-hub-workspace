from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Job, TimeEntry


class JobForm(forms.ModelForm):
    """Form for creating and editing jobs."""
    
    class Meta:
        model = Job
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job name (optional)'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job address (optional)'
            }),
        }

    def clean(self):
        """Ensure at least one of name or address is provided."""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')
        
        if not name and not address:
            raise ValidationError('Please provide either a job name or address.')
        
        return cleaned_data


class TimeEntryForm(forms.ModelForm):
    """Form for creating and editing time entries."""
    
    class Meta:
        model = TimeEntry
        fields = ['job', 'date', 'start_time', 'end_time', 'break_duration']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'break_duration': forms.Select(attrs={
                'class': 'form-select'
            }),
            'job': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter jobs by the current user
            self.fields['job'].queryset = Job.objects.filter(user=user)
            
        # Add helpful labels
        self.fields['break_duration'].help_text = "Select break duration"
        self.fields['job'].help_text = "Select the job for this time entry"

    def clean(self):
        """Validate the time entry form."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError('End time must be after start time.')
        
        return cleaned_data


class QuickTimeEntryForm(forms.ModelForm):
    """Simplified form for quick time entry on dashboard."""
    
    class Meta:
        model = TimeEntry
        fields = ['job', 'start_time', 'end_time', 'break_duration']
        widgets = {
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control form-control-sm'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control form-control-sm'
            }),
            'break_duration': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
            'job': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['job'].queryset = Job.objects.filter(user=user)


class DateFilterForm(forms.Form):
    """Form for filtering entries by date."""
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        help_text="Select date to view entries"
    )
