#!/usr/bin/env python
"""
Database Migration Verification Test
Tests that timesheet database tables exist and are properly structured
"""

import os
import django
from django.db import connection

def test_database_migrations():
    """Test database migrations and table structure"""
    print("🔍 Testing Database Migration Configuration")
    print("=" * 60)
    
    try:
        # Get database connection
        cursor = connection.cursor()
        
        # Check for timesheet tables
        print("1. Checking for timesheet database tables...")
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        timesheet_tables = [table for table in tables if 'timesheet' in table]
        
        expected_tables = ['timesheet_job', 'timesheet_timeentry']
        
        for table in expected_tables:
            if table in timesheet_tables:
                print(f"   ✅ Table exists: {table}")
            else:
                print(f"   ❌ Table missing: {table}")
        
        print(f"\n2. Found {len(timesheet_tables)} timesheet tables:")
        for table in timesheet_tables:
            print(f"   - {table}")
        
        # Check table structure for Job model
        if 'timesheet_job' in timesheet_tables:
            print("\n3. Checking timesheet_job table structure...")
            cursor.execute("PRAGMA table_info(timesheet_job);")
            columns = cursor.fetchall()
            
            expected_columns = ['id', 'name', 'address', 'user_id', 'created_at', 'updated_at', 'description']
            found_columns = [col[1] for col in columns]
            
            for col in expected_columns:
                if col in found_columns:
                    print(f"   ✅ Column exists: {col}")
                else:
                    print(f"   ⚠️  Column missing: {col}")
        
        # Check table structure for TimeEntry model
        if 'timesheet_timeentry' in timesheet_tables:
            print("\n4. Checking timesheet_timeentry table structure...")
            cursor.execute("PRAGMA table_info(timesheet_timeentry);")
            columns = cursor.fetchall()
            
            expected_columns = ['id', 'user_id', 'job_id', 'date', 'start_time', 'end_time', 'break_duration']
            found_columns = [col[1] for col in columns]
            
            for col in expected_columns:
                if col in found_columns:
                    print(f"   ✅ Column exists: {col}")
                else:
                    print(f"   ❌ Column missing: {col}")
        
        # Test model imports and basic operations
        print("\n5. Testing model operations...")
        from timesheet.models import Job, TimeEntry
        
        # Count existing records
        job_count = Job.objects.count()
        entry_count = TimeEntry.objects.count()
        
        print(f"   ✅ Job model operational - {job_count} jobs in database")
        print(f"   ✅ TimeEntry model operational - {entry_count} entries in database")
        
        print("\n🎉 Database migration verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database Migration Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_database_migrations()
    
    if success:
        print("\n✅ Database Migration Test: PASSED")
    else:
        print("\n❌ Database Migration Test: FAILED")
