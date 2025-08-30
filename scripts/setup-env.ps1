# Environment Setup Script for FamilyHub (Windows PowerShell)

Write-Host "🔧 FamilyHub Environment Setup" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Function to generate Django secret key
function Generate-SecretKey {
    try {
        $key = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        return $key
    } catch {
        # Fallback method
        $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        $key = ""
        for ($i = 0; $i -lt 50; $i++) {
            $key += $chars[(Get-Random -Maximum $chars.Length)]
        }
        return $key
    }
}

# Function to generate secure password
function Generate-Password {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    $password = ""
    for ($i = 0; $i -lt 16; $i++) {
        $password += $chars[(Get-Random -Maximum $chars.Length)]
    }
    return $password
}

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python is required but not installed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Available environment templates:" -ForegroundColor Cyan
Write-Host "1. Local Development (.env.local)" -ForegroundColor White
Write-Host "2. Docker Development (.env.docker)" -ForegroundColor White
Write-Host "3. Production (.env.prod.example)" -ForegroundColor White
Write-Host "4. Custom setup" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Choose environment type (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🖥️  Setting up Local Development environment..." -ForegroundColor Blue
        Copy-Item ".env.local" ".env"
        $envFile = ".env"
    }
    "2" {
        Write-Host "🐳 Setting up Docker Development environment..." -ForegroundColor Blue
        Copy-Item ".env.docker" ".env"
        $envFile = ".env"
    }
    "3" {
        Write-Host "🚀 Setting up Production environment..." -ForegroundColor Blue
        Copy-Item ".env.prod.example" ".env.prod"
        $envFile = ".env.prod"
    }
    "4" {
        Write-Host "🔧 Custom setup..." -ForegroundColor Blue
        Copy-Item ".env.example" ".env"
        $envFile = ".env"
    }
    default {
        Write-Host "❌ Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🔐 Generating secure credentials..." -ForegroundColor Yellow

# Generate new credentials
$newSecretKey = Generate-SecretKey
Write-Host "✅ Generated Django SECRET_KEY" -ForegroundColor Green

$newDbPassword = Generate-Password
Write-Host "✅ Generated database password" -ForegroundColor Green

$newAdminPassword = Generate-Password
Write-Host "✅ Generated admin password" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Updating environment file: $envFile" -ForegroundColor Blue

# Read file content
$content = Get-Content $envFile

# Update credentials
$content = $content -replace "SECRET_KEY=.*", "SECRET_KEY=$newSecretKey"
$content = $content -replace "POSTGRES_PASSWORD=.*", "POSTGRES_PASSWORD=$newDbPassword"
$content = $content -replace "DJANGO_SUPERUSER_PASSWORD=.*", "DJANGO_SUPERUSER_PASSWORD=$newAdminPassword"

# Write updated content
$content | Set-Content $envFile

Write-Host "✅ Updated SECRET_KEY" -ForegroundColor Green
Write-Host "✅ Updated POSTGRES_PASSWORD" -ForegroundColor Green
Write-Host "✅ Updated DJANGO_SUPERUSER_PASSWORD" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan

switch ($choice) {
    "1" {
        Write-Host "1. Install PostgreSQL locally" -ForegroundColor White
        Write-Host "2. Create database: createdb familyhub_dev" -ForegroundColor White
        Write-Host "3. Run: python manage.py migrate" -ForegroundColor White
        Write-Host "4. Run: python manage.py runserver" -ForegroundColor White
    }
    "2" {
        Write-Host "1. Start Docker services: docker-compose up -d" -ForegroundColor White
        Write-Host "2. Check status: docker-compose ps" -ForegroundColor White
        Write-Host "3. View logs: docker-compose logs -f" -ForegroundColor White
    }
    "3" {
        Write-Host "1. Review and update $envFile with your domain" -ForegroundColor White
        Write-Host "2. Set ALLOWED_HOSTS to your production domain" -ForegroundColor White
        Write-Host "3. Configure email settings if needed" -ForegroundColor White
        Write-Host "4. Deploy: docker-compose -f docker-compose.prod.yml up -d" -ForegroundColor White
    }
    default {
        Write-Host "1. Review and customize $envFile" -ForegroundColor White
        Write-Host "2. Follow the deployment guide for your chosen setup" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "📖 For more details, see ENVIRONMENT_SETUP.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔑 Your generated credentials:" -ForegroundColor Yellow
Write-Host "   Database Password: $newDbPassword" -ForegroundColor White
Write-Host "   Admin Password: $newAdminPassword" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Save these credentials securely and never commit $envFile to version control!" -ForegroundColor Red
