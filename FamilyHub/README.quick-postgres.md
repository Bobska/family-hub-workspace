# FamilyHub Quick PostgreSQL Setup

## ⚡ 5-Minute PostgreSQL 17.6 Development Environment

Get PostgreSQL 17.6 + pgAdmin running instantly for FamilyHub development!

### 🚀 Quick Start

```bash
# 1. Start PostgreSQL + pgAdmin (5 minutes setup)
docker-compose -f docker-compose.quick.yml --env-file .env.quick up -d

# 2. Verify services are running
docker-compose -f docker-compose.quick.yml ps

# 3. Access your database!
```

### 🌐 Access Points

- **pgAdmin Web Interface**: http://localhost:5050
  - Email: `admin@familyhub.local`
  - Password: `admin123`

- **PostgreSQL Direct Connection**:
  - Host: `localhost`
  - Port: `5432`
  - Database: `familyhub`
  - Username: `django`
  - Password: `secretpass`

- **Django Database URL**: 
  ```
  postgresql://django:secretpass@localhost:5432/familyhub
  ```

### 📦 What's Included

#### Core Services
- **PostgreSQL 17.6 Alpine** - Latest PostgreSQL with optimal performance
- **pgAdmin 4** - Web-based database administration tool
- **Health Checks** - Automatic service monitoring
- **Persistent Storage** - Data survives container restarts

#### Optional Services
```bash
# Add Redis for caching and sessions
docker-compose -f docker-compose.quick.yml --profile full --env-file .env.quick up -d
```

### ⚙️ Configuration

#### Environment Variables (`.env.quick`)
```bash
POSTGRES_DB=familyhub
POSTGRES_USER=django  
POSTGRES_PASSWORD=secretpass
PGADMIN_EMAIL=admin@familyhub.local
PGADMIN_PASSWORD=admin123
REDIS_PASSWORD=redis123
```

#### pgAdmin Pre-configured Server
- Server automatically appears in pgAdmin
- No manual server setup required
- Direct connection to PostgreSQL container

### 🔧 Management Commands

```bash
# Start services
docker-compose -f docker-compose.quick.yml up -d

# Stop services  
docker-compose -f docker-compose.quick.yml down

# View logs
docker-compose -f docker-compose.quick.yml logs -f

# Restart PostgreSQL only
docker-compose -f docker-compose.quick.yml restart postgres-dev

# Clean everything (removes data!)
docker-compose -f docker-compose.quick.yml down -v
```

### 🧪 Django Integration

#### Update Django Settings
```python
# In your settings/development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'familyhub',
        'USER': 'django',
        'PASSWORD': 'secretpass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Run Django Commands
```bash
# Navigate to FamilyHub directory
cd FamilyHub

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 🔍 Troubleshooting

#### Service Status Check
```bash
# Check if containers are running
docker ps | grep familyhub

# Check service health
docker-compose -f docker-compose.quick.yml exec postgres-dev pg_isready -U django -d familyhub
```

#### Connection Issues
```bash
# Test PostgreSQL connection
psql -h localhost -p 5432 -U django -d familyhub

# View PostgreSQL logs
docker-compose -f docker-compose.quick.yml logs postgres-dev

# Restart all services
docker-compose -f docker-compose.quick.yml restart
```

#### Reset Database
```bash
# Stop services
docker-compose -f docker-compose.quick.yml down

# Remove volumes (WARNING: Deletes all data!)
docker volume rm familyhub_postgres_quick_data
docker volume rm familyhub_pgadmin_quick_data

# Start fresh
docker-compose -f docker-compose.quick.yml up -d
```

### 📊 Performance Notes

- **PostgreSQL 17.6**: Latest features and performance improvements
- **Alpine Linux**: Minimal footprint for faster startup
- **Health Checks**: Automatic service monitoring and restart
- **Optimized Settings**: Pre-configured for development workloads

### 🔐 Security Notes

**Development Only**: This setup uses simple passwords and is designed for local development only.

For production, use:
- Strong, unique passwords
- SSL/TLS connections
- Network isolation
- Regular backups

### 🎯 Next Steps

1. **Start Services**: `docker-compose -f docker-compose.quick.yml up -d`
2. **Open pgAdmin**: http://localhost:5050
3. **Connect Django**: Update your settings with the database URL
4. **Run Migrations**: `python manage.py migrate`
5. **Start Coding**: Your PostgreSQL environment is ready!

---

**Ready in 5 minutes!** 🚀
**PostgreSQL 17.6** ✅
**pgAdmin Included** ✅  
**Zero Configuration** ✅
