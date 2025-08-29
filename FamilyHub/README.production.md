# Production Docker Environment Documentation

## 🚀 FamilyHub Complete Production Stack

This directory contains a complete production-ready Docker environment for FamilyHub with 5 core services plus backup.

### 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│     Django      │────│   PostgreSQL    │
│  (Reverse Proxy │    │   (Gunicorn)    │    │   (Database)    │
│   Static Files) │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         │              │ (Cache/Broker)  │              │
         │              └─────────────────┘              │
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Celery      │              │
         │              │   (Workers)     │              │
         │              └─────────────────┘              │
         │                                               │
         │              ┌─────────────────┐              │
         └──────────────│     Backup      │──────────────┘
                        │   (pg-backup)   │
                        └─────────────────┘
```

### 📦 Services Configuration

#### 1. **Django Web Application** (`web`)
- **Image**: Custom Python 3.11 with Django
- **Server**: Gunicorn with gevent workers
- **Workers**: 3 processes, 1000 connections each
- **Health Check**: `/health/` endpoint
- **Restart Policy**: Always
- **Resources**: 1GB RAM limit, 1 CPU limit

#### 2. **PostgreSQL Database** (`postgres`)
- **Image**: PostgreSQL 17.6 Alpine
- **Configuration**: Production optimized
- **Memory**: 2GB shared_buffers, 3GB total limit
- **Connections**: 200 max connections
- **Health Check**: `pg_isready` command
- **Restart Policy**: Always

#### 3. **Redis Cache & Message Broker** (`redis`)
- **Image**: Redis 7 Alpine
- **Configuration**: AOF persistence, LRU eviction
- **Memory**: 1GB limit with allkeys-lru policy
- **Health Check**: Redis PING command
- **Restart Policy**: Always

#### 4. **Nginx Reverse Proxy** (`nginx`)
- **Image**: Custom Nginx with SSL
- **Features**: HTTPS redirect, security headers, rate limiting
- **SSL**: Self-signed certificates for local development
- **Static Files**: Optimized serving with caching
- **Health Check**: HTTP request to `/health/`
- **Restart Policy**: Always

#### 5. **Celery Worker** (`celery`)
- **Image**: Same as Django web
- **Workers**: 2 concurrent workers
- **Queues**: default, timesheet, backup, email
- **Health Check**: Celery inspect ping
- **Restart Policy**: Always

#### 6. **Celery Beat Scheduler** (`celery-beat`)
- **Image**: Same as Django web
- **Function**: Schedule periodic tasks
- **Database Scheduler**: Uses Django database for persistence
- **Tasks**: Session cleanup, reports, backups, health checks

#### 7. **Backup Service** (`backup`)
- **Image**: postgres-backup-s3:15
- **Schedule**: Daily at 2 AM
- **Retention**: 7 days, 4 weeks, 6 months
- **Local Storage**: `./backups/` directory
- **Health Check**: HTTP endpoint on port 8080

### 🔧 Production Configuration

#### Environment Variables (`.env.production`)
```bash
# Django
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=familyhub.local,localhost,your-domain.com

# Database
POSTGRES_DB=familyhub
POSTGRES_USER=familyhub_user
POSTGRES_PASSWORD=secure-password

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=secure-redis-password

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

#### Network Security
- **Internal Network**: `familyhub_internal` (isolated)
- **External Network**: `familyhub_external` (public access)
- **Database**: Only accessible from internal network
- **Redis**: Only accessible from internal network
- **Web Application**: Accessible through Nginx only

#### Health Monitoring
- **Web Health**: `http://localhost/health/`
- **Ready Check**: `http://localhost/ready/`
- **Alive Check**: `http://localhost/alive/`
- **Database Check**: `pg_isready` command
- **Redis Check**: `PING` command
- **Celery Check**: `inspect ping` command

### 🚀 Deployment Commands

#### Quick Start
```bash
# 1. Configure environment
cp .env.production .env
# Edit .env with your settings

# 2. Build and start
make build -f Makefile.production
make up -f Makefile.production

# 3. Check health
make health -f Makefile.production
```

#### Management Commands
```bash
# Service Management
make up -f Makefile.production          # Start all services
make down -f Makefile.production        # Stop all services
make restart -f Makefile.production     # Restart services
make logs -f Makefile.production        # View all logs

# Database Operations
make migrate -f Makefile.production     # Run migrations
make shell -f Makefile.production       # Django shell
make psql -f Makefile.production        # PostgreSQL shell

# Monitoring
make health -f Makefile.production      # Health check
make stats -f Makefile.production       # Resource usage
make ps -f Makefile.production          # Container status

# Backup & Restore
make backup -f Makefile.production      # Create backup
make backup-now -f Makefile.production # Immediate backup
make restore BACKUP_FILE=backup.sql -f Makefile.production
```

### 📊 Monitoring & Logging

#### Log Access
```bash
# All services
make logs -f Makefile.production

# Specific services
make logs-web -f Makefile.production
make logs-nginx -f Makefile.production
make logs-postgres -f Makefile.production
make logs-redis -f Makefile.production
make logs-celery -f Makefile.production
```

#### Redis Commander (Optional)
- **URL**: `http://localhost:8082`
- **Profile**: Start with `make monitoring -f Makefile.production`
- **Credentials**: admin/admin123 (configure in .env)

#### Health Endpoints
- **Application Health**: `GET /health/` - Comprehensive system check
- **Readiness Check**: `GET /ready/` - Service readiness
- **Liveness Check**: `GET /alive/` - Basic availability

### 🔒 Security Features

#### SSL/TLS
- **HTTPS Redirect**: HTTP automatically redirects to HTTPS
- **Self-signed Certificates**: For local development
- **Production Certificates**: Replace with real certificates

#### Security Headers
- **HSTS**: HTTP Strict Transport Security
- **CSP**: Content Security Policy
- **X-Frame-Options**: Clickjacking protection
- **X-Content-Type-Options**: MIME sniffing protection

#### Rate Limiting
- **API Endpoints**: 100 requests/minute per IP
- **General Traffic**: 1000 requests/minute per IP
- **Burst Protection**: 10 concurrent connections

### 💾 Backup Strategy

#### Automated Backups
- **Schedule**: Daily at 2 AM
- **Retention**: 7 daily, 4 weekly, 6 monthly
- **Format**: PostgreSQL dump format
- **Storage**: Local `./backups/` directory

#### Manual Backup
```bash
# Create immediate backup
make backup-now -f Makefile.production

# Restore from backup
make restore BACKUP_FILE=./backups/backup.sql -f Makefile.production
```

### 🚨 Troubleshooting

#### Common Issues

1. **Service Won't Start**
   ```bash
   # Check container status
   make ps -f Makefile.production
   
   # View specific service logs
   make logs-web -f Makefile.production
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connectivity
   make psql -f Makefile.production
   
   # Check PostgreSQL logs
   make logs-postgres -f Makefile.production
   ```

3. **Performance Issues**
   ```bash
   # Monitor resource usage
   make stats -f Makefile.production
   
   # Check health status
   make health -f Makefile.production
   ```

#### Emergency Commands
```bash
# Emergency stop
docker-compose -f docker-compose.yml -f docker-compose.production.yml down

# Force restart
docker-compose -f docker-compose.yml -f docker-compose.production.yml restart

# Full reset (DANGEROUS - loses data)
make reset -f Makefile.production
```

### 📈 Performance Tuning

#### PostgreSQL Optimization
- **shared_buffers**: 2GB (25% of 8GB system RAM)
- **effective_cache_size**: 4GB (50% of system RAM)
- **work_mem**: 16MB per connection
- **maintenance_work_mem**: 256MB

#### Redis Optimization
- **maxmemory**: 1GB with LRU eviction
- **appendonly**: Enabled for persistence
- **tcp-keepalive**: 60 seconds

#### Gunicorn Optimization
- **Workers**: 3 (2 * CPU cores + 1)
- **Worker Class**: gevent for async handling
- **Connections**: 1000 per worker
- **Timeout**: 120 seconds

### 🔄 Updates & Maintenance

#### Regular Maintenance
```bash
# Update images
make update -f Makefile.production

# Clean old data
docker system prune -f

# Check security
make security-scan -f Makefile.production
```

#### Zero-Downtime Deployment
1. Build new images
2. Update docker-compose.yml
3. Use rolling updates with health checks
4. Monitor service health during deployment

---

## 📞 Support

For issues with the production stack:

1. **Check Health**: Run `make health -f Makefile.production`
2. **Review Logs**: Run `make logs -f Makefile.production`
3. **Monitor Resources**: Run `make stats -f Makefile.production`
4. **Test Connectivity**: Use provided health endpoints

**Production Stack Version**: 1.0  
**Last Updated**: August 29, 2025  
**Docker Compose Version**: 3.8+  
**Minimum Requirements**: 4GB RAM, 2 CPU cores, 20GB storage
