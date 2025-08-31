"""
Home App URL Configuration

URLs for the home application including dashboard and debug views.
"""
from django.urls import path
from . import views
from . import debug_views

app_name = 'home'

urlpatterns = [
    # Main dashboard (root URL)
    path('', views.home_dashboard, name='dashboard'),
    
    # Debug and monitoring endpoints  
    path('debug/', views.debug_dashboard, name='debug_dashboard'),
    path('debug/templates/', debug_views.template_debug_showcase, name='template_debug'),
    path('health/', views.health_check, name='health_check'),
]
