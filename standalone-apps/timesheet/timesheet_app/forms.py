from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from .models import Job, TimeEntry


class JobForm(forms.ModelForm):
    """Form for creating and editing jobs."""
    
    class Meta:
        model = Job
        fields = ['name', 'address', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job name (required if no address)'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job address (required if no name)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional job description or notes'
            }),
        }

    def clean(self):
        """Ensure at least one of name or address is provided."""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')
        
        if not name and not address:
            raise forms.ValidationError(
                'Please provide either a job name or address (or both)'
            )
        
        return cleaned_data


class TimeEntryForm(forms.ModelForm):
    """Form for creating and editing time entries."""
    
    class Meta:
        model = TimeEntry
        fields = ['job', 'date', 'start_time', 'end_time', 'break_duration']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'max': date.today().strftime('%Y-%m-%d')
                },
                format='%Y-%m-%d'
            ),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                },
                format='%H:%M'
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                },
                format='%H:%M'
            ),
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
        
        # Format existing values for editing
        if self.instance and self.instance.pk:
            if self.instance.date:
                self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')
            if self.instance.start_time:
                self.initial['start_time'] = self.instance.start_time.strftime('%H:%M')
            if self.instance.end_time:
                self.initial['end_time'] = self.instance.end_time.strftime('%H:%M')

    def clean_date(self):
        """Validate that the date is not in the future."""
        entry_date = self.cleaned_data.get('date')
        if entry_date and entry_date > date.today():
            raise ValidationError("Cannot add entries for future dates")
        return entry_date

    def clean(self):
        """Validate the time entry form."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        entry_date = cleaned_data.get('date')
        
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
            'class': 'form-control',
            'max': date.today().strftime('%Y-%m-%d')  # Prevent future dates
        }),
        help_text="Select date to view entries"
    )
    
    def clean_date(self):
        """Validate that the selected date is not in the future."""
        selected_date = self.cleaned_data['date']
        if selected_date > date.today():
            raise ValidationError("Cannot select future dates")
        return selected_date
