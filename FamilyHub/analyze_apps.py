#!/usr/bin/env python3
"""
Analyze FamilyHub/apps directories to identify empty or stub directories
"""
import os
from pathlib import Path

apps_dir = Path(__file__).parent / "apps"
print("=== FAMILYHUB APPS DIRECTORY ANALYSIS ===\n")

for app_path in sorted(apps_dir.iterdir()):
    if app_path.is_dir() and app_path.name != "__pycache__":
        print(f"📁 {app_path.name}/")
        
        # Count files
        py_files = list(app_path.glob("*.py"))
        all_files = list(app_path.rglob("*"))
        non_cache_files = [f for f in all_files if "__pycache__" not in str(f) and f.is_file()]
        
        print(f"   Python files: {len(py_files)}")
        print(f"   Total files (non-cache): {len(non_cache_files)}")
        
        # Check if it has models.py with content
        models_file = app_path / "models.py"
        if models_file.exists():
            content = models_file.read_text()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            actual_content_lines = len([line for line in lines if 'import' not in line and 'from' not in line])
            print(f"   models.py content lines: {actual_content_lines}")
            if actual_content_lines <= 2:  # Just class definitions with pass
                print("   ⚠️  STUB: models.py has minimal content")
        else:
            print("   ❌ No models.py")
        
        # Check if it has views.py with content
        views_file = app_path / "views.py"
        if views_file.exists():
            content = views_file.read_text()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            actual_content_lines = len([line for line in lines if 'import' not in line and 'from' not in line])
            print(f"   views.py content lines: {actual_content_lines}")
            if actual_content_lines <= 2:
                print("   ⚠️  STUB: views.py has minimal content")
        else:
            print("   ❌ No views.py")
            
        # Recommend action
        if len(non_cache_files) <= 8 and models_file.exists():  # Typical Django starter files
            content = models_file.read_text()
            if "pass" in content and len(content) < 500:
                print("   🗑️  RECOMMENDATION: Remove empty stub directory")
        
        print()

# Check standalone apps
print("\n=== STANDALONE APPS AVAILABLE ===")
standalone_dir = Path(__file__).parent.parent / "standalone-apps"
for standalone_app in sorted(standalone_dir.iterdir()):
    if standalone_app.is_dir():
        app_dir = standalone_app / f"{standalone_app.name}_app"
        if app_dir.exists():
            models_file = app_dir / "models.py"
            if models_file.exists():
                content = models_file.read_text()
                if len(content) > 500:  # Has actual content
                    print(f"   ✅ {standalone_app.name} - Ready for integration")
                else:
                    print(f"   ⚠️  {standalone_app.name} - Stub implementation")
            else:
                print(f"   ❌ {standalone_app.name} - No models.py")
        else:
            print(f"   ❌ {standalone_app.name} - No app directory")
