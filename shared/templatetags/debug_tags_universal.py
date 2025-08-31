"""
Universal Template Debug Tags for FamilyHub Apps

Custom Django template tags for debugging template rendering and displaying
template hierarchy information in development mode. This is a generic version
that can be copied to any FamilyHub standalone app.

Usage in templates:
    {% load debug_tags %}
    {% template_debug_banner %}
    {% show_template_path %}
    {% template_info "custom_template_name.html" %}

To use in your app:
1. Copy this file to your_app/templatetags/debug_tags.py
2. Update the app_name variable below
3. Customize colors and app context as needed
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import os
from pathlib import Path

register = template.Library()

# Configuration - customize for each app
APP_NAME = "Generic App"  # Change this for each app
APP_COLOR = "#6366f1"  # Change this for each app (primary color)
APP_COLOR_SECONDARY = "#4f46e5"  # Change this for each app (secondary color)
APP_ICON = "🔧"  # Change this for each app


@register.simple_tag(takes_context=True)
def template_debug_banner(context, template_name=None):
    """
    Display a debug banner showing template information.
    Only shows in DEBUG mode.
    
    Usage: {% template_debug_banner %}
    Usage: {% template_debug_banner "custom_template.html" %}
    """
    if not settings.DEBUG:
        return ''
    
    # Get the current template name
    if template_name is None:
        template_obj = context.template
        if hasattr(template_obj, 'name'):
            template_name = template_obj.name
        elif hasattr(template_obj, 'origin') and template_obj.origin:
            template_name = template_obj.origin.name
        else:
            template_name = "Unknown Template"
    
    # Try to get relative path from project root
    try:
        if template_name and os.path.isabs(template_name):
            # Convert absolute path to relative from workspace root
            workspace_root = Path(__file__).resolve().parent.parent.parent.parent
            template_path = Path(template_name)
            try:
                rel_path = template_path.relative_to(workspace_root)
                template_display = str(rel_path)
            except ValueError:
                template_display = template_name
        else:
            template_display = template_name or "Unknown"
    except Exception:
        template_display = template_name or "Unknown"
    
    # Get the template directory info
    template_dir = "Unknown"
    app_context = "Unknown"
    
    if template_name and isinstance(template_name, str):
        if 'standalone-apps/' in template_name:
            template_dir = f"Standalone {APP_NAME}"
            app_context = "Independent Mode"
        elif f'{APP_NAME.lower()}_app/templates/' in template_name:
            template_dir = f"{APP_NAME} App"
            app_context = "Standalone App"
        elif 'registration/' in template_name:
            template_dir = "Authentication"
            app_context = "Django Auth"
        elif 'FamilyHub/' in template_name:
            template_dir = f"Integrated {APP_NAME}"
            app_context = "FamilyHub Integration"
        else:
            template_dir = f"{APP_NAME} Templates"
            app_context = "App Mode"
    
    # Create the debug banner HTML
    banner_html = f"""
    <div class="template-debug-banner" style="
        background: linear-gradient(135deg, {APP_COLOR} 0%, {APP_COLOR_SECONDARY} 100%);
        color: white;
        padding: 8px 15px;
        margin: 0;
        border-left: 4px solid #10b981;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        line-height: 1.3;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1050;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 3px; margin-right: 10px;">
                    {APP_ICON} {APP_NAME.upper()} DEBUG
                </span>
                <strong>{template_display}</strong>
            </div>
            <div style="font-size: 11px; opacity: 0.9;">
                <span style="margin-right: 15px;">📁 {template_dir}</span>
                <span style="margin-right: 15px;">🎯 {app_context}</span>
                <span>🕒 {context.request.method if 'request' in context else 'N/A'}</span>
            </div>
        </div>
    </div>
    """
    
    return mark_safe(banner_html)


@register.simple_tag(takes_context=True)
def show_template_path(context):
    """
    Display just the template path for debugging.
    
    Usage: {% show_template_path %}
    """
    if not settings.DEBUG:
        return ''
    
    template_obj = context.template
    template_name = "Unknown"
    
    if hasattr(template_obj, 'name'):
        template_name = template_obj.name
    elif hasattr(template_obj, 'origin') and template_obj.origin:
        template_name = template_obj.origin.name
    
    return mark_safe(f'<small class="text-muted">Template: {template_name}</small>')


@register.simple_tag
def template_info(template_name, show_full_path=False):
    """
    Display information about a specific template.
    
    Usage: {% template_info "base.html" %}
    Usage: {% template_info "app/dashboard.html" True %}
    """
    if not settings.DEBUG:
        return ''
    
    # Basic template info
    info_html = f"""
    <div class="template-info alert alert-info p-2 mb-2" style="font-size: 11px; border-left: 4px solid {APP_COLOR};">
        <strong>{APP_NAME} Template:</strong> {template_name}
        {f'<br><strong>Full Path:</strong> {template_name}' if show_full_path else ''}
    </div>
    """
    
    return mark_safe(info_html)


@register.simple_tag(takes_context=True)
def debug_context_vars(context, *var_names):
    """
    Display context variables for debugging.
    
    Usage: {% debug_context_vars "user" "entries" "request" %}
    """
    if not settings.DEBUG:
        return ''
    
    debug_info = []
    for var_name in var_names:
        if var_name in context:
            value = context[var_name]
            value_type = type(value).__name__
            if hasattr(value, '__len__') and not isinstance(value, str):
                value_repr = f"{value_type}({len(value)} items)"
            else:
                value_repr = f"{value_type}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}"
            debug_info.append(f"<strong>{var_name}:</strong> {value_repr}")
        else:
            debug_info.append(f"<strong>{var_name}:</strong> <em>Not found</em>")
    
    if not debug_info:
        return ''
    
    html = f"""
    <div class="debug-context-vars alert alert-secondary p-2 mb-2" style="font-size: 11px; border-left: 4px solid {APP_COLOR};">
        <strong>{APP_NAME} Context Variables:</strong><br>
        {'<br>'.join(debug_info)}
    </div>
    """
    
    return mark_safe(html)


@register.filter
def debug_type(value):
    """
    Return the type of a value for debugging.
    
    Usage: {{ some_variable|debug_type }}
    """
    return type(value).__name__


@register.filter
def debug_length(value):
    """
    Return the length of a value if it has one.
    
    Usage: {{ some_list|debug_length }}
    """
    try:
        return len(value)
    except (TypeError, AttributeError):
        return "No length"


@register.simple_tag
def template_hierarchy():
    """
    Show the current template hierarchy for debugging.
    
    Usage: {% template_hierarchy %}
    """
    if not settings.DEBUG:
        return ''
    
    html = f"""
    <div class="template-hierarchy alert alert-warning p-2 mb-2" style="font-size: 11px; border-left: 4px solid {APP_COLOR};">
        <strong>{APP_NAME} Template Hierarchy:</strong><br>
        Current Template → Base Template → Django Root
    </div>
    """
    
    return mark_safe(html)


@register.simple_tag
def app_debug_info():
    """
    Display app-specific debug information.
    
    Usage: {% app_debug_info %}
    """
    if not settings.DEBUG:
        return ''
    
    html = f"""
    <div class="app-debug-info alert alert-light p-2 mb-2" style="font-size: 11px; border-left: 4px solid {APP_COLOR};">
        <strong>{APP_ICON} {APP_NAME} Debug Info:</strong><br>
        <strong>App Name:</strong> {APP_NAME}<br>
        <strong>Primary Color:</strong> {APP_COLOR}<br>
        <strong>Mode:</strong> Standalone Django App
    </div>
    """
    
    return mark_safe(html)
