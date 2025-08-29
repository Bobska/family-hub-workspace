#!/bin/bash
# PostgreSQL Database Backup Script for FamilyHub
# Author: FamilyHub Team
# Date: August 29, 2025

set -e

# Configuration
CONTAINER_NAME="familyhub-postgres"
DATABASE_NAME="familyhub"
DATABASE_USER="django_user"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="familyhub_backup_${TIMESTAMP}.sql"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 FamilyHub Database Backup Script${NC}"
echo -e "${BLUE}====================================${NC}"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if Docker container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}❌ Error: PostgreSQL container '$CONTAINER_NAME' is not running${NC}"
    echo -e "${YELLOW}💡 Start the container with: docker-compose up -d db${NC}"
    exit 1
fi

echo -e "${YELLOW}📊 Creating database backup...${NC}"
echo -e "Container: $CONTAINER_NAME"
echo -e "Database: $DATABASE_NAME"
echo -e "Backup file: $BACKUP_DIR/$BACKUP_FILE"
echo ""

# Create database backup
if docker exec "$CONTAINER_NAME" pg_dump -U "$DATABASE_USER" -d "$DATABASE_NAME" --verbose --clean --no-acl --no-owner > "$BACKUP_DIR/$BACKUP_FILE"; then
    
    # Get file size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    
    echo ""
    echo -e "${GREEN}✅ Backup completed successfully!${NC}"
    echo -e "${GREEN}📁 File: $BACKUP_DIR/$BACKUP_FILE${NC}"
    echo -e "${GREEN}📏 Size: $BACKUP_SIZE${NC}"
    
    # Compress the backup
    echo -e "${YELLOW}🗜️  Compressing backup...${NC}"
    if gzip "$BACKUP_DIR/$BACKUP_FILE"; then
        COMPRESSED_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE.gz" | cut -f1)
        echo -e "${GREEN}✅ Backup compressed successfully!${NC}"
        echo -e "${GREEN}📁 Compressed file: $BACKUP_DIR/$BACKUP_FILE.gz${NC}"
        echo -e "${GREEN}📏 Compressed size: $COMPRESSED_SIZE${NC}"
    else
        echo -e "${YELLOW}⚠️  Compression failed, but backup is still available${NC}"
    fi
    
    # List recent backups
    echo ""
    echo -e "${BLUE}📋 Recent backups:${NC}"
    ls -lah "$BACKUP_DIR" | grep "familyhub_backup" | tail -5
    
    # Clean up old backups (keep last 10)
    echo ""
    echo -e "${YELLOW}🧹 Cleaning up old backups (keeping last 10)...${NC}"
    cd "$BACKUP_DIR"
    ls -t familyhub_backup_*.sql.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
    ls -t familyhub_backup_*.sql 2>/dev/null | tail -n +11 | xargs -r rm -f
    echo -e "${GREEN}✅ Cleanup completed${NC}"
    
else
    echo -e "${RED}❌ Backup failed!${NC}"
    echo -e "${YELLOW}💡 Check Docker container status and database connectivity${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Database backup process completed successfully!${NC}"
