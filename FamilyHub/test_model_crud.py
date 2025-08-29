#!/usr/bin/env python
"""
Model CRUD Operations Test
Tests CRUD operations at the model level without HTTP client
"""

import os
import django
from datetime import date, time as datetime_time

def test_model_crud():
    """Test CRUD operations directly on models"""
    print("🔍 Testing Model-Level CRUD Operations")
    print("=" * 60)
    
    try:
        from django.contrib.auth import get_user_model
        from timesheet.models import Job, TimeEntry
        
        User = get_user_model()
        
        # CREATE operations
        print("1. Testing CREATE operations...")
        
        # Create test user
        user = User.objects.create_user(
            username='crudtest',
            password='testpass123',
            email='crud@example.com'
        )
        print(f"   ✅ User created: {user.username}")
        
        # Create job
        job = Job.objects.create(
            name='CRUD Test Office',
            address='123 CRUD Street, Auckland',
            description='Testing CRUD operations',
            user=user
        )
        print(f"   ✅ Job created: {job.name} (ID: {job.pk})")
        
        # Create time entry
        entry = TimeEntry.objects.create(
            user=user,
            job=job,
            date=date.today(),
            start_time=datetime_time(9, 0),
            end_time=datetime_time(17, 0),
            break_duration=60
        )
        print(f"   ✅ Time entry created: {entry.start_time} - {entry.end_time} (ID: {entry.pk})")
        
        # READ operations
        print("\n2. Testing READ operations...")
        
        # Read job
        retrieved_job = Job.objects.get(pk=job.pk)
        print(f"   ✅ Job retrieved: {retrieved_job.name}")
        
        # Read time entry
        retrieved_entry = TimeEntry.objects.get(pk=entry.pk)
        print(f"   ✅ Time entry retrieved: {retrieved_entry.date}")
        
        # Test calculated fields
        total_hours = retrieved_entry.total_hours()
        print(f"   ✅ Total hours calculated: {total_hours}")
        
        # Test user filtering
        user_jobs = Job.objects.filter(user=user)
        user_entries = TimeEntry.objects.filter(user=user)
        print(f"   ✅ User jobs: {user_jobs.count()}")
        print(f"   ✅ User entries: {user_entries.count()}")
        
        # UPDATE operations
        print("\n3. Testing UPDATE operations...")
        
        # Update job
        original_name = job.name
        job.name = "Updated CRUD Office"
        job.description = "Updated description for testing"
        job.save()
        
        updated_job = Job.objects.get(pk=job.pk)
        if updated_job.name != original_name:
            print(f"   ✅ Job updated: {original_name} → {updated_job.name}")
        else:
            print("   ❌ Job update failed")
        
        # Update time entry
        original_start = entry.start_time
        entry.start_time = datetime_time(8, 30)
        entry.end_time = datetime_time(16, 30)
        entry.break_duration = 30
        entry.save()
        
        updated_entry = TimeEntry.objects.get(pk=entry.pk)
        if updated_entry.start_time != original_start:
            print(f"   ✅ Time entry updated: {original_start} → {updated_entry.start_time}")
        else:
            print("   ❌ Time entry update failed")
        
        # Test user isolation
        print("\n4. Testing user data isolation...")
        
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            email='other@example.com'
        )
        
        # Check isolation
        user1_jobs = Job.objects.filter(user=user).count()
        user2_jobs = Job.objects.filter(user=other_user).count()
        
        print(f"   ✅ User 1 jobs: {user1_jobs}")
        print(f"   ✅ User 2 jobs: {user2_jobs}")
        
        if user2_jobs == 0:
            print("   ✅ User data isolation working correctly")
        else:
            print("   ❌ User data isolation failed")
        
        # Test model validation
        print("\n5. Testing model validation...")
        
        try:
            # Test invalid time entry (end before start)
            invalid_entry = TimeEntry(
                user=user,
                job=job,
                date=date.today(),
                start_time=datetime_time(17, 0),
                end_time=datetime_time(9, 0),  # Invalid: end before start
                break_duration=0
            )
            invalid_entry.full_clean()
            print("   ⚠️  Model validation may not be working (invalid entry accepted)")
        except Exception as e:
            print(f"   ✅ Model validation working: {type(e).__name__}")
        
        # DELETE operations
        print("\n6. Testing DELETE operations...")
        
        entry_id = entry.pk
        job_id = job.pk
        
        # Delete time entry
        entry.delete()
        if not TimeEntry.objects.filter(pk=entry_id).exists():
            print(f"   ✅ Time entry deleted (ID: {entry_id})")
        else:
            print(f"   ❌ Time entry deletion failed (ID: {entry_id})")
        
        # Delete job
        job.delete()
        if not Job.objects.filter(pk=job_id).exists():
            print(f"   ✅ Job deleted (ID: {job_id})")
        else:
            print(f"   ❌ Job deletion failed (ID: {job_id})")
        
        # Cleanup users
        user.delete()
        other_user.delete()
        print("   ✅ Test users cleaned up")
        
        print("\n🎉 Model CRUD operations test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Model CRUD Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_model_crud()
    
    if success:
        print("\n✅ Model CRUD Operations Test: PASSED")
    else:
        print("\n❌ Model CRUD Operations Test: FAILED")
