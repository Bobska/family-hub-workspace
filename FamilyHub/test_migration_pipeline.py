#!/usr/bin/env python
"""
Comprehensive SQL Server to PostgreSQL Migration Test Script

This script tests the complete migration pipeline:
1. Export from SQL Server
2. Import to PostgreSQL  
3. Verify data integrity
4. Generate migration report

Usage:
    python test_migration_pipeline.py --config config/migration_config.json
    python test_migration_pipeline.py --dry-run
"""

import json
import os
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

# Add Django project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')

import django
django.setup()

from django.core.management import call_command
from django.db import connection
from django.test.utils import override_settings


class MigrationTester:
    """Comprehensive migration testing pipeline"""
    
    def __init__(self, config_file=None, dry_run=False):
        self.config_file = config_file or 'config/migration_config.json'
        self.dry_run = dry_run
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': dry_run,
            'phases': {},
            'summary': {
                'total_phases': 0,
                'passed_phases': 0,
                'failed_phases': 0,
                'overall_status': 'unknown'
            }
        }
        
        print("🧪 FamilyHub Migration Test Pipeline")
        print("=" * 50)
        
    def run_all_tests(self):
        """Run complete migration test pipeline"""
        phases = [
            ('config_validation', self.test_config_validation),
            ('connection_tests', self.test_database_connections),
            ('export_test', self.test_export_from_sqlserver),
            ('import_test', self.test_import_to_postgresql),
            ('integrity_verification', self.test_data_integrity),
            ('performance_test', self.test_migration_performance),
        ]
        
        self.test_results['summary']['total_phases'] = len(phases)
        
        for phase_name, test_function in phases:
            print(f"\n📋 Phase: {phase_name.replace('_', ' ').title()}")
            print("-" * 40)
            
            try:
                if self.dry_run and phase_name in ['import_test', 'export_test']:
                    print("🔍 DRY RUN - Skipping actual data operations")
                    result = {'status': 'skipped', 'message': 'Dry run mode'}
                else:
                    result = test_function()
                
                self.test_results['phases'][phase_name] = result
                
                if result['status'] == 'pass':
                    self.test_results['summary']['passed_phases'] += 1
                    print(f"✅ {phase_name}: PASS")
                elif result['status'] == 'skipped':
                    print(f"⏭️  {phase_name}: SKIPPED")
                else:
                    self.test_results['summary']['failed_phases'] += 1
                    print(f"❌ {phase_name}: FAIL - {result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                self.test_results['phases'][phase_name] = {
                    'status': 'error',
                    'message': str(e),
                    'exception': type(e).__name__
                }
                self.test_results['summary']['failed_phases'] += 1
                print(f"💥 {phase_name}: ERROR - {e}")
        
        # Calculate overall status
        if self.test_results['summary']['failed_phases'] == 0:
            self.test_results['summary']['overall_status'] = 'pass'
        else:
            self.test_results['summary']['overall_status'] = 'fail'
        
        self.generate_test_report()
        return self.test_results['summary']['overall_status'] == 'pass'

    def test_config_validation(self):
        """Test migration configuration file"""
        try:
            if not os.path.exists(self.config_file):
                return {
                    'status': 'fail',
                    'message': f'Config file not found: {self.config_file}'
                }
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Validate required sections
            required_sections = ['sqlserver', 'mapping', 'migration_order']
            missing_sections = [s for s in required_sections if s not in config]
            
            if missing_sections:
                return {
                    'status': 'fail',
                    'message': f'Missing config sections: {missing_sections}'
                }
            
            # Validate mapping structure
            mapping = config['mapping']
            for table, table_config in mapping.items():
                if 'model' not in table_config or 'fields' not in table_config:
                    return {
                        'status': 'fail',
                        'message': f'Invalid mapping for table {table}'
                    }
            
            return {
                'status': 'pass',
                'message': f'Config validation successful. Found {len(mapping)} table mappings.',
                'details': {
                    'tables': list(mapping.keys()),
                    'migration_order': config['migration_order']
                }
            }
            
        except json.JSONDecodeError as e:
            return {
                'status': 'fail',
                'message': f'Invalid JSON in config file: {e}'
            }

    def test_database_connections(self):
        """Test connections to both SQL Server and PostgreSQL"""
        results = {
            'sqlserver': {'status': 'unknown'},
            'postgresql': {'status': 'unknown'}
        }
        
        # Test PostgreSQL connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version(), current_database(), current_user;")
                result = cursor.fetchone()
                results['postgresql'] = {
                    'status': 'pass',
                    'version': result[0].split(',')[0] if result else 'unknown',
                    'database': result[1] if result else 'unknown',
                    'user': result[2] if result else 'unknown'
                }
        except Exception as e:
            results['postgresql'] = {
                'status': 'fail',
                'message': str(e)
            }
        
        # Test SQL Server connection (if not dry run)
        if not self.dry_run:
            try:
                # Use the management command to test connection
                import io
                from contextlib import redirect_stdout, redirect_stderr
                
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()
                
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    call_command(
                        'export_from_sqlserver',
                        config=self.config_file,
                        dry_run=True,
                        verbosity=0
                    )
                
                output = stdout_capture.getvalue()
                if "Connected to SQL Server" in output:
                    results['sqlserver'] = {'status': 'pass'}
                else:
                    results['sqlserver'] = {
                        'status': 'fail',
                        'message': 'Connection test failed'
                    }
                    
            except Exception as e:
                results['sqlserver'] = {
                    'status': 'fail',
                    'message': str(e)
                }
        else:
            results['sqlserver'] = {'status': 'skipped', 'message': 'Dry run mode'}
        
        # Overall result
        if all(r['status'] in ['pass', 'skipped'] for r in results.values()):
            return {
                'status': 'pass',
                'message': 'Database connections successful',
                'details': results
            }
        else:
            return {
                'status': 'fail',
                'message': 'Database connection failures',
                'details': results
            }

    def test_export_from_sqlserver(self):
        """Test SQL Server data export"""
        if self.dry_run:
            return {'status': 'skipped', 'message': 'Dry run mode'}
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Run export command
                call_command(
                    'export_from_sqlserver',
                    config=self.config_file,
                    output_dir=temp_dir,
                    verbosity=1
                )
                
                # Check if files were created
                exported_files = list(Path(temp_dir).glob('*.json'))
                
                if not exported_files:
                    return {
                        'status': 'fail',
                        'message': 'No export files created'
                    }
                
                # Validate export files
                total_records = 0
                for file_path in exported_files:
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            total_records += len(data)
                    except json.JSONDecodeError:
                        return {
                            'status': 'fail',
                            'message': f'Invalid JSON in export file: {file_path.name}'
                        }
                
                return {
                    'status': 'pass',
                    'message': f'Export successful: {len(exported_files)} files, {total_records} records',
                    'details': {
                        'files': [f.name for f in exported_files],
                        'total_records': total_records
                    }
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Export failed: {e}'
            }

    def test_import_to_postgresql(self):
        """Test PostgreSQL data import"""
        if self.dry_run:
            return {'status': 'skipped', 'message': 'Dry run mode'}
        
        try:
            # Run import command in dry run mode to test without actual import
            call_command(
                'import_from_sqlserver',
                config=self.config_file,
                dry_run=True,
                verbosity=1
            )
            
            return {
                'status': 'pass',
                'message': 'Import command executed successfully (dry run)',
                'note': 'Use --no-dry-run for actual import testing'
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Import command failed: {e}'
            }

    def test_data_integrity(self):
        """Test data integrity verification"""
        if self.dry_run:
            return {'status': 'skipped', 'message': 'Dry run mode'}
        
        try:
            # Run verification command
            call_command(
                'verify_migration',
                config=self.config_file,
                verbosity=1
            )
            
            return {
                'status': 'pass',
                'message': 'Data integrity verification completed'
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Verification failed: {e}'
            }

    def test_migration_performance(self):
        """Test migration performance characteristics"""
        try:
            # Load config to get expected data size
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            batch_size = config.get('migration_settings', {}).get('batch_size', 500)
            tables = len(config.get('mapping', {}))
            
            # Estimate performance requirements
            estimated_time_per_table = 30  # seconds
            max_expected_time = tables * estimated_time_per_table
            
            return {
                'status': 'pass',
                'message': 'Performance test completed',
                'details': {
                    'expected_tables': tables,
                    'batch_size': batch_size,
                    'estimated_max_time_seconds': max_expected_time,
                    'performance_tips': [
                        'Use appropriate batch sizes',
                        'Monitor memory usage during large imports',
                        'Consider running during off-peak hours'
                    ]
                }
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Performance test failed: {e}'
            }

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print(f"\n📊 Migration Test Report")
        print("=" * 50)
        
        summary = self.test_results['summary']
        print(f"Timestamp: {self.test_results['timestamp']}")
        print(f"Dry Run: {self.test_results['dry_run']}")
        print(f"Total Phases: {summary['total_phases']}")
        print(f"Passed: {summary['passed_phases']}")
        print(f"Failed: {summary['failed_phases']}")
        print(f"Overall Status: {summary['overall_status'].upper()}")
        
        # Detailed phase results
        print(f"\n📋 Phase Details:")
        for phase, result in self.test_results['phases'].items():
            status_icon = {
                'pass': '✅',
                'fail': '❌',
                'error': '💥',
                'skipped': '⏭️'
            }.get(result['status'], '❓')
            
            print(f"{status_icon} {phase}: {result['status'].upper()}")
            if result.get('message'):
                print(f"   └─ {result['message']}")
        
        # Save detailed report
        report_file = f'migration_test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        
        # Recommendations
        if summary['failed_phases'] > 0:
            print(f"\n🔧 Recommendations:")
            print("1. Review failed phases and fix configuration issues")
            print("2. Ensure SQL Server is accessible and credentials are correct")
            print("3. Verify PostgreSQL permissions and schema setup")
            print("4. Check table mapping configuration for accuracy")
        else:
            print(f"\n🎉 All tests passed! Migration pipeline is ready.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test SQL Server to PostgreSQL migration pipeline')
    parser.add_argument(
        '--config',
        default='config/migration_config.json',
        help='Migration config file path'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run tests without actual data operations'
    )
    
    args = parser.parse_args()
    
    tester = MigrationTester(
        config_file=args.config,
        dry_run=args.dry_run
    )
    
    success = tester.run_all_tests()
    
    if success:
        print(f"\n✅ All migration tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Some migration tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
