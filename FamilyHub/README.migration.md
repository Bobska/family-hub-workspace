# SQL Server to PostgreSQL Migration Documentation

## 🗄️ Database Migration System

This directory contains a comprehensive SQL Server to PostgreSQL migration system with data type conversion, integrity verification, and error handling.

### 🏗️ Migration Architecture

```
SQL Server Database
        ↓
    Export Tool
        ↓
   JSON Fixtures
        ↓
    Import Tool
        ↓
PostgreSQL Database
        ↓
  Verification Tool
        ↓
Migration Report
```

### 📦 Migration Components

#### 1. **Export Command** (`export_from_sqlserver`)
- **Purpose**: Export SQL Server data to Django JSON fixtures
- **Features**: Batch processing, type conversion, schema analysis
- **Output**: JSON fixture files compatible with Django

#### 2. **Import Command** (`import_from_sqlserver`)
- **Purpose**: Direct SQL Server to PostgreSQL data migration
- **Features**: Bulk operations, error handling, transaction safety
- **Performance**: Configurable batch sizes, parallel processing

#### 3. **Verification Command** (`verify_migration`)
- **Purpose**: Validate migration integrity and accuracy
- **Features**: Record count verification, sample data comparison
- **Output**: Detailed verification reports with data integrity scores

### 🔧 Configuration System

#### Migration Config File (`config/migration_config.json`)
```json
{
  "sqlserver": {
    "server": "localhost\\SQLEXPRESS",
    "database": "FamilyHubTimesheet",
    "username": "sa",
    "password": "your-password"
  },
  "mapping": {
    "SourceTable": {
      "model": "app.Model",
      "fields": {
        "SourceField": "target_field"
      },
      "transformations": {
        "field": {"type": "conversion_type"}
      }
    }
  }
}
```

#### Supported Data Type Conversions
- **String Types**: VARCHAR, NVARCHAR, CHAR, TEXT → CharField, TextField
- **Numeric Types**: INT, BIGINT, DECIMAL, FLOAT → IntegerField, DecimalField
- **Date/Time**: DATETIME, DATE, TIME → DateTimeField, DateField, TimeField
- **Boolean**: BIT → BooleanField
- **Binary**: VARBINARY, IMAGE → BinaryField (hex encoded)
- **UUID**: UNIQUEIDENTIFIER → UUIDField

### 🚀 Usage Examples

#### Basic Export
```bash
# Export all tables
python manage.py export_from_sqlserver \
    --server "localhost\SQLEXPRESS" \
    --database "FamilyHubTimesheet" \
    --username "sa" \
    --password "password"

# Export with config file
python manage.py export_from_sqlserver \
    --config config/migration_config.json
```

#### Direct Import
```bash
# Import with mapping
python manage.py import_from_sqlserver \
    --config config/migration_config.json \
    --app timesheet

# Import specific tables
python manage.py import_from_sqlserver \
    --config config/migration_config.json \
    --tables Jobs TimeEntries Users
```

#### Verify Migration
```bash
# Basic verification
python manage.py verify_migration \
    --config config/migration_config.json

# Detailed verification with sample checking
python manage.py verify_migration \
    --config config/migration_config.json \
    --detailed \
    --sample-size 500
```

### 📊 Migration Pipeline Testing

#### Comprehensive Test Script
```bash
# Test complete pipeline
python test_migration_pipeline.py \
    --config config/migration_config.json

# Dry run testing
python test_migration_pipeline.py \
    --config config/migration_config.json \
    --dry-run
```

#### Test Phases
1. **Config Validation** - Verify configuration file structure
2. **Connection Tests** - Test SQL Server and PostgreSQL connections
3. **Export Test** - Validate SQL Server data export
4. **Import Test** - Test PostgreSQL data import
5. **Integrity Verification** - Verify data migration accuracy
6. **Performance Test** - Assess migration performance characteristics

### 🔒 Security & Best Practices

#### Connection Security
- **Windows Authentication**: Use `trusted_connection: true` for SQL Server
- **Encrypted Connections**: Configure SSL/TLS for database connections
- **Credential Management**: Store passwords in environment variables
- **Limited Permissions**: Use read-only accounts for SQL Server export

#### Data Integrity
- **Transaction Safety**: All imports use database transactions
- **Batch Processing**: Configurable batch sizes to manage memory
- **Error Handling**: Skip individual records vs. fail entire migration
- **Backup Strategy**: Automatic backup before destructive operations

#### Performance Optimization
- **Batch Sizes**: Default 500 records per batch (configurable)
- **Memory Management**: Process large tables in chunks
- **Index Strategy**: Rebuild indexes after bulk imports
- **Parallel Processing**: Multiple table imports can run concurrently

### 🗃️ Data Mapping Examples

#### Timesheet Application Mapping
```json
{
  "Jobs": {
    "model": "timesheet.Job",
    "fields": {
      "JobId": "id",
      "JobName": "name",
      "JobDescription": "description",
      "HourlyRate": "hourly_rate",
      "IsActive": "is_active"
    },
    "transformations": {
      "HourlyRate": {"type": "decimal_to_float"},
      "IsActive": {"type": "bit_to_boolean"}
    }
  },
  "TimeEntries": {
    "model": "timesheet.TimeEntry",
    "fields": {
      "EntryId": "id",
      "JobId": "job_id",
      "EntryDate": "date",
      "StartTime": "start_time",
      "EndTime": "end_time",
      "BreakMinutes": "break_duration"
    },
    "dependencies": ["Jobs", "Users"]
  }
}
```

### 📈 Migration Monitoring

#### Progress Tracking
- **Real-time Progress**: Live progress indicators during migration
- **Record Counters**: Track imported vs. total records
- **Error Reporting**: Detailed error logs with failed record information
- **Performance Metrics**: Processing speed and estimated completion time

#### Verification Reports
```json
{
  "summary": {
    "total_tables": 4,
    "passed_tables": 4,
    "failed_tables": 0,
    "data_integrity_score": 100.0
  },
  "table_results": {
    "Jobs": {
      "source_count": 150,
      "target_count": 150,
      "count_match": true,
      "passed": true
    }
  }
}
```

### 🔧 Troubleshooting

#### Common Issues

1. **ODBC Driver Missing**
   ```bash
   # Install ODBC Driver 17 for SQL Server
   # Windows: Download from Microsoft
   # Linux: Use package manager
   ```

2. **Connection Timeout**
   ```json
   {
     "sqlserver": {
       "connection_timeout": 60,
       "command_timeout": 300
     }
   }
   ```

3. **Memory Issues with Large Tables**
   ```json
   {
     "migration_settings": {
       "batch_size": 100,
       "memory_limit_mb": 1024
     }
   }
   ```

4. **Data Type Conversion Errors**
   ```json
   {
     "transformations": {
       "problematic_field": {
         "type": "custom_converter",
         "default_value": null,
         "error_action": "skip"
       }
     }
   }
   ```

### 🔄 Migration Workflow

#### Pre-Migration Checklist
- [ ] Backup source SQL Server database
- [ ] Backup target PostgreSQL database
- [ ] Test database connections
- [ ] Validate configuration file
- [ ] Run migration test pipeline
- [ ] Verify disk space for export files

#### Migration Steps
1. **Export Phase**: Extract data from SQL Server
2. **Validation Phase**: Verify exported data integrity
3. **Import Phase**: Load data into PostgreSQL
4. **Verification Phase**: Compare source and target data
5. **Post-Processing**: Update sequences, rebuild indexes
6. **Final Verification**: Run application tests

#### Post-Migration Tasks
```sql
-- Update PostgreSQL sequences
SELECT setval(pg_get_serial_sequence('timesheet_job', 'id'), MAX(id)) FROM timesheet_job;

-- Rebuild indexes
REINDEX DATABASE familyhub;

-- Analyze tables for query planner
ANALYZE;
```

### 📋 Dependencies

#### Required Packages
```bash
# SQL Server connectivity
pip install pyodbc==5.0.1

# Data processing
pip install pandas==2.1.4
pip install numpy==1.24.4

# Progress monitoring
pip install tqdm==4.66.1

# Configuration validation
pip install jsonschema==4.20.0
```

#### System Requirements
- **Python**: 3.10+
- **ODBC Driver**: Microsoft ODBC Driver 17 for SQL Server
- **Memory**: 4GB+ recommended for large datasets
- **Storage**: 2x source database size for temporary files

---

## 📞 Support

For migration issues:

1. **Test Pipeline**: Run `python test_migration_pipeline.py --dry-run`
2. **Check Logs**: Review Django logs and migration command output
3. **Verify Config**: Validate configuration file with schema
4. **Connection Test**: Ensure both databases are accessible

**Migration System Version**: 1.0  
**Last Updated**: August 29, 2025  
**Supported SQL Server**: 2012+  
**Supported PostgreSQL**: 12+
