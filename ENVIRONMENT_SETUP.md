# 🔧 Environment Variables Configuration Guide

## 📋 Overview
FamilyHub uses environment variables for secure configuration management across different deployment environments. This guide explains how to set up and manage environment variables for local development, Docker containers, and production deployment.

## 🏗️ Environment Files Structure

```
family-hub-workspace/
├── .env.example         # ✅ Template with all variables documented (committed)
├── .env.local           # ✅ Local development template (committed)  
├── .env.docker          # ✅ Docker development template (committed)
├── .env.prod.example    # ✅ Production template (committed)
├── .env                 # ❌ Your actual environment file (DO NOT COMMIT)
├── .env.prod           # ❌ Production environment file (DO NOT COMMIT)
└── .gitignore          # ✅ Protects sensitive .env files
```

## 🚀 Quick Setup

### 1. **Choose Your Environment**

#### **Local Development (without Docker)**
```bash
cp .env.local .env
# Edit .env with your local settings
```

#### **Docker Development**
```bash
cp .env.docker .env
# No additional changes needed for basic Docker setup
```

#### **Production Deployment**
```bash
cp .env.prod.example .env.prod
# Edit .env.prod with your production values
```

### 2. **Generate Secret Key**
```bash
# Generate a new Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. **Update Critical Variables**
Always change these before deployment:
- `SECRET_KEY` - Generate new key for each environment
- `POSTGRES_PASSWORD` - Use strong database password
- `DJANGO_SUPERUSER_PASSWORD` - Use strong admin password
- `ALLOWED_HOSTS` - Add your domain for production

## 📚 Environment Variables Reference

### 🗄️ **Database Configuration**

| Variable | Description | Local Example | Docker Example | Production Example |
|----------|-------------|---------------|----------------|-------------------|
| `POSTGRES_DB` | Database name | `familyhub_dev` | `familyhub_docker` | `familyhub_prod` |
| `POSTGRES_USER` | Database user | `familyhub_user` | `familyhub_user` | `familyhub_user` |
| `POSTGRES_PASSWORD` | Database password | `DevPassword123!` | `DockerPassword123!` | `ProD_Pass_2025!` |
| `POSTGRES_HOST` | Database host | `localhost` | `db` | `db` |
| `POSTGRES_PORT` | Database port | `5432` | `5432` | `5432` |

### ⚙️ **Django Core Settings**

| Variable | Description | Local | Docker | Production |
|----------|-------------|-------|--------|------------|
| `SECRET_KEY` | Django secret key | `django-insecure-local-...` | `django-insecure-docker-...` | `generate-new-key-here` |
| `DEBUG` | Debug mode | `True` | `True` | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` | `localhost,127.0.0.1,web` | `yourdomain.com,localhost` |
| `DJANGO_SETTINGS_MODULE` | Settings module | `.development` | `.docker` | `.production` |

### 🔐 **Security Settings**

| Variable | Description | Development | Production |
|----------|-------------|-------------|------------|
| `SECURE_SSL_REDIRECT` | Force HTTPS | `False` | `True` |
| `SESSION_COOKIE_SECURE` | Secure cookies | `False` | `True` |
| `CSRF_COOKIE_SECURE` | Secure CSRF | `False` | `True` |
| `SESSION_COOKIE_AGE` | Session timeout | `86400` (24h) | `3600` (1h) |

### 📧 **Email Configuration**

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_BACKEND` | Email backend | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` (TLS) or `465` (SSL) |
| `EMAIL_USE_TLS` | Use TLS | `True` |
| `EMAIL_HOST_USER` | SMTP username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | SMTP password | `your-app-password` |

### 📊 **Cache & Performance**

| Variable | Description | Example |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection | `redis://redis:6379/0` |
| `CACHE_TIMEOUT` | Default cache timeout | `300` (5 minutes) |
| `DATABASE_CONN_MAX_AGE` | DB connection lifetime | `600` (10 minutes) |

## 🔄 Environment-Specific Setup

### 🖥️ **Local Development Setup**

1. **Install PostgreSQL locally**
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   
   # macOS with Homebrew
   brew install postgresql
   
   # Windows - Download from postgresql.org
   ```

2. **Create local database**
   ```bash
   sudo -u postgres createuser familyhub_user
   sudo -u postgres createdb familyhub_dev
   sudo -u postgres psql -c "ALTER USER familyhub_user PASSWORD 'DevPassword123!';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE familyhub_dev TO familyhub_user;"
   ```

3. **Configure environment**
   ```bash
   cp .env.local .env
   # Edit SECRET_KEY and passwords
   ```

### 🐳 **Docker Development Setup**

1. **Use Docker environment**
   ```bash
   cp .env.docker .env
   docker-compose up -d
   ```

2. **Access services**
   - **Application**: http://localhost:8000
   - **Database**: localhost:5432
   - **Admin**: http://localhost:8000/admin/

### 🚀 **Production Setup**

1. **Prepare production environment**
   ```bash
   cp .env.prod.example .env.prod
   # Edit all production values
   ```

2. **Generate secure credentials**
   ```bash
   # Generate secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   
   # Generate passwords
   openssl rand -base64 32
   ```

3. **Deploy with production config**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🛡️ Security Best Practices

### ✅ **Do's**
- ✅ Use different passwords for each environment
- ✅ Generate new SECRET_KEY for each environment
- ✅ Set `DEBUG=False` in production
- ✅ Use strong passwords (12+ characters, mixed case, numbers, symbols)
- ✅ Regularly rotate passwords and keys
- ✅ Use HTTPS in production (`SECURE_SSL_REDIRECT=True`)
- ✅ Keep `.env` files in `.gitignore`

### ❌ **Don'ts**
- ❌ Never commit `.env` files with real credentials
- ❌ Don't use default passwords in production
- ❌ Don't share environment files via email/chat
- ❌ Don't use same passwords across environments
- ❌ Don't enable DEBUG in production
- ❌ Don't ignore SSL settings in production

## 🔍 Environment Validation

### **Check Current Configuration**
```bash
# View current environment (without secrets)
python manage.py diffsettings

# Test database connection
python manage.py dbshell

# Validate configuration
python manage.py check --deploy
```

### **Common Issues & Solutions**

#### **Database Connection Failed**
```bash
# Check environment variables
echo $POSTGRES_HOST $POSTGRES_PORT $POSTGRES_DB

# Test connection manually
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB
```

#### **SECRET_KEY Not Set**
```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### **ALLOWED_HOSTS Error**
```bash
# Add your domain to ALLOWED_HOSTS
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

## 📋 Environment Checklist

### **Development Checklist**
- [ ] `.env` file created from template
- [ ] `SECRET_KEY` generated and set
- [ ] Database credentials configured
- [ ] `DEBUG=True` for development
- [ ] Local database accessible
- [ ] Django server starts successfully

### **Production Checklist**
- [ ] `.env.prod` file created with production values
- [ ] Strong `SECRET_KEY` generated
- [ ] Strong database password set
- [ ] Strong admin password set
- [ ] `DEBUG=False` confirmed
- [ ] `ALLOWED_HOSTS` includes production domain
- [ ] SSL settings configured if using HTTPS
- [ ] Email settings configured for notifications
- [ ] Backup strategy implemented

## 🆘 Troubleshooting

### **Reset Environment**
```bash
# Start fresh with clean environment
rm .env
cp .env.example .env
# Edit with your settings
```

### **Docker Environment Issues**
```bash
# Rebuild containers with new environment
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **Permission Issues**
```bash
# Fix Docker volume permissions
docker-compose exec web chown -R app:app /app/FamilyHub/media
docker-compose exec web chown -R app:app /app/FamilyHub/staticfiles
```

---

**🔧 Need Help?**
- Check the main [PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md) for full deployment guide
- Review Django settings in `FamilyHub/settings/` directory
- Test configuration with `python manage.py check --deploy`

**Last Updated**: August 31, 2025
