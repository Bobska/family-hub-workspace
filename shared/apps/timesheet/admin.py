from django.contrib import admin
from .models import Job, TimeEntry


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'address']
    ordering = ['name']
    
    def get_queryset(self, request):
        """Only show user's own jobs unless superuser"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically set user on creation"""
        if not change:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'date', 'start_time', 'end_time', 'break_duration', 'total_hours_display']
    list_filter = ['user', 'job', 'date', 'break_duration']
    search_fields = ['job__name', 'user__username']
    date_hierarchy = 'date'
    ordering = ['-date', '-start_time']
    
    def get_queryset(self, request):
        """Only show user's own entries unless superuser"""
        qs = super().get_queryset(request).select_related('user', 'job')
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically set user on creation"""
        if not change:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def total_hours_display(self, obj):
        """Display total hours in admin"""
        return f"{obj.total_hours():.2f}h"
    total_hours_display.short_description = 'Total Hours'
    total_hours_display.admin_order_field = 'start_time'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter job choices to user's jobs"""
        if db_field.name == "job" and request and hasattr(request, 'user') and request.user.is_authenticated:
            kwargs["queryset"] = Job.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
