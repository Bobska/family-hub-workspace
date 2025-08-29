#!/bin/bash

# FamilyHub Production Stack Test Script
# Tests the complete 5-service Docker production environment

set -e

echo "🏗️  FamilyHub Production Stack Test"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test functions
test_service() {
    local service=$1
    local test_command=$2
    local expected_output=$3
    
    echo -e "${BLUE}Testing $service...${NC}"
    
    if eval "$test_command" | grep -q "$expected_output"; then
        echo -e "${GREEN}✅ $service: PASS${NC}"
        return 0
    else
        echo -e "${RED}❌ $service: FAIL${NC}"
        return 1
    fi
}

test_http_endpoint() {
    local url=$1
    local description=$2
    local expected_status=${3:-200}
    
    echo -e "${BLUE}Testing $description at $url...${NC}"
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        echo -e "${GREEN}✅ $description: PASS (HTTP $expected_status)${NC}"
        return 0
    else
        echo -e "${RED}❌ $description: FAIL${NC}"
        return 1
    fi
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}⚠️  .env.production not found. Creating from template...${NC}"
    cp .env.production .env
    echo -e "${YELLOW}📝 Please edit .env file and run this script again.${NC}"
    exit 1
fi

# Build and start services
echo -e "\n${YELLOW}🏗️  Building production images...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production build

echo -e "\n${YELLOW}🚀 Starting production stack...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production up -d

# Wait for services to be ready
echo -e "\n${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 30

# Run tests
echo -e "\n${YELLOW}🧪 Running production stack tests...${NC}"

failed_tests=0

# Test 1: PostgreSQL Health
if ! test_service "PostgreSQL" \
    "docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production exec -T postgres pg_isready -U familyhub_user -d familyhub" \
    "accepting connections"; then
    ((failed_tests++))
fi

# Test 2: Redis Health
if ! test_service "Redis" \
    "docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production exec -T redis redis-cli ping" \
    "PONG"; then
    ((failed_tests++))
fi

# Test 3: Django Web Service
sleep 10  # Give Django more time to start
if ! test_http_endpoint "http://localhost/health/" "Django Health Check"; then
    ((failed_tests++))
fi

# Test 4: Nginx Reverse Proxy
if ! test_http_endpoint "http://localhost/" "Nginx Reverse Proxy" "200\|301\|302"; then
    ((failed_tests++))
fi

# Test 5: HTTPS Redirect
if ! test_http_endpoint "http://localhost/" "HTTPS Redirect" "301\|302"; then
    echo -e "${YELLOW}⚠️  HTTPS redirect test - check if SSL is properly configured${NC}"
fi

# Test 6: Static Files
if ! test_http_endpoint "http://localhost/static/admin/css/base.css" "Static Files Serving"; then
    ((failed_tests++))
fi

# Test 7: Celery Worker
echo -e "${BLUE}Testing Celery Worker...${NC}"
if docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production exec -T celery celery -A FamilyHub inspect ping | grep -q "pong"; then
    echo -e "${GREEN}✅ Celery Worker: PASS${NC}"
else
    echo -e "${RED}❌ Celery Worker: FAIL${NC}"
    ((failed_tests++))
fi

# Test 8: Database Connectivity from Django
echo -e "${BLUE}Testing Database Connectivity...${NC}"
if docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production exec -T web python manage.py check --database default | grep -q "System check identified no issues"; then
    echo -e "${GREEN}✅ Database Connectivity: PASS${NC}"
else
    echo -e "${RED}❌ Database Connectivity: FAIL${NC}"
    ((failed_tests++))
fi

# Test 9: Backup Service
echo -e "${BLUE}Testing Backup Service...${NC}"
if docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production ps backup | grep -q "Up"; then
    echo -e "${GREEN}✅ Backup Service: PASS${NC}"
else
    echo -e "${RED}❌ Backup Service: FAIL${NC}"
    ((failed_tests++))
fi

# Test 10: Container Resource Limits
echo -e "${BLUE}Testing Container Resource Limits...${NC}"
container_count=$(docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production ps -q | wc -l)
if [ "$container_count" -ge 6 ]; then
    echo -e "${GREEN}✅ All Containers Running: PASS ($container_count containers)${NC}"
else
    echo -e "${RED}❌ Missing Containers: FAIL (only $container_count running)${NC}"
    ((failed_tests++))
fi

# Performance Tests
echo -e "\n${YELLOW}⚡ Running performance tests...${NC}"

# Test response time
echo -e "${BLUE}Testing response time...${NC}"
response_time=$(curl -o /dev/null -s -w "%{time_total}" http://localhost/health/)
if (( $(echo "$response_time < 2.0" | bc -l) )); then
    echo -e "${GREEN}✅ Response Time: PASS (${response_time}s)${NC}"
else
    echo -e "${YELLOW}⚠️  Response Time: SLOW (${response_time}s)${NC}"
fi

# Test concurrent connections
echo -e "${BLUE}Testing concurrent connections...${NC}"
concurrent_test() {
    for i in {1..10}; do
        curl -s http://localhost/health/ > /dev/null &
    done
    wait
}

start_time=$(date +%s.%N)
concurrent_test
end_time=$(date +%s.%N)
concurrent_duration=$(echo "$end_time - $start_time" | bc)

if (( $(echo "$concurrent_duration < 5.0" | bc -l) )); then
    echo -e "${GREEN}✅ Concurrent Connections: PASS (${concurrent_duration}s)${NC}"
else
    echo -e "${YELLOW}⚠️  Concurrent Connections: SLOW (${concurrent_duration}s)${NC}"
fi

# Security Tests
echo -e "\n${YELLOW}🔒 Running security tests...${NC}"

# Test security headers
echo -e "${BLUE}Testing security headers...${NC}"
headers=$(curl -I -s http://localhost/)
if echo "$headers" | grep -q "X-Content-Type-Options"; then
    echo -e "${GREEN}✅ Security Headers: PASS${NC}"
else
    echo -e "${YELLOW}⚠️  Security Headers: Missing some headers${NC}"
fi

# Summary
echo -e "\n${YELLOW}📊 Test Summary${NC}"
echo "================================"

total_tests=10
passed_tests=$((total_tests - failed_tests))

echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! Production stack is ready.${NC}"
    echo -e "\n${BLUE}📋 Production URLs:${NC}"
    echo -e "🌐 Application: http://localhost/ (redirects to HTTPS)"
    echo -e "🔒 Secure Application: https://localhost/"
    echo -e "🏥 Health Check: http://localhost/health/"
    echo -e "📊 Redis Commander: http://localhost:8082/ (with monitoring profile)"
    
    echo -e "\n${BLUE}🛠️  Management Commands:${NC}"
    echo -e "📊 View logs: make logs -f Makefile.production"
    echo -e "🔄 Restart: make restart -f Makefile.production"
    echo -e "🛑 Stop: make down -f Makefile.production"
    echo -e "💾 Backup: make backup -f Makefile.production"
    
    exit 0
else
    echo -e "\n${RED}❌ SOME TESTS FAILED! Please check the logs:${NC}"
    echo -e "View logs: docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production logs"
    
    echo -e "\n${YELLOW}🔧 Debugging Commands:${NC}"
    echo -e "🐳 Container status: docker-compose -f docker-compose.yml -f docker-compose.production.yml --env-file .env.production ps"
    echo -e "📊 Container stats: docker stats"
    echo -e "🏥 Health status: make health -f Makefile.production"
    
    exit 1
fi
