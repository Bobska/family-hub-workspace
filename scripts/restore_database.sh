#!/bin/bash
# PostgreSQL Database Restore Script for FamilyHub
# Author: FamilyHub Team
# Date: August 29, 2025

set -e

# Configuration
CONTAINER_NAME="familyhub-postgres"
DATABASE_NAME="familyhub"
DATABASE_USER="django_user"
BACKUP_DIR="./backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 FamilyHub Database Restore Script${NC}"
echo -e "${BLUE}====================================${NC}"
echo ""

# Check if backup file is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}📋 Available backup files:${NC}"
    if [ -d "$BACKUP_DIR" ]; then
        ls -lah "$BACKUP_DIR" | grep "familyhub_backup" | head -10
    else
        echo -e "${RED}❌ No backup directory found${NC}"
    fi
    echo ""
    echo -e "${YELLOW}Usage: $0 <backup_file>${NC}"
    echo -e "${YELLOW}Example: $0 familyhub_backup_20250829_143000.sql.gz${NC}"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ] && [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}❌ Error: Backup file not found${NC}"
    echo -e "Checked paths:"
    echo -e "  - $BACKUP_DIR/$BACKUP_FILE"
    echo -e "  - $BACKUP_FILE"
    exit 1
fi

# Determine full path to backup file
if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"
else
    FULL_BACKUP_PATH="$BACKUP_FILE"
fi

# Check if Docker container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}❌ Error: PostgreSQL container '$CONTAINER_NAME' is not running${NC}"
    echo -e "${YELLOW}💡 Start the container with: docker-compose up -d db${NC}"
    exit 1
fi

echo -e "${YELLOW}📊 Database restore information:${NC}"
echo -e "Container: $CONTAINER_NAME"
echo -e "Database: $DATABASE_NAME"
echo -e "Backup file: $FULL_BACKUP_PATH"
echo ""

# Warning about data loss
echo -e "${RED}⚠️  WARNING: This will REPLACE all existing data in the database!${NC}"
echo -e "${YELLOW}📋 Current database content will be lost.${NC}"
echo ""
read -p "Are you sure you want to continue? (yes/NO): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${YELLOW}❌ Restore cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}🔄 Starting database restore...${NC}"

# Handle compressed files
TEMP_FILE=""
if [[ "$FULL_BACKUP_PATH" == *.gz ]]; then
    echo -e "${YELLOW}📦 Decompressing backup file...${NC}"
    TEMP_FILE="/tmp/familyhub_restore_temp.sql"
    if gunzip -c "$FULL_BACKUP_PATH" > "$TEMP_FILE"; then
        echo -e "${GREEN}✅ Backup decompressed successfully${NC}"
        SOURCE_FILE="$TEMP_FILE"
    else
        echo -e "${RED}❌ Failed to decompress backup file${NC}"
        exit 1
    fi
else
    SOURCE_FILE="$FULL_BACKUP_PATH"
fi

# Restore database
echo -e "${YELLOW}🔄 Restoring database...${NC}"
if docker exec -i "$CONTAINER_NAME" psql -U "$DATABASE_USER" -d "$DATABASE_NAME" < "$SOURCE_FILE"; then
    echo -e "${GREEN}✅ Database restore completed successfully!${NC}"
    
    # Clean up temporary file
    if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
        rm -f "$TEMP_FILE"
        echo -e "${GREEN}🧹 Temporary files cleaned up${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}📊 Database status:${NC}"
    docker exec "$CONTAINER_NAME" psql -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "\dt" || true
    
else
    echo -e "${RED}❌ Database restore failed!${NC}"
    
    # Clean up temporary file on error
    if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
        rm -f "$TEMP_FILE"
    fi
    
    echo -e "${YELLOW}💡 Check the backup file format and database connectivity${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Database restore process completed successfully!${NC}"
echo -e "${YELLOW}💡 You may need to restart your Django application${NC}"
