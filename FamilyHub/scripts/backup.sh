#!/bin/bash
# Database backup script for FamilyHub

# Set backup directory
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="familyhub_backup_${DATE}.sql"

# Database connection details
DB_HOST="postgres"
DB_NAME="familyhub"
DB_USER="familyhub_user"

# Create backup
echo "Creating backup: ${BACKUP_FILE}"
pg_dump -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} > ${BACKUP_DIR}/${BACKUP_FILE}

if [ $? -eq 0 ]; then
    echo "Backup created successfully: ${BACKUP_FILE}"
    
    # Compress the backup
    gzip ${BACKUP_DIR}/${BACKUP_FILE}
    echo "Backup compressed: ${BACKUP_FILE}.gz"
    
    # Keep only last 7 days of backups
    find ${BACKUP_DIR} -name "familyhub_backup_*.sql.gz" -mtime +7 -delete
    echo "Old backups cleaned up"
else
    echo "Backup failed!"
    exit 1
fi
