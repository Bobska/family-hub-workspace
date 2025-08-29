"""
Django management command to export SQL Server data to JSON fixtures.

This command connects to SQL Server and exports data in Django fixture format
for easy import into PostgreSQL.

Usage:
    python manage.py export_from_sqlserver --server SERVER --database DB --username USER --password PASS
    python manage.py export_from_sqlserver --config config.json
"""

import json
import os
import pyodbc
from datetime import datetime, date, time
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = 'Export data from SQL Server to Django JSON fixtures'

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
            '--output-dir',
            type=str,
            default='./fixtures/sqlserver_export',
            help='Directory to save fixture files (default: ./fixtures/sqlserver_export)',
        )
        parser.add_argument(
            '--tables',
            type=str,
            nargs='*',
            help='Specific tables to export (default: all tables)',
        )
        parser.add_argument(
            '--exclude-tables',
            type=str,
            nargs='*',
            default=['sysdiagrams', 'dtproperties'],
            help='Tables to exclude from export',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Number of records to process at once (default: 1000)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be exported without actually exporting',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('🗄️  SQL Server Data Export Tool')
        )
        self.stdout.write('=' * 50)

        # Get connection parameters
        conn_params = self.get_connection_params(options)
        
        # Test connection
        try:
            conn = self.connect_to_sqlserver(conn_params)
            self.stdout.write(
                self.style.SUCCESS(f"✅ Connected to SQL Server: {conn_params['server']}")
            )
        except Exception as e:
            raise CommandError(f"❌ Failed to connect to SQL Server: {e}")

        # Get tables to export
        tables = self.get_tables_to_export(conn, options)
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING("🔍 DRY RUN - No files will be created"))
            self.stdout.write(f"Tables to export: {', '.join(tables)}")
            return

        # Create output directory
        output_dir = options['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        
        # Export each table
        total_records = 0
        exported_files = []
        
        for table in tables:
            try:
                records_count = self.export_table(
                    conn, table, output_dir, options['batch_size']
                )
                total_records += records_count
                exported_files.append(f"{table}.json")
                
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Exported {table}: {records_count} records")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to export {table}: {e}")
                )

        # Create summary file
        self.create_export_summary(output_dir, exported_files, total_records)
        
        conn.close()
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Export completed!")
        )
        self.stdout.write(f"📁 Output directory: {output_dir}")
        self.stdout.write(f"📊 Total records exported: {total_records}")
        self.stdout.write(f"📄 Files created: {len(exported_files)}")

    def get_connection_params(self, options):
        """Get SQL Server connection parameters from options or config file"""
        if options['config']:
            try:
                with open(options['config'], 'r') as f:
                    config = json.load(f)
                return {
                    'server': config['server'],
                    'database': config['database'],
                    'username': config.get('username'),
                    'password': config.get('password'),
                    'trusted_connection': config.get('trusted_connection', False),
                }
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
        if params['trusted_connection']:
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

    def get_tables_to_export(self, conn, options):
        """Get list of tables to export"""
        cursor = conn.cursor()
        
        # Get all user tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            AND TABLE_SCHEMA = 'dbo'
            ORDER BY TABLE_NAME
        """)
        
        all_tables = [row[0] for row in cursor.fetchall()]
        
        # Filter tables
        if options['tables']:
            tables = [t for t in options['tables'] if t in all_tables]
            missing = set(options['tables']) - set(tables)
            if missing:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Tables not found: {', '.join(missing)}")
                )
        else:
            tables = all_tables
        
        # Exclude specified tables
        exclude_tables = options.get('exclude_tables', [])
        tables = [t for t in tables if t not in exclude_tables]
        
        cursor.close()
        return tables

    def export_table(self, conn, table_name, output_dir, batch_size):
        """Export a single table to JSON fixture"""
        cursor = conn.cursor()
        
        # Get table schema
        schema = self.get_table_schema(conn, table_name)
        
        # Get total record count
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        total_count = cursor.fetchone()[0]
        
        if total_count == 0:
            # Create empty fixture file
            fixture_data = []
            output_file = os.path.join(output_dir, f"{table_name}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(fixture_data, f, indent=2, default=self.json_serializer)
            return 0
        
        # Export data in batches
        fixture_data = []
        offset = 0
        pk_value = 1
        
        while offset < total_count:
            cursor.execute(f"""
                SELECT * FROM [{table_name}]
                ORDER BY (SELECT NULL)
                OFFSET {offset} ROWS
                FETCH NEXT {batch_size} ROWS ONLY
            """)
            
            batch = cursor.fetchall()
            
            for row in batch:
                fields = {}
                for i, column in enumerate(schema):
                    value = row[i]
                    field_name = column['name']
                    
                    # Convert SQL Server types to Django-compatible values
                    converted_value = self.convert_sqlserver_value(
                        value, column['type']
                    )
                    fields[field_name] = converted_value
                
                fixture_data.append({
                    'model': f'legacy.{table_name.lower()}',
                    'pk': pk_value,
                    'fields': fields
                })
                pk_value += 1
            
            offset += len(batch)
            
            # Progress indicator
            progress = (offset / total_count) * 100
            self.stdout.write(
                f"  📊 {table_name}: {progress:.1f}% ({offset}/{total_count})",
                ending='\r'
            )
        
        # Save fixture file
        output_file = os.path.join(output_dir, f"{table_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixture_data, f, indent=2, default=self.json_serializer)
        
        cursor.close()
        return total_count

    def get_table_schema(self, conn, table_name):
        """Get table schema information"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """, table_name)
        
        schema = []
        for row in cursor.fetchall():
            schema.append({
                'name': row[0],
                'type': row[1],
                'nullable': row[2] == 'YES',
                'max_length': row[3],
                'precision': row[4],
                'scale': row[5],
                'default': row[6],
            })
        
        cursor.close()
        return schema

    def convert_sqlserver_value(self, value, sql_type):
        """Convert SQL Server value to Django-compatible format"""
        if value is None:
            return None
        
        # String types
        if sql_type in ['varchar', 'nvarchar', 'char', 'nchar', 'text', 'ntext']:
            return str(value).strip() if value else None
        
        # Numeric types
        elif sql_type in ['int', 'bigint', 'smallint', 'tinyint']:
            return int(value)
        
        elif sql_type in ['decimal', 'numeric', 'money', 'smallmoney']:
            return float(value) if isinstance(value, Decimal) else value
        
        elif sql_type in ['float', 'real']:
            return float(value)
        
        # Date/Time types
        elif sql_type in ['datetime', 'datetime2', 'smalldatetime']:
            if isinstance(value, datetime):
                return value.isoformat()
            return str(value)
        
        elif sql_type == 'date':
            if isinstance(value, date):
                return value.isoformat()
            return str(value)
        
        elif sql_type == 'time':
            if isinstance(value, time):
                return value.isoformat()
            return str(value)
        
        # Boolean type
        elif sql_type == 'bit':
            return bool(value)
        
        # Binary types
        elif sql_type in ['binary', 'varbinary', 'image']:
            if isinstance(value, bytes):
                return value.hex()
            return str(value)
        
        # UUID type
        elif sql_type == 'uniqueidentifier':
            return str(value)
        
        # Default: convert to string
        else:
            return str(value)

    def json_serializer(self, obj):
        """JSON serializer for non-standard types"""
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.hex()
        else:
            return str(obj)

    def create_export_summary(self, output_dir, exported_files, total_records):
        """Create export summary file"""
        summary = {
            'export_date': datetime.now().isoformat(),
            'total_files': len(exported_files),
            'total_records': total_records,
            'files': exported_files,
            'source': 'SQL Server',
            'format': 'Django JSON Fixtures',
        }
        
        summary_file = os.path.join(output_dir, 'export_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        self.stdout.write(f"📋 Export summary saved: {summary_file}")
