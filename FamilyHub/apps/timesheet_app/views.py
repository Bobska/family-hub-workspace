from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q, Count, F, DurationField
from django.db.models.functions import Cast
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime, timedelta, date
from decimal import Decimal
import pytz
from .models import Job, TimeEntry
from .forms import JobForm, TimeEntryForm, QuickTimeEntryForm, DateFilterForm


@login_required
def dashboard(request):
    """Dashboard view showing today's overview with quick entry form."""
    # Set timezone to Auckland
    auckland_tz = pytz.timezone('Pacific/Auckland')
    now = timezone.now().astimezone(auckland_tz)
    today = now.date()
    
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
                # Handle different types of validation errors
                if hasattr(e, 'error_dict'):
                    # Field-specific errors
                    error_messages = []
                    for field, errors in e.error_dict.items():
                        for error in errors:
                            error_messages.append(str(error))
                    messages.error(request, '; '.join(error_messages))
                elif hasattr(e, 'messages'):
                    # List of error messages
                    messages.error(request, '; '.join(e.messages))
                else:
                    # Single error message
                    messages.error(request, str(e))
            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickTimeEntryForm(user=request.user)
    
    context = {
        'today': today,
        'current_datetime': now,
        'formatted_date': now.strftime('%d %B, %Y').lstrip('0'),  # "29 August, 2025" (Windows compatible)
        'formatted_time': now.strftime('%I:%M %p'),  # 12-hour format with AM/PM
        'day_name': now.strftime('%A'),
        'today_entries': today_entries,
        'today_total': today_total,
        'form': form,
        'has_jobs': Job.objects.filter(user=request.user).exists(),
    }
    
    # When rendered inside FamilyHub, indicate integrated mode so shared templates
    # will extend the FamilyHub base template. FamilyHub always sets integrated_mode=True.
    context['integrated_mode'] = True
    # Use the integrated timesheet base which itself extends FamilyHub `base.html`
    # and includes the timesheet navigation under the global FamilyHub navigation.
    context['base_template'] = 'timesheet/base_integrated.html'

    # For standalone app, always use the dashboard template
    template_name = 'timesheet/dashboard.html'
    
    return render(request, template_name, context)


@login_required
def daily_entry(request):
    """Daily entry view with date picker to select any date."""
    # Get current date for comparison
    auckland_tz = pytz.timezone('Pacific/Auckland')
    today = timezone.now().astimezone(auckland_tz).date()
    
    # Get date from GET parameter or default to today
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            # Prevent future dates
            if selected_date > today:
                messages.warning(request, "Cannot view future dates")
                return redirect(f'{reverse("timesheet:daily_entry")}?date={today}')
        except ValueError:
            selected_date = today
    else:
        selected_date = today
    
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
                error_msg = ', '.join(e.messages) if hasattr(e, 'messages') else str(e)
                messages.error(request, f'Validation error: {error_msg}')
            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the form errors below.')
    else:
        # Pre-fill form with selected date
        form = TimeEntryForm(user=request.user, initial={'date': selected_date})
    
    # Date filter form
    date_form = DateFilterForm(initial={'date': selected_date})
    
    # Navigation dates
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    # Don't allow next date navigation to future
    if next_date > today:
        next_date = None
    
    # Format selected date like dashboard
    formatted_date = selected_date.strftime('%d %B, %Y').lstrip('0')
    day_name = selected_date.strftime('%A')
    
    context = {
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'day_name': day_name,
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
    # Get current date and week info
    auckland_tz = pytz.timezone('Pacific/Auckland')
    current_date = timezone.now().astimezone(auckland_tz).date()
    current_year, current_week_num, _ = current_date.isocalendar()
    
    # Get week start date from GET parameter or default to current week
    year = int(request.GET.get('year', current_year))
    week = int(request.GET.get('week', current_week_num))
    
    # Prevent future weeks
    if year > current_year or (year == current_year and week > current_week_num):
        messages.warning(request, "Cannot view future weeks")
        return redirect(f"{reverse('timesheet:weekly_summary')}?year={current_year}&week={current_week_num}")
    
    # Calculate week start from year and week number
    jan_1 = date(year, 1, 1)
    week_start = jan_1 + timedelta(weeks=week-1) - timedelta(days=jan_1.weekday())
    
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
        current_date_iter = week_start + timedelta(days=i)
        day_entries = [entry for entry in week_entries if entry.date == current_date_iter]
        day_total = sum(entry.total_hours() for entry in day_entries)
        weekly_total += day_total
        
        week_data.append({
            'date': current_date_iter,
            'day_name': current_date_iter.strftime('%A'),
            'weekday': current_date_iter.weekday(),  # 0=Monday, 6=Sunday
            'entries': day_entries,
            'total': day_total,
            'is_today': current_date_iter == current_date,
        })
    
    # Calculate statistics
    days_worked = set(entry.date for entry in week_entries)
    total_entries_count = len(week_entries)
    
    # Navigation weeks
    prev_week_start = week_start - timedelta(weeks=1)
    prev_year, prev_week_num, _ = prev_week_start.isocalendar()
    
    next_week_start = week_start + timedelta(weeks=1)
    next_year, next_week_num, _ = next_week_start.isocalendar()
    
    # Don't show next week if it's in the future
    show_next = not (next_year > current_year or (next_year == current_year and next_week_num > current_week_num))
    
    # Calculate daily average
    daily_average = round(float(weekly_total) / 7, 1) if weekly_total > 0 else 0
    
    context = {
        'week_start': week_start,
        'week_end': week_end,
        'week_data': week_data,
        'weekly_total': weekly_total,
        'daily_average': daily_average,
        'days_worked': len(days_worked),
        'total_entries': total_entries_count,
        'current_week': week,
        'current_year': year,
        'prev_year': prev_year,
        'prev_week': prev_week_num,
        'next_year': next_year,
        'next_week': next_week_num,
        'show_next': show_next,
    }
    return render(request, 'timesheet/weekly_summary.html', context)


@login_required
def job_list(request):
    """List all jobs for the current user with optimized queries."""
    # Optimized query with annotations
    jobs = Job.objects.filter(user=request.user).annotate(
        entry_count=Count('time_entries')
    ).order_by('name', 'address')
    
    # Calculate statistics using annotations
    total_jobs = jobs.count()
    total_entries = sum(job.entry_count for job in jobs)
    total_hours = sum(job.total_hours() for job in jobs)  # Keep using model method for accuracy
    avg_entries_per_job = round(total_entries / total_jobs, 1) if total_jobs > 0 else 0
    
    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_entries': total_entries,
        'total_hours': total_hours,
        'avg_entries_per_job': avg_entries_per_job,
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
def entry_add(request):
    """Add a new time entry."""
    initial_data = {}
    if 'job' in request.GET:
        initial_data['job'] = request.GET['job']
    if 'date' in request.GET:
        try:
            initial_data['date'] = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if request.method == 'POST':
        form = TimeEntryForm(user=request.user, data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            try:
                entry.full_clean()
                entry.save()
                messages.success(request, 'Time entry added successfully!')
                return redirect(f'{reverse("timesheet:daily_entry")}?date={entry.date}')
            except ValidationError as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimeEntryForm(user=request.user, initial=initial_data)
    
    context = {
        'form': form,
        'title': 'Add Time Entry',
    }
    return render(request, 'timesheet/entry_form.html', context)


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
