#!/usr/bin/env python3
"""
Template Debug Setup Script for FamilyHub Standalone Apps

This script sets up template debugging for any FamilyHub standalone app.
It copies the debug template tags and creates basic debugging templates.

Usage:
    python setup_template_debug.py <app_path> <app_name> [app_color] [app_icon]

Examples:
    python setup_template_debug.py standalone-apps/daycare_invoice "Daycare Invoice" "#ef4444" "🧾"
    python setup_template_debug.py standalone-apps/credit_card_mgmt "Credit Card" "#10b981" "💳"
    python setup_template_debug.py standalone-apps/upcoming_payments "Upcoming Payments" "#f59e0b" "📅"
    python setup_template_debug.py standalone-apps/employment_history "Employment" "#8b5cf6" "💼"
    python setup_template_debug.py standalone-apps/household_budget "Budget" "#06b6d4" "💰"
"""

import os
import sys
import shutil
from pathlib import Path


def setup_template_debug(app_path, app_name, app_color="#6366f1", app_icon="🔧"):
    """
    Set up template debugging for a standalone app.
    
    Args:
        app_path: Path to the standalone app (e.g., "standalone-apps/daycare_invoice")
        app_name: Display name for the app (e.g., "Daycare Invoice")
        app_color: Primary color for debug banners (e.g., "#ef4444")
        app_icon: Icon for debug banners (e.g., "🧾")
    """
    workspace_root = Path(__file__).parent
    app_full_path = workspace_root / app_path
    
    # Find the Django app directory
    app_dirs = [d for d in app_full_path.iterdir() if d.is_dir() and d.name.endswith('_app')]
    if not app_dirs:
        print(f"❌ No Django app directory found in {app_path}")
        return False
    
    django_app_path = app_dirs[0]
    app_slug = django_app_path.name.replace('_app', '')
    
    print(f"🔧 Setting up template debugging for {app_name}")
    print(f"📁 App path: {django_app_path}")
    print(f"🎨 Color: {app_color}")
    print(f"🎯 Icon: {app_icon}")
    
    # Create templatetags directory
    templatetags_dir = django_app_path / "templatetags"
    templatetags_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_file = templatetags_dir / "__init__.py"
    init_file.write_text(f"# Template tags for {app_name} debug functionality")
    
    # Copy and customize debug_tags.py
    universal_debug_path = workspace_root / "shared" / "templatetags" / "debug_tags_universal.py"
    debug_tags_path = templatetags_dir / "debug_tags.py"
    
    if not universal_debug_path.exists():
        print(f"❌ Universal debug tags not found at {universal_debug_path}")
        return False
    
    # Read and customize the debug tags
    debug_content = universal_debug_path.read_text()
    debug_content = debug_content.replace('APP_NAME = "Generic App"', f'APP_NAME = "{app_name}"')
    debug_content = debug_content.replace('APP_COLOR = "#6366f1"', f'APP_COLOR = "{app_color}"')
    debug_content = debug_content.replace('APP_COLOR_SECONDARY = "#4f46e5"', f'APP_COLOR_SECONDARY = "{app_color}dd"')
    debug_content = debug_content.replace('APP_ICON = "🔧"', f'APP_ICON = "{app_icon}"')
    
    debug_tags_path.write_text(debug_content)
    
    # Create templates directory if it doesn't exist
    templates_dir = django_app_path / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    app_templates_dir = templates_dir / app_slug
    app_templates_dir.mkdir(exist_ok=True)
    
    # Create a basic base template if it doesn't exist
    base_template_path = app_templates_dir / "base.html"
    if not base_template_path.exists():
        base_template_content = f'''{{{% load debug_tags %}}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{% block title %}}}{app_name}{{{% endblock %}}}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* Custom styles for {app_name.lower()} app */
        :root {{
            --primary: {app_color};
            --primary-light: {app_color}20;
        }}
        
        .navbar-brand {{
            font-weight: bold;
        }}
        
        .card {{
            border: none;
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        }}
        
        .btn-primary {{
            background-color: var(--primary);
            border-color: var(--primary);
        }}
        
        .btn-primary:hover {{
            background-color: var(--primary);
            border-color: var(--primary);
            opacity: 0.9;
        }}
        
        {{{% block extra_css %}}{{{% endblock %}}}
    </style>
</head>
<body>
    {{{% template_debug_banner %}}}
    
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-{app_icon} me-2"></i>{app_name}
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Dashboard</a>
                    </li>
                    {{{% if user.is_authenticated %}}}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            {{{{ user.username }}}}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{{{% url 'admin:logout' %}}}">Logout</a></li>
                        </ul>
                    </li>
                    {{{% else %}}}
                    <li class="nav-item">
                        <a class="nav-link" href="{{{% url 'admin:login' %}}}">Login</a>
                    </li>
                    {{{% endif %}}}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <main class="container my-4">
        {{{% block content %}}}
        <div class="row">
            <div class="col-12">
                <div class="jumbotron bg-light p-5 rounded">
                    <h1 class="display-4">{app_icon} {app_name}</h1>
                    <p class="lead">Welcome to the {app_name} standalone application.</p>
                    <hr class="my-4">
                    <p>This app is running independently with its own database and settings.</p>
                    <a class="btn btn-primary btn-lg" href="#" role="button">Get Started</a>
                </div>
            </div>
        </div>
        {{{% endblock %}}}
    </main>
    
    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {{{% block extra_js %}}{{{% endblock %}}}
</body>
</html>'''
        base_template_path.write_text(base_template_content)
    
    # Create debug showcase template
    debug_template_path = app_templates_dir / "debug_showcase.html"
    debug_template_content = f'''{{{% extends "{app_slug}/base.html" %}}}
{{{% load debug_tags %}}}

{{{% block title %}}}{{{{ title }}}}{{{% endblock %}}}

{{{% block content %}}}
{{{% template_info "{app_slug}/debug_showcase.html" True %}}}

<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header" style="background: {app_color}; color: white;">
                    <h3><i class="fas fa-bug me-2"></i>{app_name} Debug Showcase</h3>
                    <p class="mb-0">Template debugging features for standalone {app_name} app</p>
                </div>
                <div class="card-body">
                    
                    <!-- App Info -->
                    <div class="mb-4">
                        <h5><i class="{app_icon} me-2" style="color: {app_color};"></i>App Information</h5>
                        {{{% app_debug_info %}}}
                    </div>

                    <!-- Template Debug Banner Demo -->
                    <div class="mb-4">
                        <h5><i class="fas fa-banner me-2" style="color: {app_color};"></i>Debug Banner</h5>
                        <p class="text-muted">The debug banner appears at the top of every page (visible above).</p>
                        <div class="alert alert-info">
                            <strong>Features:</strong> Shows template path, app context, request method, and more.
                        </div>
                    </div>

                    <!-- Template Path Demo -->
                    <div class="mb-4">
                        <h5><i class="fas fa-map-marker-alt me-2" style="color: {app_color};"></i>Template Path</h5>
                        <p>Current template path: {{{% show_template_path %}}}</p>
                    </div>

                    <!-- Context Variables Demo -->
                    <div class="mb-4">
                        <h5><i class="fas fa-database me-2" style="color: {app_color};"></i>Context Variables</h5>
                        {{{% debug_context_vars "title" "user" %}}}
                    </div>

                    <!-- Template Hierarchy Demo -->
                    <div class="mb-4">
                        <h5><i class="fas fa-sitemap me-2" style="color: {app_color};"></i>Template Hierarchy</h5>
                        {{{% template_hierarchy %}}}
                    </div>

                    <!-- Development Info -->
                    <div class="mt-5">
                        <h5><i class="fas fa-info-circle me-2" style="color: {app_color};"></i>Development Information</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="alert alert-warning">
                                    <h6><i class="fas fa-exclamation-triangle me-2"></i>Debug Mode Only</h6>
                                    <p class="mb-0">Template debugging features are only visible when <code>DEBUG=True</code>.</p>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="alert alert-info">
                                    <h6><i class="fas fa-server me-2"></i>Standalone App</h6>
                                    <p class="mb-1"><strong>Independent:</strong> Own database and settings</p>
                                    <p class="mb-0"><strong>Customizable:</strong> Can run on any port</p>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>
{{{% endblock %}}}'''
    debug_template_path.write_text(debug_template_content)
    
    print(f"✅ Template debugging setup complete for {app_name}!")
    print(f"📝 Created files:")
    print(f"   - {templatetags_dir}/debug_tags.py")
    print(f"   - {base_template_path}")
    print(f"   - {debug_template_path}")
    print(f"")
    print(f"🚀 To test the debugging:")
    print(f"   1. Add template debugging to your views")
    print(f"   2. Add debug URLs to your app")
    print(f"   3. Run: python manage.py runserver")
    print(f"   4. Visit the debug showcase page")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python setup_template_debug.py <app_path> <app_name> [app_color] [app_icon]")
        print("Example: python setup_template_debug.py standalone-apps/daycare_invoice 'Daycare Invoice' '#ef4444' '🧾'")
        sys.exit(1)
    
    app_path = sys.argv[1]
    app_name = sys.argv[2]
    app_color = sys.argv[3] if len(sys.argv) > 3 else "#6366f1"
    app_icon = sys.argv[4] if len(sys.argv) > 4 else "🔧"
    
    success = setup_template_debug(app_path, app_name, app_color, app_icon)
    sys.exit(0 if success else 1)
