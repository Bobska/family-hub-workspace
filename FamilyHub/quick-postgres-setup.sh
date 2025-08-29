#!/bin/bash

# ⚡ FamilyHub Quick PostgreSQL Setup Script
# 🚀 Get PostgreSQL 17.6 + pgAdmin running in 5 minutes!

echo "⚡ FamilyHub Quick PostgreSQL Setup"
echo "=================================="

# Colors for output  
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"  
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"

# Check if services are already running
if docker ps | grep -q "familyhub_postgres_dev_quick"; then
    echo -e "${YELLOW}⚠️  PostgreSQL container already running${NC}"
    echo -e "${BLUE}Choose an option:${NC}"
    echo "1) Stop and restart"
    echo "2) Keep running and exit"
    echo "3) Stop and clean everything"
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            echo -e "${YELLOW}🔄 Restarting services...${NC}"
            docker-compose -f docker-compose.quick.yml --env-file .env.quick down
            ;;
        2)
            echo -e "${GREEN}✅ Services already running!${NC}"
            echo -e "${BLUE}🌐 pgAdmin: http://localhost:5050${NC}"
            echo -e "${BLUE}📊 PostgreSQL: localhost:5432${NC}"
            exit 0
            ;;
        3)
            echo -e "${RED}🗑️  Cleaning everything...${NC}"
            docker-compose -f docker-compose.quick.yml --env-file .env.quick down -v
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${NC}"
            exit 1
            ;;
    esac
fi

# Start services
echo -e "${BLUE}🚀 Starting PostgreSQL 17.6 + pgAdmin...${NC}"
docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Check service status
echo -e "${BLUE}🔍 Checking service status...${NC}"

# Check PostgreSQL
if docker-compose -f docker-compose.quick.yml --env-file .env.quick exec -T postgres-dev pg_isready -U django -d familyhub > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL 17.6: Running${NC}"
    postgres_status="OK"
else
    echo -e "${RED}❌ PostgreSQL 17.6: Not ready${NC}"
    postgres_status="FAIL"
fi

# Check pgAdmin
if curl -s http://localhost:5050 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ pgAdmin 4: Running${NC}"
    pgadmin_status="OK"
else
    echo -e "${RED}❌ pgAdmin 4: Not ready${NC}"
    pgadmin_status="FAIL"
fi

# Show results
echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "===================="

if [[ "$postgres_status" == "OK" && "$pgadmin_status" == "OK" ]]; then
    echo -e "${GREEN}✅ All services running successfully!${NC}"
    
    echo ""
    echo -e "${BLUE}🌐 Access Points:${NC}"
    echo -e "📊 pgAdmin Web: ${YELLOW}http://localhost:5050${NC}"
    echo -e "   └─ Email: ${YELLOW}admin@familyhub.local${NC}"
    echo -e "   └─ Password: ${YELLOW}admin123${NC}"
    echo ""
    echo -e "🐘 PostgreSQL Direct: ${YELLOW}localhost:5432${NC}"
    echo -e "   └─ Database: ${YELLOW}familyhub${NC}"
    echo -e "   └─ Username: ${YELLOW}django${NC}"
    echo -e "   └─ Password: ${YELLOW}secretpass${NC}"
    echo ""
    echo -e "🔗 Django Database URL:"
    echo -e "   ${YELLOW}postgresql://django:secretpass@localhost:5432/familyhub${NC}"
    
    echo ""
    echo -e "${BLUE}🛠️  Quick Commands:${NC}"
    echo -e "📊 View logs: ${YELLOW}docker-compose -f docker-compose.quick.yml logs -f${NC}"
    echo -e "🔄 Restart: ${YELLOW}docker-compose -f docker-compose.quick.yml restart${NC}"
    echo -e "🛑 Stop: ${YELLOW}docker-compose -f docker-compose.quick.yml down${NC}"
    echo -e "🗑️  Clean: ${YELLOW}docker-compose -f docker-compose.quick.yml down -v${NC}"
    
    echo ""
    echo -e "${BLUE}📖 Documentation: README.quick-postgres.md${NC}"
    
    exit 0
else
    echo -e "${RED}❌ Some services failed to start${NC}"
    echo ""
    echo -e "${BLUE}🔧 Troubleshooting:${NC}"
    echo -e "📊 View logs: ${YELLOW}docker-compose -f docker-compose.quick.yml logs${NC}"
    echo -e "🔄 Restart: ${YELLOW}docker-compose -f docker-compose.quick.yml restart${NC}"
    echo -e "🛑 Stop: ${YELLOW}docker-compose -f docker-compose.quick.yml down${NC}"
    
    exit 1
fi
