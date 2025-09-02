#!/usr/bin/env python
"""
Comprehensive Architecture Compliance Check for FamilyHub
Verifies all architecture requirements are met according to instructions.
"""

import os
import sys
from pathlib import Path

class ArchitectureChecker:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.violations = []
        self.checks_passed = 0
        self.checks_failed = 0
    
    def log_violation(self, level, message):
        """Log an architecture violation."""
        self.violations.append(f"{level}: {message}")
        if level in ['ERROR', 'CRITICAL']:
            self.checks_failed += 1
        else:
            self.checks_passed += 1
    
    def log_success(self, message):
        """Log a successful check."""
        self.checks_passed += 1
        print(f"✅ {message}")
    
    def check_project_structure(self):
        """Check the fundamental project structure."""
        print("\n🏗️  CHECKING PROJECT STRUCTURE")
        print("=" * 50)
        
        # Check FamilyHub directory exists
        familyhub_path = self.workspace_path / "FamilyHub"
        if familyhub_path.exists():
            self.log_success("FamilyHub main directory exists")
        else:
            self.log_violation("CRITICAL", "FamilyHub main directory missing")
        
        # Check standalone-apps directory exists
        standalone_path = self.workspace_path / "standalone-apps"
        if standalone_path.exists():
            self.log_success("standalone-apps directory exists")
        else:
            self.log_violation("CRITICAL", "standalone-apps directory missing")
        
        # Check FamilyHub apps directory exists and is for symbolic links only
        apps_path = familyhub_path / "apps"
        if apps_path.exists():
            self.log_success("FamilyHub/apps directory exists")
        else:
            self.log_violation("ERROR", "FamilyHub/apps directory missing")
    
    def check_symbolic_links(self):
        """Check symbolic link implementation."""
        print("\n🔗 CHECKING SYMBOLIC LINKS")
        print("=" * 50)
        
        familyhub_apps = self.workspace_path / "FamilyHub" / "apps"
        
        # Check timesheet_app symbolic link
        timesheet_link = familyhub_apps / "timesheet_app"
        if timesheet_link.exists():
            if timesheet_link.is_symlink() or os.path.islink(str(timesheet_link)):
                self.log_success("timesheet_app symbolic link exists")
            else:
                self.log_violation("ERROR", "timesheet_app exists but is not a symbolic link")
        else:
            self.log_violation("ERROR", "timesheet_app symbolic link missing")
    
    def check_template_duplication(self):
        """Check for template duplication violations."""
        print("\n📄 CHECKING TEMPLATE DUPLICATION")
        print("=" * 50)
        
        # Check that templates don't exist in FamilyHub/apps as real files
        familyhub_templates = self.workspace_path / "FamilyHub" / "apps" / "timesheet_app" / "templates"
        standalone_templates = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "templates"
        
        if standalone_templates.exists():
            self.log_success("Standalone templates directory exists")
            
            # Count templates in standalone
            template_files = list(standalone_templates.rglob("*.html"))
            if len(template_files) > 0:
                self.log_success(f"Found {len(template_files)} template files in standalone")
            else:
                self.log_violation("WARNING", "No template files found in standalone")
        else:
            self.log_violation("CRITICAL", "Standalone templates directory missing")
    
    def check_conditional_extends_issue(self):
        """Check for the conditional extends issue that breaks Django."""
        print("\n🚨 CHECKING CONDITIONAL EXTENDS PATTERN")
        print("=" * 50)
        
        dashboard_path = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "templates" / "timesheet" / "dashboard.html"
        
        if dashboard_path.exists():
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for conditional extends pattern
            if "{% if integrated_mode %}" in content and "{% extends" in content:
                self.log_violation("CRITICAL", "dashboard.html uses conditional extends - Django doesn't support this!")
                self.log_violation("ERROR", "This will cause TemplateSyntaxError in standalone mode")
                return False
            else:
                self.log_success("dashboard.html doesn't use conditional extends")
                return True
        else:
            self.log_violation("ERROR", "dashboard.html template missing")
            return False
    
    def check_separate_templates_exist(self):
        """Check if the correct separate templates exist."""
        print("\n📑 CHECKING SEPARATE TEMPLATE SOLUTION")
        print("=" * 50)
        
        template_dir = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "templates" / "timesheet"
        
        # Check for the separate template files
        integrated_template = template_dir / "dashboard_integrated.html"
        standalone_template = template_dir / "dashboard_standalone.html"
        content_template = template_dir / "dashboard_content.html"
        
        if integrated_template.exists():
            self.log_success("dashboard_integrated.html exists")
        else:
            self.log_violation("ERROR", "dashboard_integrated.html missing")
        
        if standalone_template.exists():
            self.log_success("dashboard_standalone.html exists")
        else:
            self.log_violation("ERROR", "dashboard_standalone.html missing")
        
        if content_template.exists():
            self.log_success("dashboard_content.html exists")
        else:
            self.log_violation("ERROR", "dashboard_content.html missing")
    
    def check_view_template_selection(self):
        """Check if views properly select templates based on integration mode."""
        print("\n👀 CHECKING VIEW TEMPLATE SELECTION")
        print("=" * 50)
        
        views_path = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "views.py"
        
        if views_path.exists():
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for template selection logic
            if "dashboard_integrated.html" in content or "dashboard_standalone.html" in content:
                self.log_success("Views contain template selection logic")
            else:
                self.log_violation("WARNING", "Views may not have proper template selection logic")
        else:
            self.log_violation("ERROR", "views.py file missing")
    
    def check_context_processors(self):
        """Check context processor implementation."""
        print("\n🔄 CHECKING CONTEXT PROCESSORS")
        print("=" * 50)
        
        # Check standalone context processor
        standalone_cp = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "context_processors.py"
        
        if standalone_cp.exists():
            with open(standalone_cp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "integration_context" in content:
                self.log_success("integration_context function exists in standalone")
            else:
                self.log_violation("ERROR", "integration_context function missing in standalone")
        else:
            self.log_violation("ERROR", "context_processors.py missing in standalone")
    
    def check_settings_configuration(self):
        """Check settings configuration for both modes."""
        print("\n⚙️  CHECKING SETTINGS CONFIGURATION")
        print("=" * 50)
        
        # Check FamilyHub settings
        familyhub_settings = self.workspace_path / "FamilyHub" / "FamilyHub" / "settings" / "base.py"
        
        if familyhub_settings.exists():
            with open(familyhub_settings, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "apps.timesheet_app" in content:
                self.log_success("FamilyHub settings include apps.timesheet_app")
            else:
                self.log_violation("WARNING", "FamilyHub settings may not include timesheet app")
            
            if "integration_context" in content:
                self.log_success("FamilyHub settings include integration context processor")
            else:
                self.log_violation("WARNING", "FamilyHub settings may not include context processor")
        
        # Check standalone settings
        standalone_settings = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_project" / "settings.py"
        
        if standalone_settings.exists():
            with open(standalone_settings, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "timesheet_app" in content:
                self.log_success("Standalone settings include timesheet_app")
            else:
                self.log_violation("WARNING", "Standalone settings may not include timesheet app")
    
    def suggest_fixes(self):
        """Suggest fixes for identified issues."""
        print("\n🔧 SUGGESTED FIXES")
        print("=" * 50)
        
        # Check if conditional extends is the main issue
        dashboard_path = self.workspace_path / "standalone-apps" / "timesheet" / "timesheet_app" / "templates" / "timesheet" / "dashboard.html"
        
        if dashboard_path.exists():
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "{% if integrated_mode %}" in content and "{% extends" in content:
                print("🚨 CRITICAL FIX NEEDED:")
                print("   The dashboard.html template uses conditional extends which Django doesn't support.")
                print("   This causes TemplateSyntaxError in standalone mode.")
                print("")
                print("💡 SOLUTION:")
                print("   1. Use separate templates: dashboard_integrated.html and dashboard_standalone.html")
                print("   2. Extract common content to dashboard_content.html")  
                print("   3. Update views to select template based on integration mode")
                print("")
                print("📝 IMPLEMENTATION:")
                print("   - dashboard_integrated.html: extends 'base.html' for FamilyHub")
                print("   - dashboard_standalone.html: extends 'timesheet/base.html' for standalone")
                print("   - Both include dashboard_content.html for shared content")
                print("   - View chooses template based on integration_mode")
    
    def run_all_checks(self):
        """Run all architecture compliance checks."""
        print("🔍 FAMILYHUB ARCHITECTURE COMPLIANCE CHECK")
        print("=" * 60)
        
        self.check_project_structure()
        self.check_symbolic_links()
        self.check_template_duplication()
        conditional_ok = self.check_conditional_extends_issue()
        self.check_separate_templates_exist()
        self.check_view_template_selection()
        self.check_context_processors()
        self.check_settings_configuration()
        
        # Print violations
        if self.violations:
            print("\n❌ VIOLATIONS FOUND:")
            print("=" * 50)
            for violation in self.violations:
                if violation.startswith("CRITICAL"):
                    print(f"🚨 {violation}")
                elif violation.startswith("ERROR"):
                    print(f"❌ {violation}")
                elif violation.startswith("WARNING"):
                    print(f"⚠️  {violation}")
        
        # Print summary
        print(f"\n📊 SUMMARY")
        print("=" * 50)
        print(f"✅ Checks Passed: {self.checks_passed}")
        print(f"❌ Checks Failed: {self.checks_failed}")
        print(f"📝 Total Issues: {len(self.violations)}")
        
        if self.checks_failed > 0 or not conditional_ok:
            print(f"\n🚨 ARCHITECTURE COMPLIANCE: FAILED")
            self.suggest_fixes()
        else:
            print(f"\n🎉 ARCHITECTURE COMPLIANCE: PASSED")
        
        return self.checks_failed == 0 and conditional_ok

if __name__ == '__main__':
    workspace_path = r'C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace'
    checker = ArchitectureChecker(workspace_path)
    compliance_ok = checker.run_all_checks()
    
    sys.exit(0 if compliance_ok else 1)
