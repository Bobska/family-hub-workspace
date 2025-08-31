from django.urls import path
from . import views
from . import debug_views

app_name = 'timesheet'

urlpatterns = [
    # Dashboard and main views
    path('', views.dashboard, name='dashboard'),
    path('daily/', views.daily_entry, name='daily_entry'),
    path('weekly/', views.weekly_summary, name='weekly_summary'),
    
    # Debug views (only available in DEBUG mode)
    path('debug/templates/', debug_views.template_debug_showcase, name='template_debug'),
    
    # Job management
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/add/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    
    # Time entry management
    path('entries/add/', views.entry_add, name='entry_add'),
    path('entries/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entries/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    
    # AJAX endpoints
    path('api/validate-overlap/', views.validate_overlap, name='validate_overlap'),
]
