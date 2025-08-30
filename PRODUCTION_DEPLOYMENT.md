# 🚀 FamilyHub Production Deployment Guide

## 📋 Overview
This guide covers the production deployment of FamilyHub using Docker Compose with PostgreSQL 17, Redis, and Nginx.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Nginx    │────│   Django    │────│ PostgreSQL  │
│   (Proxy)   │    │ (Gunicorn)  │    │   (DB)      │
│  Port 80/443│    │  Port 8000  │    │  Port 5432  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                   ┌─────────────┐
                   │    Redis    │
                   │  (Cache)    │
                   │  Port 6379  │
                   └─────────────┘
```

## 🛠️ Services

### 1. **Nginx (Reverse Proxy)**
- **Image**: `nginx:alpine`
- **Purpose**: 
  - Reverse proxy to Django application
  - Serves static and media files directly
  - SSL termination (when configured)
  - Security headers and rate limiting
- **Ports**: 80 (HTTP), 443 (HTTPS)

### 2. **Django Web Application**
- **Image**: Custom built from `Dockerfile.prod`
- **Purpose**: 
  - Main FamilyHub application
  - Gunicorn WSGI server with 3 workers
  - Static file collection and serving
- **Port**: 8000 (internal)

### 3. **PostgreSQL Database**
- **Image**: `postgres:17-alpine`
- **Purpose**: 
  - Primary database storage
  - Persistent data volumes
  - Health monitoring
- **Port**: 5432

### 4. **Redis Cache**
- **Image**: `redis:alpine`
- **Purpose**: 
  - Session storage
  - Application caching
  - Performance optimization
- **Port**: 6379

## 🚀 Quick Start

### 1. **Prepare Environment**
```bash
# Copy environment template
cp .env.prod.example .env.prod

# Edit production settings
nano .env.prod
```

### 2. **Deploy Application**
```bash
# Linux/Mac
./scripts/production/deploy.sh

# Windows PowerShell
.\scripts\production\deploy.ps1

# Manual deployment
docker-compose -f docker-compose.prod.yml up -d
```

### 3. **Verify Deployment**
```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Test health endpoint
curl http://localhost/health/

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## ⚙️ Configuration

### Environment Variables (.env.prod)

#### **Django Settings**
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DJANGO_SETTINGS_MODULE=FamilyHub.settings.production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

#### **Database Configuration**
```env
POSTGRES_DB=familyhub_prod
POSTGRES_USER=familyhub_user
POSTGRES_PASSWORD=your-secure-database-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

#### **Cache Configuration**
```env
REDIS_URL=redis://redis:6379/0
```

#### **Admin User**
```env
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=your-secure-admin-password
```

### Nginx Configuration

#### **Security Features**
- ✅ Security headers (XSS, CSRF, Content-Type)
- ✅ Rate limiting for admin and API endpoints
- ✅ File upload size limits (10MB)
- ✅ Gzip compression
- ✅ Static file caching

#### **Performance Features**
- ✅ Static file serving with long-term caching
- ✅ Gzip compression for text assets
- ✅ Connection pooling and keep-alive
- ✅ Optimized proxy settings

## 🔧 Management Commands

### **Application Management**
```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# Stop services
docker-compose -f docker-compose.prod.yml down

# Restart specific service
docker-compose -f docker-compose.prod.yml restart web

# View logs
docker-compose -f docker-compose.prod.yml logs -f web
```

### **Database Operations**
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Database backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U familyhub_user familyhub_prod > backup.sql
```

### **Static Files**
```bash
# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Clear cache
docker-compose -f docker-compose.prod.yml exec web python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

## 📊 Monitoring

### **Health Checks**
- **Application**: `http://localhost/health/`
- **Database**: Built-in PostgreSQL health check
- **Cache**: Redis ping command
- **Nginx**: Configuration test

### **Log Files**
```bash
# Application logs
docker-compose -f docker-compose.prod.yml logs web

# Database logs
docker-compose -f docker-compose.prod.yml logs db

# Nginx logs
docker-compose -f docker-compose.prod.yml logs nginx

# All services
docker-compose -f docker-compose.prod.yml logs -f
```

### **Performance Monitoring**
- Django logs: `/app/FamilyHub/logs/familyhub.log`
- Nginx access logs: Standard Docker logging
- Database performance: PostgreSQL built-in monitoring

## 🔐 Security

### **Current Security Measures**
- ✅ Non-root user in containers
- ✅ Security headers via Nginx
- ✅ Rate limiting on sensitive endpoints
- ✅ CSRF protection
- ✅ Input validation and sanitization
- ✅ Secure session configuration

### **SSL/HTTPS Setup** (Optional)
```nginx
# Uncomment in nginx.conf for SSL
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    
    # ... rest of configuration
}
```

## 🔄 Backup & Recovery

### **Database Backup**
```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U familyhub_user familyhub_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
cat backup.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U familyhub_user familyhub_prod
```

### **Volume Backup**
```bash
# Backup persistent volumes
docker run --rm -v family-hub-workspace_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
docker run --rm -v family-hub-workspace_static_volume:/data -v $(pwd):/backup alpine tar czf /backup/static_backup.tar.gz -C /data .
```

## 🚨 Troubleshooting

### **Common Issues**

#### **503 Service Unavailable**
```bash
# Check Django service status
docker-compose -f docker-compose.prod.yml logs web

# Verify database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

#### **Static Files Not Loading**
```bash
# Recollect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

#### **Database Connection Issues**
```bash
# Check database health
docker-compose -f docker-compose.prod.yml exec db pg_isready -U familyhub_user

# Check network connectivity
docker-compose -f docker-compose.prod.yml exec web ping db
```

### **Performance Issues**
```bash
# Check resource usage
docker stats

# Monitor application performance
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```

## 📈 Scaling

### **Horizontal Scaling**
```yaml
# Scale web workers
web:
  deploy:
    replicas: 3
  command: gunicorn --workers 4 --bind 0.0.0.0:8000 FamilyHub.wsgi:application
```

### **Load Balancing**
- Configure Nginx upstream for multiple Django instances
- Use Docker Swarm or Kubernetes for orchestration
- Implement Redis Sentinel for cache high availability

## 🔮 Future Enhancements

### **Planned Features**
- [ ] SSL/TLS certificate automation (Let's Encrypt)
- [ ] Application Performance Monitoring (APM)
- [ ] Log aggregation (ELK Stack)
- [ ] Automated backups with retention
- [ ] Container orchestration (Kubernetes)
- [ ] CI/CD pipeline integration

### **Production Readiness Checklist**
- ✅ Multi-service Docker Compose setup
- ✅ Production Django settings
- ✅ PostgreSQL with persistent storage
- ✅ Redis caching layer
- ✅ Nginx reverse proxy
- ✅ Security headers and rate limiting
- ✅ Health checks and monitoring
- ✅ Deployment automation scripts
- ⏳ SSL/HTTPS configuration
- ⏳ Automated backup system
- ⏳ Log aggregation
- ⏳ Performance monitoring

---

**Version**: 1.0.0  
**Last Updated**: August 31, 2025  
**Maintained by**: FamilyHub Development Team
