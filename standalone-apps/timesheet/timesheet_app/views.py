from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from decimal import Decimal
from .models import Job, TimeEntry
from .forms import JobForm, TimeEntryForm, QuickTimeEntryForm, DateFilterForm


@login_required
def dashboard(request):
    """Dashboard view showing today's overview with quick entry form."""
    today = timezone.now().date()
    
    # Get today's entries
    today_entries = TimeEntry.objects.filter(
        user=request.user,
        date=today
    ).select_related('job').order_by('start_time')
    
    # Calculate today's total hours
    today_total = sum(entry.total_hours() for entry in today_entries)
    
    # Handle quick entry form
    if request.method == 'POST':
        form = QuickTimeEntryForm(user=request.user, data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = today
            try:
                entry.full_clean()
                entry.save()
                messages.success(request, 'Time entry added successfully!')
                return redirect('timesheet:dashboard')
            except ValidationError as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickTimeEntryForm(user=request.user)
    
    context = {
        'today': today,
        'today_entries': today_entries,
        'today_total': today_total,
        'form': form,
        'has_jobs': Job.objects.filter(user=request.user).exists(),
    }
    return render(request, 'timesheet/dashboard.html', context)


@login_required
def daily_entry(request):
    """Daily entry view with date picker to select any date."""
    # Get date from GET parameter or default to today
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    # Get entries for selected date
    entries = TimeEntry.objects.filter(
        user=request.user,
        date=selected_date
    ).select_related('job').order_by('start_time')
    
    # Calculate daily total
    daily_total = sum(entry.total_hours() for entry in entries)
    
    # Handle form submission
    if request.method == 'POST':
        form = TimeEntryForm(user=request.user, data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            try:
                entry.full_clean()
                entry.save()
                messages.success(request, 'Time entry added successfully!')
                return redirect(f'{reverse("timesheet:daily_entry")}?date={selected_date}')
            except ValidationError as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with selected date
        form = TimeEntryForm(user=request.user, initial={'date': selected_date})
    
    # Date filter form
    date_form = DateFilterForm(initial={'date': selected_date})
    
    # Navigation dates
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    context = {
        'selected_date': selected_date,
        'entries': entries,
        'daily_total': daily_total,
        'form': form,
        'date_form': date_form,
        'prev_date': prev_date,
        'next_date': next_date,
        'has_jobs': Job.objects.filter(user=request.user).exists(),
    }
    return render(request, 'timesheet/daily_entry.html', context)


@login_required
def weekly_summary(request):
    """Weekly summary view showing current week with totals."""
    # Get week start date from GET parameter or default to current week
    week_start_str = request.GET.get('week_start')
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
            # Ensure it's a Monday
            week_start = week_start - timedelta(days=week_start.weekday())
        except ValueError:
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
    else:
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
    
    # Calculate week end
    week_end = week_start + timedelta(days=6)
    
    # Get all entries for the week
    week_entries = TimeEntry.objects.filter(
        user=request.user,
        date__range=[week_start, week_end]
    ).select_related('job').order_by('date', 'start_time')
    
    # Organize entries by day
    week_data = []
    weekly_total = Decimal('0.00')
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        day_entries = [entry for entry in week_entries if entry.date == current_date]
        day_total = sum(entry.total_hours() for entry in day_entries)
        weekly_total += day_total
        
        week_data.append({
            'date': current_date,
            'day_name': current_date.strftime('%A'),
            'entries': day_entries,
            'total': day_total,
            'is_today': current_date == timezone.now().date(),
        })
    
    # Navigation weeks
    prev_week = week_start - timedelta(weeks=1)
    next_week = week_start + timedelta(weeks=1)
    
    context = {
        'week_start': week_start,
        'week_end': week_end,
        'week_data': week_data,
        'weekly_total': weekly_total,
        'prev_week': prev_week,
        'next_week': next_week,
    }
    return render(request, 'timesheet/weekly_summary.html', context)


@login_required
def job_list(request):
    """List all jobs for the current user."""
    jobs = Job.objects.filter(user=request.user).order_by('name', 'address')
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'timesheet/job_list.html', context)


@login_required
def job_create(request):
    """Create a new job."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, f'Job "{job.display_name()}" created successfully!')
            return redirect('timesheet:job_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    
    context = {
        'form': form,
        'title': 'Add New Job',
        'submit_text': 'Create Job',
    }
    return render(request, 'timesheet/job_form.html', context)


@login_required
def job_edit(request, pk):
    """Edit an existing job."""
    job = get_object_or_404(Job, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job "{job.display_name()}" updated successfully!')
            return redirect('timesheet:job_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'title': f'Edit Job: {job.display_name()}',
        'submit_text': 'Update Job',
    }
    return render(request, 'timesheet/job_form.html', context)


@login_required
def job_delete(request, pk):
    """Delete a job with confirmation."""
    job = get_object_or_404(Job, pk=pk, user=request.user)
    
    # Check if job has time entries
    entry_count = TimeEntry.objects.filter(job=job).count()
    
    if request.method == 'POST':
        job_name = job.display_name()
        job.delete()
        messages.success(request, f'Job "{job_name}" deleted successfully!')
        return redirect('timesheet:job_list')
    
    context = {
        'job': job,
        'entry_count': entry_count,
    }
    return render(request, 'timesheet/job_delete.html', context)


@login_required
def entry_edit(request, pk):
    """Edit an existing time entry."""
    entry = get_object_or_404(TimeEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TimeEntryForm(user=request.user, data=request.POST, instance=entry)
        if form.is_valid():
            try:
                entry = form.save()
                entry.full_clean()
                entry.save()
                messages.success(request, 'Time entry updated successfully!')
                return redirect(f'{reverse("timesheet:daily_entry")}?date={entry.date}')
            except ValidationError as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimeEntryForm(user=request.user, instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'title': f'Edit Time Entry for {entry.date}',
    }
    return render(request, 'timesheet/entry_form.html', context)


@login_required
def entry_delete(request, pk):
    """Delete a time entry with confirmation."""
    entry = get_object_or_404(TimeEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entry_date = entry.date
        entry.delete()
        messages.success(request, 'Time entry deleted successfully!')
        return redirect(f'{reverse("timesheet:daily_entry")}?date={entry_date}')
    
    context = {
        'entry': entry,
    }
    return render(request, 'timesheet/entry_delete.html', context)


@login_required
def validate_overlap(request):
    """AJAX endpoint to validate time entry overlaps."""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        entry_id = request.POST.get('entry_id')  # For editing existing entries
        
        try:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            # Check for overlaps
            overlapping_entries = TimeEntry.objects.filter(
                user=request.user,
                date=entry_date
            )
            
            if entry_id:
                overlapping_entries = overlapping_entries.exclude(pk=entry_id)
            
            for entry in overlapping_entries:
                if start_time < entry.end_time and end_time > entry.start_time:
                    return JsonResponse({
                        'valid': False,
                        'message': f'Time overlaps with existing entry: {entry.start_time} - {entry.end_time} for {entry.job}'
                    })
            
            return JsonResponse({'valid': True})
            
        except (ValueError, TypeError):
            return JsonResponse({
                'valid': False,
                'message': 'Invalid date or time format'
            })
    
    return JsonResponse({'valid': False, 'message': 'Invalid request'})
