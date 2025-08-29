"""
Context processors for timesheet app
Provides deployment-specific context variables using app settings
"""
from .app_settings import get_timesheet_settings, get_app_context


def deployment_context(request):
    """
    Add deployment context to templates using app settings
    Provides comprehensive context for both standalone and integrated deployments
    """
    settings = get_timesheet_settings()
    
    # Get base context from app settings
    context = get_app_context(request=request)
    
    # Add legacy context variables for backward compatibility
    context.update({
        'is_standalone': settings.is_standalone,
        'is_integrated': settings.is_integrated,
        'base_template': settings.base_template,
        'deployment_context': settings.deployment_context
    })
    
    return context
