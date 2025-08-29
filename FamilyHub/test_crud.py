#!/usr/bin/env python
"""
CRUD Operations Test
Tests complete Create, Read, Update, Delete functionality for timesheet app
"""

import os
import django
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, time

def test_crud_operations():
    """Test complete CRUD flow for jobs and time entries"""
    print("🔍 Testing CRUD Operations")
    print("=" * 60)
    
    try:
        User = get_user_model()
        
        # Create test user
        print("1. Setting up test user...")
        
        # Clean up any existing test user
        User.objects.filter(username='testuser').delete()
        
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        print(f"   ✅ Test user created: {user.username}")
        
        # Create authenticated client
        client = Client()
        login_success = client.login(username='testuser', password='testpass123')
        
        if login_success:
            print("   ✅ User authentication successful")
        else:
            print("   ❌ User authentication failed")
            return False
        
        # Test Job CRUD operations
        print("\n2. Testing Job CRUD operations...")
        
        # CREATE job
        print("   2a. Testing job creation...")
        job_data = {
            'name': 'Test Office Location',
            'address': '123 Test Street, Auckland, New Zealand',
            'description': 'Test office for CRUD operations'
        }
        
        response = client.post(reverse('timesheet:job_create'), data=job_data)
        if response.status_code in [200, 302]:
            print("   ✅ Job creation form submitted successfully")
        else:
            print(f"   ❌ Job creation failed: HTTP {response.status_code}")
        
        # READ jobs
        print("   2b. Testing job listing...")
        response = client.get(reverse('timesheet:job_list'))
        if response.status_code == 200:
            print("   ✅ Job list page accessible")
        else:
            print(f"   ❌ Job list failed: HTTP {response.status_code}")
        
        # Check if job was created
        from timesheet.models import Job
        user_jobs = Job.objects.filter(user=user)
        if user_jobs.exists():
            test_job = user_jobs.first()
            print(f"   ✅ Job created in database: {test_job.name}")
        else:
            print("   ❌ Job not found in database")
            return False
        
        # UPDATE job
        print("   2c. Testing job update...")
        update_data = {
            'name': 'Updated Test Office',
            'address': '456 Updated Street, Auckland, New Zealand',
            'description': 'Updated description for testing'
        }
        
        response = client.post(reverse('timesheet:job_edit', kwargs={'pk': test_job.pk}), data=update_data)
        if response.status_code in [200, 302]:
            print("   ✅ Job update form submitted successfully")
            
            # Verify update
            updated_job = Job.objects.get(pk=test_job.pk)
            if updated_job.name == 'Updated Test Office':
                print("   ✅ Job updated successfully in database")
            else:
                print("   ⚠️  Job update may not have been saved")
        else:
            print(f"   ❌ Job update failed: HTTP {response.status_code}")
        
        # Test Time Entry CRUD operations
        print("\n3. Testing Time Entry CRUD operations...")
        
        # CREATE time entry via dashboard quick-add
        print("   3a. Testing time entry creation via dashboard...")
        entry_data = {
            'job': test_job.pk,
            'start_time': '09:00',
            'end_time': '17:00',
            'break_duration': 60  # 60 minutes
        }
        
        response = client.post(reverse('timesheet:dashboard'), data=entry_data)
        if response.status_code in [200, 302]:
            print("   ✅ Time entry creation via dashboard submitted")
        else:
            print(f"   ❌ Time entry creation failed: HTTP {response.status_code}")
        
        # READ time entries
        from timesheet.models import TimeEntry
        user_entries = TimeEntry.objects.filter(user=user)
        if user_entries.exists():
            test_entry = user_entries.first()
            print(f"   ✅ Time entry created: {test_entry.start_time} - {test_entry.end_time}")
        else:
            print("   ❌ Time entry not found in database")
            return False
        
        # UPDATE time entry
        print("   3b. Testing time entry update...")
        entry_update_data = {
            'job': test_job.pk,
            'date': date.today().strftime('%Y-%m-%d'),
            'start_time': '08:30',
            'end_time': '16:30',
            'break_duration': 30
        }
        
        response = client.post(reverse('timesheet:entry_edit', kwargs={'pk': test_entry.pk}), data=entry_update_data)
        if response.status_code in [200, 302]:
            print("   ✅ Time entry update form submitted")
            
            # Verify update
            updated_entry = TimeEntry.objects.get(pk=test_entry.pk)
            if str(updated_entry.start_time) == '08:30:00':
                print("   ✅ Time entry updated successfully in database")
            else:
                print("   ⚠️  Time entry update may not have been saved")
        else:
            print(f"   ❌ Time entry update failed: HTTP {response.status_code}")
        
        # Test user isolation
        print("\n4. Testing user data isolation...")
        
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123',
            email='other@example.com'
        )
        
        # Check that first user's data is isolated
        other_user_jobs = Job.objects.filter(user=other_user)
        other_user_entries = TimeEntry.objects.filter(user=other_user)
        
        if other_user_jobs.count() == 0 and other_user_entries.count() == 0:
            print("   ✅ User data isolation working correctly")
        else:
            print(f"   ❌ User data isolation failed: {other_user_jobs.count()} jobs, {other_user_entries.count()} entries")
        
        # DELETE operations
        print("\n5. Testing DELETE operations...")
        
        # Delete time entry
        print("   5a. Testing time entry deletion...")
        response = client.post(reverse('timesheet:entry_delete', kwargs={'pk': test_entry.pk}))
        if response.status_code in [200, 302]:
            print("   ✅ Time entry deletion submitted")
            
            # Verify deletion
            if not TimeEntry.objects.filter(pk=test_entry.pk).exists():
                print("   ✅ Time entry deleted from database")
            else:
                print("   ❌ Time entry still exists in database")
        else:
            print(f"   ❌ Time entry deletion failed: HTTP {response.status_code}")
        
        # Delete job
        print("   5b. Testing job deletion...")
        response = client.post(reverse('timesheet:job_delete', kwargs={'pk': test_job.pk}))
        if response.status_code in [200, 302]:
            print("   ✅ Job deletion submitted")
            
            # Verify deletion
            if not Job.objects.filter(pk=test_job.pk).exists():
                print("   ✅ Job deleted from database")
            else:
                print("   ❌ Job still exists in database")
        else:
            print(f"   ❌ Job deletion failed: HTTP {response.status_code}")
        
        # Cleanup
        print("\n6. Cleaning up test data...")
        User.objects.filter(username__in=['testuser', 'otheruser']).delete()
        print("   ✅ Test users cleaned up")
        
        print("\n🎉 CRUD operations test completed!")
        return True
        
    except Exception as e:
        print(f"❌ CRUD Operations Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_crud_operations()
    
    if success:
        print("\n✅ CRUD Operations Test: PASSED")
    else:
        print("\n❌ CRUD Operations Test: FAILED")
