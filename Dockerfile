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

# Copy application directories
COPY ./FamilyHub /app/FamilyHub
COPY ./shared /app/shared
COPY ./standalone-apps/timesheet/timesheet_app /app/timesheet_app
COPY ./scripts /app/scripts

# Set working directory to Django project root
WORKDIR /app/FamilyHub

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/FamilyHub/requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
