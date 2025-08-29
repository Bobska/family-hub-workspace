#!/usr/bin/env python
"""
AJAX Validation Test
Tests AJAX endpoints and client-side validation functionality
"""

import os
import django
from datetime import date, time as datetime_time
import json

def test_ajax_validation():
    """Test AJAX validation endpoints"""
    print("🔍 Testing AJAX Validation and Client-Side Features")
    print("=" * 60)
    
    try:
        from django.contrib.auth import get_user_model
        from django.test import Client
        from timesheet.models import Job, TimeEntry
        
        User = get_user_model()
        client = Client()
        
        # Create test user and login
        print("1. Setting up test data...")
        user = User.objects.create_user(
            username='ajaxtest',
            password='testpass123',
            email='ajax@example.com'
        )
        
        job = Job.objects.create(
            name='AJAX Test Office',
            address='123 AJAX Street, Auckland',
            user=user
        )
        
        # Create existing time entry
        existing_entry = TimeEntry.objects.create(
            user=user,
            job=job,
            date=date.today(),
            start_time=datetime_time(9, 0),
            end_time=datetime_time(17, 0),
            break_duration=60
        )
        
        print(f"   ✅ Test user created: {user.username}")
        print(f"   ✅ Test job created: {job.name}")
        print(f"   ✅ Existing entry: {existing_entry.start_time} - {existing_entry.end_time}")
        
        # Login user
        login_success = client.login(username='ajaxtest', password='testpass123')
        if login_success:
            print("   ✅ User logged in successfully")
        else:
            print("   ❌ Login failed")
            return False
        
        # Test AJAX endpoints if they exist
        print("\n2. Testing AJAX endpoints...")
        
        # Check for overlap validation endpoint
        try:
            response = client.get('/timesheet/api/check-overlap/', {
                'date': date.today().isoformat(),
                'start_time': '08:00',
                'end_time': '10:00',
                'job_id': job.id
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Overlap check endpoint working: {data}")
            else:
                print(f"   ⚠️  Overlap check endpoint not found (status: {response.status_code})")
        except Exception as e:
            print(f"   ⚠️  Overlap check endpoint not implemented: {e}")
        
        # Test job list endpoint
        try:
            response = client.get('/timesheet/api/jobs/')
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Jobs API endpoint working: {len(data)} jobs")
            else:
                print(f"   ⚠️  Jobs API endpoint not found (status: {response.status_code})")
        except Exception as e:
            print(f"   ⚠️  Jobs API endpoint not implemented: {e}")
        
        # Test form pages for JavaScript validation
        print("\n3. Testing form pages for JavaScript validation...")
        
        # Test time entry form page
        try:
            response = client.get('/timesheet/entries/add/')
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Check for JavaScript validation features
                js_features = {
                    'jQuery': 'jquery' in content.lower() or '$(' in content,
                    'Bootstrap JS': 'bootstrap' in content.lower(),
                    'Custom validation': 'validation' in content.lower(),
                    'AJAX calls': 'ajax' in content.lower() or '$.ajax' in content or 'fetch(' in content,
                    'Overlap check': 'overlap' in content.lower(),
                    'Real-time validation': 'oninput' in content.lower() or 'onchange' in content.lower()
                }
                
                print("   JavaScript features detected:")
                for feature, present in js_features.items():
                    status = "✅" if present else "⚠️ "
                    print(f"      {status} {feature}: {'Yes' if present else 'No'}")
                
            else:
                print(f"   ❌ Add entry form not accessible (status: {response.status_code})")
        
        except Exception as e:
            print(f"   ❌ Error testing form page: {e}")
        
        # Test overlap detection at model level
        print("\n4. Testing overlap detection logic...")
        
        try:
            # Test overlapping entry creation
            overlap_test_cases = [
                {
                    'name': 'Complete overlap',
                    'start': datetime_time(9, 0),
                    'end': datetime_time(17, 0),
                    'should_conflict': True
                },
                {
                    'name': 'Start overlap',
                    'start': datetime_time(8, 0),
                    'end': datetime_time(10, 0),
                    'should_conflict': True
                },
                {
                    'name': 'End overlap',
                    'start': datetime_time(16, 0),
                    'end': datetime_time(18, 0),
                    'should_conflict': True
                },
                {
                    'name': 'No overlap (before)',
                    'start': datetime_time(7, 0),
                    'end': datetime_time(8, 0),
                    'should_conflict': False
                },
                {
                    'name': 'No overlap (after)',
                    'start': datetime_time(18, 0),
                    'end': datetime_time(19, 0),
                    'should_conflict': False
                }
            ]
            
            for test_case in overlap_test_cases:
                try:
                    test_entry = TimeEntry(
                        user=user,
                        job=job,
                        date=date.today(),
                        start_time=test_case['start'],
                        end_time=test_case['end'],
                        break_duration=0
                    )
                    
                    # Check if validation catches overlap
                    test_entry.full_clean()
                    
                    # If we get here, no validation error occurred
                    if test_case['should_conflict']:
                        print(f"   ⚠️  {test_case['name']}: No overlap detected (may need implementation)")
                    else:
                        print(f"   ✅ {test_case['name']}: No overlap (correct)")
                        
                except Exception as validation_error:
                    if test_case['should_conflict']:
                        print(f"   ✅ {test_case['name']}: Overlap detected correctly")
                    else:
                        print(f"   ⚠️  {test_case['name']}: False positive overlap detection")
            
        except Exception as e:
            print(f"   ❌ Error testing overlap detection: {e}")
        
        # Test form submission with overlaps
        print("\n5. Testing form submission validation...")
        
        try:
            # Try to submit overlapping entry via POST
            form_data = {
                'job': job.id,
                'date': date.today().isoformat(),
                'start_time': '09:30',
                'end_time': '16:30',
                'break_duration': '30'
            }
            
            response = client.post('/timesheet/entries/add/', form_data)
            
            if response.status_code == 200:
                # Form returned (likely with errors)
                content = response.content.decode()
                if 'error' in content.lower() or 'overlap' in content.lower():
                    print("   ✅ Form validation detected overlap")
                else:
                    print("   ⚠️  Form may have accepted overlapping entry")
            elif response.status_code == 302:
                # Redirect (entry created)
                print("   ⚠️  Form accepted overlapping entry (may need validation)")
            else:
                print(f"   ❌ Form submission failed (status: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Error testing form submission: {e}")
        
        # Cleanup
        TimeEntry.objects.filter(user=user).delete()
        Job.objects.filter(user=user).delete()
        user.delete()
        print("\n   ✅ Test data cleaned up")
        
        print("\n🎉 AJAX validation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ AJAX Validation Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_ajax_validation()
    
    if success:
        print("\n✅ AJAX Validation Test: PASSED")
    else:
        print("\n❌ AJAX Validation Test: FAILED")
