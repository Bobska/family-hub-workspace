FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements/ /requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements/development.txt

# Copy project directories
COPY FamilyHub/ /app/
COPY standalone-apps/ /standalone-apps/
COPY shared/ /shared/

# Set Python path to include all necessary directories
ENV PYTHONPATH="/app:/standalone-apps:/shared"

# Create non-root user
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app /standalone-apps /shared
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
