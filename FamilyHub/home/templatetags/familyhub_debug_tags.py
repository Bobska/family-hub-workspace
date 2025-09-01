"""
FamilyHub Home App Template Tags

Simple debug tags for FamilyHub main dashboard templates.
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def familyhub_debug_banner(context):
    """
    Display a debug banner for FamilyHub main platform.
    Only shows in DEBUG mode with FamilyHub purple branding.
    """
    if not settings.DEBUG:
        return ''

    # Get the current template name
    template_obj = context.template
    template_name = "Unknown Template"
    if hasattr(template_obj, 'name'):
        template_name = template_obj.name
    elif hasattr(template_obj, 'origin') and template_obj.origin:
        template_name = template_obj.origin.name

    # Create FamilyHub debug banner
    banner_html = f"""
    <div class="familyhub-debug-banner" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 3px; margin-right: 10px;">
                    🏠 FAMILYHUB PLATFORM
                </span>
                <strong>{template_name}</strong>
            </div>
            <div style="font-size: 11px; opacity: 0.9;">
                <span style="margin-right: 15px;">🎯 Main Dashboard</span>
                <span style="margin-right: 15px;">🔧 DEBUG MODE</span>
                <span>🌐 Port 8000</span>
            </div>
        </div>
    </div>
    """

    return mark_safe(banner_html)


@register.simple_tag
def familyhub_debug_context():
    """
    Return debug context information for FamilyHub platform
    """
    if not settings.DEBUG:
        return ""
    
    return "DEBUG: FamilyHub Platform - Main Dashboard - Port 8000"


@register.filter
def familyhub_debug_highlight(value):
    """
    Add debug highlighting with FamilyHub purple theme
    """
    if not settings.DEBUG:
        return value
    
    return mark_safe(f'<span style="background-color: rgba(102, 126, 234, 0.2); padding: 2px 4px; border-radius: 3px;">{value}</span>')
