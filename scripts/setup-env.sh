#!/bin/bash
# Environment Setup Script for FamilyHub

set -e

echo "🔧 FamilyHub Environment Setup"
echo "=============================="

# Function to generate Django secret key
generate_secret_key() {
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
}

# Function to generate secure password
generate_password() {
    openssl rand -base64 24 | tr -d "=+/" | cut -c1-16
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo ""
echo "📋 Available environment templates:"
echo "1. Local Development (.env.local)"
echo "2. Docker Development (.env.docker)"  
echo "3. Production (.env.prod.example)"
echo "4. Custom setup"
echo ""

read -p "Choose environment type (1-4): " choice

case $choice in
    1)
        echo "🖥️  Setting up Local Development environment..."
        cp .env.local .env
        env_file=".env"
        ;;
    2)
        echo "🐳 Setting up Docker Development environment..."
        cp .env.docker .env
        env_file=".env"
        ;;
    3)
        echo "🚀 Setting up Production environment..."
        cp .env.prod.example .env.prod
        env_file=".env.prod"
        ;;
    4)
        echo "🔧 Custom setup..."
        cp .env.example .env
        env_file=".env"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🔐 Generating secure credentials..."

# Generate new secret key
new_secret_key=$(generate_secret_key)
echo "✅ Generated Django SECRET_KEY"

# Generate database password
new_db_password=$(generate_password)
echo "✅ Generated database password"

# Generate admin password
new_admin_password=$(generate_password)
echo "✅ Generated admin password"

echo ""
echo "📝 Updating environment file: $env_file"

# Update SECRET_KEY
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$new_secret_key/" "$env_file"
    sed -i '' "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$new_db_password/" "$env_file"
    sed -i '' "s/DJANGO_SUPERUSER_PASSWORD=.*/DJANGO_SUPERUSER_PASSWORD=$new_admin_password/" "$env_file"
else
    # Linux
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$new_secret_key/" "$env_file"
    sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$new_db_password/" "$env_file"
    sed -i "s/DJANGO_SUPERUSER_PASSWORD=.*/DJANGO_SUPERUSER_PASSWORD=$new_admin_password/" "$env_file"
fi

echo "✅ Updated SECRET_KEY"
echo "✅ Updated POSTGRES_PASSWORD"
echo "✅ Updated DJANGO_SUPERUSER_PASSWORD"

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "📋 Next steps:"

if [[ $choice == 1 ]]; then
    echo "1. Install PostgreSQL locally"
    echo "2. Create database: createdb familyhub_dev"
    echo "3. Run: python manage.py migrate"
    echo "4. Run: python manage.py runserver"
elif [[ $choice == 2 ]]; then
    echo "1. Start Docker services: docker-compose up -d"
    echo "2. Check status: docker-compose ps"
    echo "3. View logs: docker-compose logs -f"
elif [[ $choice == 3 ]]; then
    echo "1. Review and update $env_file with your domain"
    echo "2. Set ALLOWED_HOSTS to your production domain"
    echo "3. Configure email settings if needed"
    echo "4. Deploy: docker-compose -f docker-compose.prod.yml up -d"
else
    echo "1. Review and customize $env_file"
    echo "2. Follow the deployment guide for your chosen setup"
fi

echo ""
echo "📖 For more details, see ENVIRONMENT_SETUP.md"
echo ""
echo "🔑 Your generated credentials:"
echo "   Database Password: $new_db_password"
echo "   Admin Password: $new_admin_password"
echo ""
echo "⚠️  Save these credentials securely and never commit $env_file to version control!"
