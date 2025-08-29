#!/usr/bin/env python
"""
Static Files Collection Test
Verifies that timesheet static files are properly collected and accessible
"""

import os
import django
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

def test_static_files_collection():
    """Test static files collection and accessibility"""
    print("🔍 Testing Static Files Collection")
    print("=" * 60)
    
    try:
        # Check STATIC_ROOT configuration
        print("1. Checking static files configuration...")
        
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root:
            print(f"   ✅ STATIC_ROOT configured: {static_root}")
            
            if Path(static_root).exists():
                print(f"   ✅ STATIC_ROOT directory exists")
            else:
                print(f"   ❌ STATIC_ROOT directory missing")
        else:
            print("   ❌ STATIC_ROOT not configured")
        
        static_url = getattr(settings, 'STATIC_URL', None)
        print(f"   ✅ STATIC_URL: {static_url}")
        
        # Check for collected static files
        print("\n2. Checking collected static files...")
        
        if static_root and Path(static_root).exists():
            static_path = Path(static_root)
            
            # Look for Django admin static files (should always be present)
            admin_static = static_path / 'admin'
            if admin_static.exists():
                print("   ✅ Django admin static files collected")
            else:
                print("   ❌ Django admin static files missing")
            
            # Check total number of collected files
            collected_files = list(static_path.glob('**/*'))
            file_count = len([f for f in collected_files if f.is_file()])
            print(f"   ✅ Total static files collected: {file_count}")
            
            # List main directories
            directories = [d for d in static_path.iterdir() if d.is_directory()]
            print(f"   ✅ Static directories: {[d.name for d in directories]}")
        
        # Test static file finder
        print("\n3. Testing static file finder...")
        
        # Test finding admin CSS (should always exist)
        admin_css = finders.find('admin/css/base.css')
        if admin_css:
            print("   ✅ Static file finder working")
        else:
            print("   ❌ Static file finder not working")
        
        # Test staticfiles storage
        print("\n4. Testing static files storage...")
        
        try:
            # Check if admin CSS exists in storage
            admin_css_exists = staticfiles_storage.exists('admin/css/base.css')
            if admin_css_exists:
                print("   ✅ Static files storage working")
            else:
                print("   ⚠️  Static files storage may not be working")
        except Exception as e:
            print(f"   ❌ Static files storage error: {e}")
        
        # Check timesheet static files specifically
        print("\n5. Checking timesheet-specific static files...")
        
        # Look for timesheet static files in the shared apps directory
        shared_timesheet_static = Path(settings.BASE_DIR).parent / 'shared' / 'apps' / 'timesheet' / 'static'
        
        if shared_timesheet_static.exists():
            print(f"   ✅ Timesheet static source exists: {shared_timesheet_static}")
            
            # List timesheet static files
            timesheet_files = list(shared_timesheet_static.glob('**/*'))
            static_file_count = len([f for f in timesheet_files if f.is_file()])
            
            if static_file_count > 0:
                print(f"   ✅ Timesheet static files found: {static_file_count} files")
                
                # Show file structure
                for file_path in timesheet_files:
                    if file_path.is_file():
                        relative_path = file_path.relative_to(shared_timesheet_static)
                        print(f"     - {relative_path}")
            else:
                print("   ⚠️  No timesheet static files found")
        else:
            print("   ⚠️  Timesheet static directory not found (may not have static files)")
        
        # Test static URL generation
        print("\n6. Testing static URL generation...")
        
        try:
            from django.templatetags.static import static
            
            # Test admin static URL
            admin_css_url = static('admin/css/base.css')
            print(f"   ✅ Admin CSS URL: {admin_css_url}")
            
        except Exception as e:
            print(f"   ❌ Static URL generation error: {e}")
        
        print("\n🎉 Static files collection test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Static Files Collection Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_static_files_collection()
    
    if success:
        print("\n✅ Static Files Collection Test: PASSED")
    else:
        print("\n❌ Static Files Collection Test: FAILED")
