FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=FamilyHub.settings.docker

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project structure
COPY . .

# Copy standalone apps from parent directory
COPY ../standalone-apps /standalone-apps

# Create symbolic links or copy apps for integration
RUN mkdir -p /app/apps && \
    if [ -d "/standalone-apps/timesheet/timesheet_app" ]; then \
        if [ ! -d "/app/apps/timesheet_app" ]; then \
            ln -sf /standalone-apps/timesheet/timesheet_app /app/apps/ || \
            cp -r /standalone-apps/timesheet/timesheet_app /app/apps/; \
        fi; \
    fi

# Set working directory to Django project root
WORKDIR /app/FamilyHub

# Run migrations and collect static files (after copying files)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=10)" || exit 1

# Command to run the application
CMD ["sh", "-c", "cd /app/FamilyHub && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
