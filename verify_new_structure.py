#!/usr/bin/env python3
"""
New Simple Template Structure Verification
Verifies the simplified template architecture is working correctly
"""

import os
import sys
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_result(message, success=True):
    color = Colors.GREEN if success else Colors.RED
    status = "✅" if success else "❌"
    print(f"{color}{status} {message}{Colors.ENDC}")

def print_header(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {message} ==={Colors.ENDC}")

def verify_new_structure():
    """Verify the new simplified template structure"""
    print_header("NEW SIMPLIFIED TEMPLATE STRUCTURE VERIFICATION")
    
    base_dir = Path(__file__).parent
    errors = []
    
    # 1. Check that shared standalone templates exist
    shared_nav = base_dir / "shared" / "templates" / "navigation" / "timesheet_standalone_nav.html"
    shared_dashboard = base_dir / "shared" / "templates" / "timesheet" / "standalone_dashboard.html"
    
    if shared_nav.exists():
        print_result("Shared standalone navigation exists")
    else:
        errors.append("Missing shared standalone navigation")
        print_result("Missing shared standalone navigation", False)
    
    if shared_dashboard.exists():
        print_result("Shared standalone dashboard exists")
    else:
        errors.append("Missing shared standalone dashboard")
        print_result("Missing shared standalone dashboard", False)
    
    # 2. Check that standalone app only has base template
    standalone_templates = base_dir / "standalone-apps" / "timesheet" / "timesheet_app" / "templates" / "timesheet"
    if standalone_templates.exists():
        template_files = list(standalone_templates.glob("*.html"))
        expected_files = ["base.html", "dashboard.html"]
        
        actual_files = [f.name for f in template_files]
        
        if set(actual_files) <= set(expected_files):
            print_result(f"Standalone templates clean: {actual_files}")
        else:
            extra_files = set(actual_files) - set(expected_files)
            errors.append(f"Extra standalone templates: {extra_files}")
            print_result(f"Extra standalone templates: {extra_files}", False)
        
        # Check dashboard template includes shared template
        dashboard_file = standalone_templates / "dashboard.html"
        if dashboard_file.exists():
            with open(dashboard_file, 'r') as f:
                content = f.read()
            
            if 'timesheet/standalone_dashboard.html' in content:
                print_result("Standalone dashboard includes shared template")
            else:
                errors.append("Standalone dashboard doesn't include shared template")
                print_result("Standalone dashboard doesn't include shared template", False)
    
    # 3. Check integrated template structure
    integrated_template = base_dir / "FamilyHub" / "templates" / "timesheet" / "dashboard_integrated.html"
    if integrated_template.exists():
        with open(integrated_template, 'r') as f:
            content = f.read()
        
        if 'timesheet/standalone_dashboard.html' in content:
            print_result("Integrated template includes shared dashboard")
        else:
            errors.append("Integrated template doesn't include shared dashboard")
            print_result("Integrated template doesn't include shared dashboard", False)
        
        if 'integrated_mode=True' in content:
            print_result("Integrated template passes correct context")
        else:
            errors.append("Integrated template missing integrated_mode=True")
            print_result("Integrated template missing integrated_mode=True", False)
    
    # 4. Check that old templates are removed
    old_templates = [
        base_dir / "shared" / "templates" / "timesheet" / "dashboard_content.html",
        base_dir / "shared" / "templates" / "navigation" / "timesheet_app_nav.html",
        base_dir / "FamilyHub" / "apps" / "timesheet_app" / "templates"
    ]
    
    for old_template in old_templates:
        if not old_template.exists():
            print_result(f"Old template removed: {old_template.name}")
        else:
            errors.append(f"Old template still exists: {old_template}")
            print_result(f"Old template still exists: {old_template.name}", False)
    
    # 5. Verify template hierarchy
    print_header("TEMPLATE HIERARCHY VERIFICATION")
    
    print("Standalone Structure:")
    print("  base.html")
    print("    └── timesheet/standalone_dashboard.html")
    print("        └── navigation/timesheet_standalone_nav.html")
    
    print("\nIntegrated Structure:")
    print("  base.html")
    print("    └── integrated_app_base.html")
    print("        └── FamilyHub global nav")
    print("        └── timesheet/standalone_dashboard.html")
    print("            └── navigation/timesheet_standalone_nav.html")
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    if not errors:
        print_result("🎉 NEW SIMPLIFIED STRUCTURE IS WORKING!", True)
        print("\n✅ Structure Benefits:")
        print("   • Cleaner template organization")
        print("   • Shared navigation and dashboard")
        print("   • Minimal templates in standalone apps")
        print("   • Same dashboard experience in both modes")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORS FOUND ({len(errors)}):{Colors.ENDC}")
        for error in errors:
            print(f"  ❌ {error}")
        return False

def show_file_structure():
    """Show the current file structure"""
    print_header("CURRENT FILE STRUCTURE")
    
    base_dir = Path(__file__).parent
    
    print("📁 Shared Templates:")
    shared_templates = base_dir / "shared" / "templates"
    if shared_templates.exists():
        for file in shared_templates.rglob("*.html"):
            rel_path = file.relative_to(shared_templates)
            print(f"  📄 {rel_path}")
    
    print("\n📁 Standalone App Templates:")
    standalone_templates = base_dir / "standalone-apps" / "timesheet" / "timesheet_app" / "templates"
    if standalone_templates.exists():
        for file in standalone_templates.rglob("*.html"):
            rel_path = file.relative_to(standalone_templates)
            print(f"  📄 {rel_path}")
    
    print("\n📁 FamilyHub Templates:")
    familyhub_templates = base_dir / "FamilyHub" / "templates"
    if familyhub_templates.exists():
        for file in familyhub_templates.rglob("*.html"):
            rel_path = file.relative_to(familyhub_templates)
            print(f"  📄 {rel_path}")

if __name__ == "__main__":
    print(f"{Colors.BLUE}{Colors.BOLD}Simplified Template Structure Verification{Colors.ENDC}")
    print("=" * 60)
    
    show_file_structure()
    success = verify_new_structure()
    
    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ VERIFICATION PASSED - New structure is working!{Colors.ENDC}")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ VERIFICATION FAILED - Structure needs fixes!{Colors.ENDC}")
        sys.exit(1)
