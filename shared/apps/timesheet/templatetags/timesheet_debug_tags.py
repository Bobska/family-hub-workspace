"""
Timesheet App Template Debug Tags - FamilyHub Integrated Mode

Custom Django template tags for debugging template rendering and displaying
template hierarchy information in development mode for FamilyHub integrated timesheet app.

Usage in templates:
    {% load debug_tags %}
    {% template_debug_banner %}
    {% show_template_path %}
    {% template_info "custom_template_name.html" %}
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import os
from pathlib import Path

register = template.Library()


@register.simple_tag(takes_context=True)
def template_debug_banner(context, template_name=None):
    """
    Display a debug banner showing template information for FamilyHub integrated mode.
    Only shows in DEBUG mode. Shows purple banner for integrated mode.

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
            workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
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
    template_dir = "FamilyHub Integrated"
    app_context = "Integrated Mode"

    if template_name and isinstance(template_name, str):
        if 'FamilyHub/apps/timesheet_app/' in template_name:
            template_dir = "FamilyHub Timesheet"
            app_context = "Integrated Mode (Port 8000)"
        elif 'registration/' in template_name:
            template_dir = "Authentication"
            app_context = "Django Auth"
        else:
            template_dir = "FamilyHub Templates"
            app_context = "Integrated Mode"

    # Create the debug banner HTML with purple gradient for FamilyHub integrated
    banner_html = f"""
    <div class="template-debug-banner" style="
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
                    🏠 FAMILYHUB INTEGRATED
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
    Usage: {% template_info "timesheet/dashboard.html" True %}
    """
    if not settings.DEBUG:
        return ''

    # Basic template info for FamilyHub integrated mode
    info_html = f"""
    <div class="template-info alert alert-info p-2 mb-2" style="font-size: 11px; background-color: rgba(118, 75, 162, 0.1); border-color: #764ba2;">
        <strong>FamilyHub Integrated Template:</strong> {template_name}
        <br><strong>Location:</strong> FamilyHub/apps/timesheet_app/templates/
        <br><strong>Mode:</strong> Integrated (Port 8000)
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
    <div class="debug-context-vars alert alert-info p-2 mb-2" style="font-size: 11px; background-color: rgba(118, 75, 162, 0.1); border-color: #764ba2;">
        <strong>Context Variables (FamilyHub Integrated):</strong><br>
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

    # Template hierarchy for FamilyHub integrated mode
    html = """
    <div class="template-hierarchy alert alert-info p-2 mb-2" style="font-size: 11px; background-color: rgba(118, 75, 162, 0.1); border-color: #764ba2;">
        <strong>FamilyHub Integrated Template Hierarchy:</strong><br>
        Current Template → Timesheet Base → FamilyHub Root
    </div>
    """

    return mark_safe(html)


# Additional tags for FamilyHub integration
@register.simple_tag
def debug_context():
    """
    Return debug context information for FamilyHub integrated mode
    """
    if not settings.DEBUG:
        return ""
    
    return "DEBUG: Timesheet (FamilyHub Integrated) - FAMILYHUB_INTEGRATED Mode - Port 8000"


@register.filter
def debug_highlight(value):
    """
    Add debug highlighting to template values with purple theme
    """
    if not settings.DEBUG:
        return value
    
    return mark_safe(f'<span style="background-color: rgba(118, 75, 162, 0.2); padding: 2px 4px; border-radius: 3px;">{value}</span>')
