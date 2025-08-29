"""
Django management command to import data from SQL Server to PostgreSQL.

This command connects to SQL Server, reads data, and imports it directly
into PostgreSQL with proper data type conversion and error handling.

Usage:
    python manage.py import_from_sqlserver --server SERVER --database DB --username USER --password PASS
    python manage.py import_from_sqlserver --config config.json --app timesheet
"""

import json
import os
import pyodbc
import psycopg2
from datetime import datetime, date, time
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.apps import apps
from django.conf import settings
from django.db.models import Model


class Command(BaseCommand):
    help = 'Import data from SQL Server directly to PostgreSQL'

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
            help='Path to JSON config file with connection details',
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Django app to import data into (default: timesheet)',
            default='timesheet',
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
            help='Specific tables to import (default: all mapped tables)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=500,
            help='Number of records to process at once (default: 500)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )
        parser.add_argument(
            '--truncate',
            action='store_true',
            help='Truncate target tables before import',
        )
        parser.add_argument(
            '--skip-errors',
            action='store_true',
            help='Continue import even if some records fail',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('🔄 SQL Server to PostgreSQL Import Tool')
        )
        self.stdout.write('=' * 50)

        # Initialize counters
        self.imported_records = 0
        self.failed_records = 0
        self.skipped_tables = 0

        # Get connection parameters
        conn_params = self.get_connection_params(options)
        
        # Test SQL Server connection
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
                pg_version = cursor.fetchone()[0]
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Connected to PostgreSQL: {pg_version.split(',')[0]}")
                )
        except Exception as e:
            raise CommandError(f"❌ Failed to connect to PostgreSQL: {e}")

        # Load table mapping
        table_mapping = self.load_table_mapping(options)
        
        # Get tables to import
        tables_to_import = self.get_tables_to_import(
            sqlserver_conn, table_mapping, options
        )
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING("🔍 DRY RUN - No data will be imported"))
            self.show_import_plan(tables_to_import, table_mapping)
            return

        # Truncate tables if requested
        if options['truncate']:
            self.truncate_target_tables(tables_to_import, table_mapping)

        # Import each table
        for table_name in tables_to_import:
            try:
                model_name = table_mapping[table_name]['model']
                field_mapping = table_mapping[table_name].get('fields', {})
                
                imported_count = self.import_table(
                    sqlserver_conn,
                    table_name,
                    model_name,
                    field_mapping,
                    options
                )
                
                self.imported_records += imported_count
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Imported {table_name} → {model_name}: {imported_count} records")
                )
                
            except Exception as e:
                self.failed_records += 1
                self.skipped_tables += 1
                
                if options['skip_errors']:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Skipped {table_name}: {e}")
                    )
                else:
                    raise CommandError(f"❌ Failed to import {table_name}: {e}")

        # Close connections
        sqlserver_conn.close()
        
        # Summary
        self.show_import_summary()

    def get_connection_params(self, options):
        """Get SQL Server connection parameters"""
        if options['config']:
            try:
                with open(options['config'], 'r') as f:
                    config = json.load(f)
                return config.get('sqlserver', config)  # Support nested or flat config
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

    def get_tables_to_import(self, sqlserver_conn, table_mapping, options):
        """Get list of tables to import"""
        available_tables = list(table_mapping.keys())
        
        if options['tables']:
            # Filter to requested tables
            tables = [t for t in options['tables'] if t in available_tables]
            missing = set(options['tables']) - set(tables)
            if missing:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Tables not in mapping: {', '.join(missing)}")
                )
        else:
            tables = available_tables
        
        # Verify tables exist in SQL Server
        cursor = sqlserver_conn.cursor()
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            AND TABLE_SCHEMA = 'dbo'
        """)
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        tables = [t for t in tables if t in existing_tables]
        
        cursor.close()
        return tables

    def show_import_plan(self, tables, mapping):
        """Show what would be imported in dry run"""
        self.stdout.write("\n📋 Import Plan:")
        for table in tables:
            model = mapping[table]['model']
            field_count = len(mapping[table].get('fields', {}))
            self.stdout.write(f"  📊 {table} → {model} ({field_count} fields)")

    def truncate_target_tables(self, tables, mapping):
        """Truncate target tables before import"""
        self.stdout.write(self.style.WARNING("🗑️  Truncating target tables..."))
        
        with transaction.atomic():
            for table in tables:
                model_path = mapping[table]['model']
                try:
                    app_label, model_name = model_path.split('.')
                    model_class = apps.get_model(app_label, model_name)
                    
                    count = model_class.objects.count()
                    model_class.objects.all().delete()
                    
                    self.stdout.write(f"  🗑️  Truncated {model_path}: {count} records")
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Failed to truncate {model_path}: {e}")
                    )

    def import_table(self, sqlserver_conn, table_name, model_path, field_mapping, options):
        """Import a single table"""
        # Get Django model
        try:
            app_label, model_name = model_path.split('.')
            model_class = apps.get_model(app_label, model_name)
        except Exception as e:
            raise CommandError(f"Invalid model path {model_path}: {e}")

        # Get source data
        cursor = sqlserver_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        total_count = cursor.fetchone()[0]
        
        if total_count == 0:
            return 0

        # Get table schema
        schema = self.get_sqlserver_schema(sqlserver_conn, table_name)
        
        # Import data in batches
        imported_count = 0
        batch_size = options['batch_size']
        offset = 0

        while offset < total_count:
            cursor.execute(f"""
                SELECT * FROM [{table_name}]
                ORDER BY (SELECT NULL)
                OFFSET {offset} ROWS
                FETCH NEXT {batch_size} ROWS ONLY
            """)
            
            batch = cursor.fetchall()
            
            # Convert batch to Django objects
            django_objects = []
            for row in batch:
                try:
                    django_obj = self.convert_row_to_django_object(
                        row, schema, field_mapping, model_class
                    )
                    if django_obj:
                        django_objects.append(django_obj)
                except Exception as e:
                    if options['skip_errors']:
                        self.failed_records += 1
                        continue
                    else:
                        raise

            # Bulk create objects
            if django_objects:
                try:
                    with transaction.atomic():
                        model_class.objects.bulk_create(
                            django_objects, 
                            ignore_conflicts=True,
                            batch_size=batch_size
                        )
                        imported_count += len(django_objects)
                except Exception as e:
                    if options['skip_errors']:
                        self.failed_records += len(django_objects)
                    else:
                        raise

            offset += len(batch)
            
            # Progress indicator
            progress = (offset / total_count) * 100
            self.stdout.write(
                f"  📊 {table_name}: {progress:.1f}% ({offset}/{total_count})",
                ending='\r'
            )

        cursor.close()
        return imported_count

    def get_sqlserver_schema(self, conn, table_name):
        """Get SQL Server table schema"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE,
                COLUMN_DEFAULT,
                ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """, table_name)
        
        schema = {}
        for row in cursor.fetchall():
            schema[row[0]] = {
                'type': row[1],
                'nullable': row[2] == 'YES',
                'max_length': row[3],
                'precision': row[4],
                'scale': row[5],
                'default': row[6],
                'position': row[7],
            }
        
        cursor.close()
        return schema

    def convert_row_to_django_object(self, row, schema, field_mapping, model_class):
        """Convert SQL Server row to Django model instance"""
        # Get column names in order
        columns = sorted(schema.keys(), key=lambda x: schema[x]['position'])
        
        # Create field values dictionary
        django_fields = {}
        
        for i, column_name in enumerate(columns):
            if column_name in field_mapping:
                django_field = field_mapping[column_name]
                sql_value = row[i]
                sql_type = schema[column_name]['type']
                
                # Convert value
                converted_value = self.convert_sqlserver_to_django_value(
                    sql_value, sql_type, django_field, model_class
                )
                
                django_fields[django_field] = converted_value

        # Create Django object
        try:
            return model_class(**django_fields)
        except Exception as e:
            if hasattr(model_class, '_meta'):
                model_name = f"{model_class._meta.app_label}.{model_class._meta.model_name}"
            else:
                model_name = str(model_class)
            raise Exception(f"Failed to create {model_name} object: {e}")

    def convert_sqlserver_to_django_value(self, value, sql_type, django_field, model_class):
        """Convert SQL Server value to Django field value"""
        if value is None:
            return None

        # Get Django field info
        try:
            field = model_class._meta.get_field(django_field)
            field_type = type(field).__name__
        except:
            field_type = 'CharField'  # Default

        # Type conversions based on Django field type
        if field_type in ['CharField', 'TextField', 'SlugField']:
            return str(value).strip() if value else ''
        
        elif field_type in ['IntegerField', 'BigIntegerField', 'SmallIntegerField', 'PositiveIntegerField']:
            return int(value) if value is not None else 0
        
        elif field_type in ['DecimalField', 'FloatField']:
            return float(value) if value is not None else 0.0
        
        elif field_type == 'BooleanField':
            if sql_type == 'bit':
                return bool(value)
            return bool(value) if value is not None else False
        
        elif field_type in ['DateTimeField']:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, str):
                try:
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                except:
                    return None
            return value
        
        elif field_type == 'DateField':
            if isinstance(value, date):
                return value
            elif isinstance(value, datetime):
                return value.date()
            elif isinstance(value, str):
                try:
                    return datetime.fromisoformat(value).date()
                except:
                    return None
            return value
        
        elif field_type == 'TimeField':
            if isinstance(value, time):
                return value
            elif isinstance(value, datetime):
                return value.time()
            elif isinstance(value, str):
                try:
                    return datetime.fromisoformat(value).time()
                except:
                    return None
            return value
        
        elif field_type == 'UUIDField':
            return str(value)
        
        elif field_type in ['ForeignKey', 'OneToOneField']:
            return int(value) if value is not None else None
        
        else:
            return str(value) if value is not None else ''

    def show_import_summary(self):
        """Show import summary"""
        self.stdout.write(f"\n🎉 Import completed!")
        self.stdout.write(f"📊 Total records imported: {self.imported_records}")
        if self.failed_records > 0:
            self.stdout.write(
                self.style.WARNING(f"⚠️  Failed records: {self.failed_records}")
            )
        if self.skipped_tables > 0:
            self.stdout.write(
                self.style.WARNING(f"⚠️  Skipped tables: {self.skipped_tables}")
            )
