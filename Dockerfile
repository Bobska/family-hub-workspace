FROM python:3.11-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=FamilyHub.settings.docker

# Copy application directories
COPY ./FamilyHub /app/FamilyHub
COPY ./standalone-apps /app/standalone-apps
COPY ./shared /app/shared
COPY ./scripts /app/scripts

# Create symbolic links for integrated apps if they don't exist
RUN mkdir -p /app/FamilyHub/apps && \
    if [ ! -d "/app/FamilyHub/apps/timesheet_app" ] && [ -d "/app/standalone-apps/timesheet/timesheet_app" ]; then \
        ln -sf /app/standalone-apps/timesheet/timesheet_app /app/FamilyHub/apps/timesheet_app; \
    fi

# Set working directory to Django project root
WORKDIR /app/FamilyHub

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/FamilyHub/requirements.txt

# Start Django application directly with simple wait
CMD ["sh", "-c", "sleep 10 && cd /app/FamilyHub && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py init_superuser && gunicorn FamilyHub.wsgi:application --bind 0.0.0.0:8000"]
