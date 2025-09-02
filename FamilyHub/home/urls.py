"""
Home App URL Configuration

URLs for the home application including dashboard.
"""
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # Main dashboard (root URL)
    path('', views.home_dashboard, name='dashboard'),
    
    # Debug and monitoring endpoints  
    path('debug/', views.debug_dashboard, name='debug_dashboard'),
    path('health/', views.health_check, name='health_check'),
]
