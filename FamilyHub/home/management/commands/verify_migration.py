"""
Data integrity verification script for SQL Server to PostgreSQL migration.

This script compares data between SQL Server source and PostgreSQL target
to ensure migration integrity and identify any discrepancies.

Usage:
    python manage.py verify_migration --config config.json
    python manage.py verify_migration --server SERVER --database DB --username USER --password PASS
"""

import json
import pyodbc
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = 'Verify data integrity after SQL Server to PostgreSQL migration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--server',
            type=str,
            help='SQL Server host (e.g., localhost\\SQLEXPRESS)',
        )
        parser.add_argument(
            '--database',
            type=str,
            help='SQL Server database name',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='SQL Server username',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='SQL Server password',
        )
        parser.add_argument(
            '--config',
            type=str,
            help='Path to JSON config file with connection details and mapping',
        )
        parser.add_argument(
            '--mapping',
            type=str,
            help='Path to JSON file with table-to-model mapping',
        )
        parser.add_argument(
            '--tables',
            type=str,
            nargs='*',
            help='Specific tables to verify (default: all mapped tables)',
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed comparison of mismatched records',
        )
        parser.add_argument(
            '--sample-size',
            type=int,
            default=100,
            help='Number of records to sample for detailed verification (default: 100)',
        )
        parser.add_argument(
            '--output',
            type=str,
            help='File to save verification report (JSON format)',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('🔍 Data Migration Verification Tool')
        )
        self.stdout.write('=' * 50)

        # Initialize verification results
        self.verification_results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tables': 0,
                'passed_tables': 0,
                'failed_tables': 0,
                'total_records_source': 0,
                'total_records_target': 0,
                'data_integrity_score': 0.0,
            },
            'table_results': {},
            'issues': [],
        }

        # Get connection parameters and mapping
        conn_params = self.get_connection_params(options)
        table_mapping = self.load_table_mapping(options)
        
        # Connect to SQL Server
        try:
            sqlserver_conn = self.connect_to_sqlserver(conn_params)
            self.stdout.write(
                self.style.SUCCESS(f"✅ Connected to SQL Server: {conn_params['server']}")
            )
        except Exception as e:
            raise CommandError(f"❌ Failed to connect to SQL Server: {e}")

        # Test PostgreSQL connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                if result:
                    pg_version = result[0]
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Connected to PostgreSQL: {pg_version.split(',')[0]}")
                    )
        except Exception as e:
            raise CommandError(f"❌ Failed to connect to PostgreSQL: {e}")

        # Get tables to verify
        tables_to_verify = self.get_tables_to_verify(
            sqlserver_conn, table_mapping, options
        )
        
        self.verification_results['summary']['total_tables'] = len(tables_to_verify)

        # Verify each table
        for table_name in tables_to_verify:
            try:
                model_path = table_mapping[table_name]['model']
                field_mapping = table_mapping[table_name].get('fields', {})
                
                table_result = self.verify_table(
                    sqlserver_conn,
                    table_name,
                    model_path,
                    field_mapping,
                    options
                )
                
                self.verification_results['table_results'][table_name] = table_result
                
                if table_result['passed']:
                    self.verification_results['summary']['passed_tables'] += 1
                    status = self.style.SUCCESS("✅ PASS")
                else:
                    self.verification_results['summary']['failed_tables'] += 1
                    status = self.style.ERROR("❌ FAIL")
                
                self.stdout.write(
                    f"{status} {table_name} → {model_path}: "
                    f"Source: {table_result['source_count']}, "
                    f"Target: {table_result['target_count']}"
                )
                
            except Exception as e:
                self.verification_results['issues'].append({
                    'table': table_name,
                    'type': 'verification_error',
                    'message': str(e),
                })
                self.stdout.write(
                    self.style.ERROR(f"❌ ERROR {table_name}: {e}")
                )

        # Calculate data integrity score
        self.calculate_integrity_score()
        
        # Show summary
        self.show_verification_summary()
        
        # Save report if requested
        if options['output']:
            self.save_verification_report(options['output'])
        
        # Close connection
        sqlserver_conn.close()
        
        # Exit with appropriate code
        if self.verification_results['summary']['failed_tables'] > 0:
            self.stdout.write(
                self.style.ERROR("\n❌ Migration verification FAILED")
            )
            exit(1)
        else:
            self.stdout.write(
                self.style.SUCCESS("\n✅ Migration verification PASSED")
            )

    def get_connection_params(self, options):
        """Get SQL Server connection parameters"""
        if options['config']:
            try:
                with open(options['config'], 'r') as f:
                    config = json.load(f)
                return config.get('sqlserver', config)
            except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
                raise CommandError(f"Invalid config file: {e}")
        
        if not all([options['server'], options['database']]):
            raise CommandError(
                "Either provide --config or --server and --database arguments"
            )
        
        return {
            'server': options['server'],
            'database': options['database'],
            'username': options['username'],
            'password': options['password'],
            'trusted_connection': not bool(options['username']),
        }

    def connect_to_sqlserver(self, params):
        """Create connection to SQL Server"""
        if params.get('trusted_connection', False):
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={params['server']};"
                f"DATABASE={params['database']};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={params['server']};"
                f"DATABASE={params['database']};"
                f"UID={params['username']};"
                f"PWD={params['password']};"
            )
        
        return pyodbc.connect(conn_str)

    def load_table_mapping(self, options):
        """Load table-to-model mapping configuration"""
        if options['config']:
            try:
                with open(options['config'], 'r') as f:
                    config = json.load(f)
                    return config.get('mapping', config.get('table_mapping', {}))
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise CommandError(f"Invalid config file: {e}")
        
        if options['mapping']:
            try:
                with open(options['mapping'], 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise CommandError(f"Invalid mapping file: {e}")
        
        # Default mapping for timesheet app
        return {
            'Jobs': {
                'model': 'timesheet.Job',
                'fields': {
                    'JobId': 'id',
                    'JobName': 'name',
                    'JobDescription': 'description',
                    'HourlyRate': 'hourly_rate',
                    'IsActive': 'is_active',
                    'CreatedDate': 'created_at',
                    'UpdatedDate': 'updated_at',
                }
            },
            'TimeEntries': {
                'model': 'timesheet.TimeEntry',
                'fields': {
                    'EntryId': 'id',
                    'JobId': 'job_id',
                    'UserId': 'user_id',
                    'EntryDate': 'date',
                    'StartTime': 'start_time',
                    'EndTime': 'end_time',
                    'BreakMinutes': 'break_duration',
                    'Notes': 'notes',
                    'CreatedDate': 'created_at',
                    'UpdatedDate': 'updated_at',
                }
            },
            'Users': {
                'model': 'auth.User',
                'fields': {
                    'UserId': 'id',
                    'Username': 'username',
                    'Email': 'email',
                    'FirstName': 'first_name',
                    'LastName': 'last_name',
                    'IsActive': 'is_active',
                    'CreatedDate': 'date_joined',
                }
            }
        }

    def get_tables_to_verify(self, sqlserver_conn, table_mapping, options):
        """Get list of tables to verify"""
        available_tables = list(table_mapping.keys())
        
        if options['tables']:
            tables = [t for t in options['tables'] if t in available_tables]
            missing = set(options['tables']) - set(tables)
            if missing:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Tables not in mapping: {', '.join(missing)}")
                )
        else:
            tables = available_tables
        
        return tables

    def verify_table(self, sqlserver_conn, table_name, model_path, field_mapping, options):
        """Verify a single table migration"""
        result = {
            'table_name': table_name,
            'model_path': model_path,
            'source_count': 0,
            'target_count': 0,
            'count_match': False,
            'sample_verification': {},
            'issues': [],
            'passed': False,
        }

        try:
            # Get Django model
            app_label, model_name = model_path.split('.')
            model_class = apps.get_model(app_label, model_name)
            
            # Count records in source (SQL Server)
            cursor = sqlserver_conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            source_count = cursor.fetchone()[0]
            result['source_count'] = source_count
            
            # Count records in target (PostgreSQL)
            target_count = model_class.objects.count()
            result['target_count'] = target_count
            
            # Check if counts match
            result['count_match'] = source_count == target_count
            
            if not result['count_match']:
                result['issues'].append({
                    'type': 'count_mismatch',
                    'message': f"Record count mismatch: Source {source_count}, Target {target_count}",
                })

            # Sample verification for detailed checking
            if options['detailed'] and source_count > 0:
                sample_result = self.verify_sample_records(
                    cursor, table_name, model_class, field_mapping, options['sample_size']
                )
                result['sample_verification'] = sample_result

            # Overall pass/fail
            result['passed'] = result['count_match'] and len(result['issues']) == 0
            
            # Update summary counters
            self.verification_results['summary']['total_records_source'] += source_count
            self.verification_results['summary']['total_records_target'] += target_count
            
            cursor.close()
            
        except Exception as e:
            result['issues'].append({
                'type': 'verification_error',
                'message': str(e),
            })
            result['passed'] = False

        return result

    def verify_sample_records(self, cursor, table_name, model_class, field_mapping, sample_size):
        """Verify a sample of records for detailed comparison"""
        sample_result = {
            'sample_size': 0,
            'matched_records': 0,
            'mismatched_records': 0,
            'missing_records': 0,
            'sample_accuracy': 0.0,
            'mismatches': [],
        }

        try:
            # Get sample records from SQL Server
            cursor.execute(f"""
                SELECT TOP {sample_size} * FROM [{table_name}]
                ORDER BY NEWID()
            """)
            
            columns = [column[0] for column in cursor.description]
            sample_records = cursor.fetchall()
            sample_result['sample_size'] = len(sample_records)
            
            for row in sample_records:
                try:
                    # Build filter for Django query
                    filter_kwargs = {}
                    record_data = {}
                    
                    for i, column_name in enumerate(columns):
                        if column_name in field_mapping:
                            django_field = field_mapping[column_name]
                            value = row[i]
                            record_data[column_name] = value
                            
                            # Use first mapped field as primary key for lookup
                            if not filter_kwargs and value is not None:
                                filter_kwargs[django_field] = value
                    
                    # Try to find corresponding record in PostgreSQL
                    if filter_kwargs:
                        try:
                            django_record = model_class.objects.get(**filter_kwargs)
                            
                            # Compare field values
                            match = self.compare_record_fields(
                                record_data, django_record, field_mapping
                            )
                            
                            if match['is_match']:
                                sample_result['matched_records'] += 1
                            else:
                                sample_result['mismatched_records'] += 1
                                sample_result['mismatches'].append(match)
                                
                        except model_class.DoesNotExist:
                            sample_result['missing_records'] += 1
                            sample_result['mismatches'].append({
                                'type': 'missing_record',
                                'source_data': record_data,
                            })
                        except model_class.MultipleObjectsReturned:
                            sample_result['mismatched_records'] += 1
                            sample_result['mismatches'].append({
                                'type': 'multiple_matches',
                                'source_data': record_data,
                            })
                            
                except Exception as e:
                    sample_result['mismatched_records'] += 1
                    sample_result['mismatches'].append({
                        'type': 'comparison_error',
                        'error': str(e),
                        'source_data': dict(zip(columns, row)),
                    })

            # Calculate accuracy
            if sample_result['sample_size'] > 0:
                sample_result['sample_accuracy'] = (
                    sample_result['matched_records'] / sample_result['sample_size']
                ) * 100

        except Exception as e:
            sample_result['error'] = str(e)

        return sample_result

    def compare_record_fields(self, source_data, django_record, field_mapping):
        """Compare fields between source and target records"""
        comparison = {
            'is_match': True,
            'field_differences': [],
        }

        for source_field, django_field in field_mapping.items():
            if source_field in source_data:
                source_value = source_data[source_field]
                
                try:
                    django_value = getattr(django_record, django_field)
                    
                    # Compare values (with type conversion tolerance)
                    if not self.values_equivalent(source_value, django_value):
                        comparison['is_match'] = False
                        comparison['field_differences'].append({
                            'field': django_field,
                            'source_value': source_value,
                            'target_value': django_value,
                        })
                        
                except AttributeError:
                    comparison['is_match'] = False
                    comparison['field_differences'].append({
                        'field': django_field,
                        'error': 'Field not found in Django model',
                    })

        return comparison

    def values_equivalent(self, source_value, target_value):
        """Check if two values are equivalent, accounting for type differences"""
        # Handle None values
        if source_value is None and target_value is None:
            return True
        if source_value is None or target_value is None:
            return False

        # Convert to strings for comparison (handles type differences)
        try:
            source_str = str(source_value).strip()
            target_str = str(target_value).strip()
            
            # Special handling for dates and times
            if hasattr(source_value, 'isoformat') and hasattr(target_value, 'isoformat'):
                return source_value.isoformat() == target_value.isoformat()
            
            return source_str == target_str
            
        except Exception:
            return False

    def calculate_integrity_score(self):
        """Calculate overall data integrity score"""
        total_tables = self.verification_results['summary']['total_tables']
        passed_tables = self.verification_results['summary']['passed_tables']
        
        if total_tables > 0:
            self.verification_results['summary']['data_integrity_score'] = (
                passed_tables / total_tables
            ) * 100

    def show_verification_summary(self):
        """Show verification summary"""
        summary = self.verification_results['summary']
        
        self.stdout.write(f"\n📊 Verification Summary")
        self.stdout.write("=" * 30)
        self.stdout.write(f"Tables verified: {summary['total_tables']}")
        self.stdout.write(
            self.style.SUCCESS(f"Passed: {summary['passed_tables']}")
        )
        if summary['failed_tables'] > 0:
            self.stdout.write(
                self.style.ERROR(f"Failed: {summary['failed_tables']}")
            )
        self.stdout.write(f"Source records: {summary['total_records_source']:,}")
        self.stdout.write(f"Target records: {summary['total_records_target']:,}")
        self.stdout.write(
            f"Data integrity score: {summary['data_integrity_score']:.1f}%"
        )

        # Show issues if any
        if self.verification_results['issues']:
            self.stdout.write(f"\n⚠️  Issues found:")
            for issue in self.verification_results['issues']:
                self.stdout.write(f"  - {issue['table']}: {issue['message']}")

    def save_verification_report(self, output_file):
        """Save verification report to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.verification_results, f, indent=2, default=str)
            
            self.stdout.write(
                self.style.SUCCESS(f"📄 Verification report saved: {output_file}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to save report: {e}")
            )
