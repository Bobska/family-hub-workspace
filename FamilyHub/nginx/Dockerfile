# FamilyHub Nginx Dockerfile
FROM nginx:alpine

# Install openssl for self-signed certificates
RUN apk add --no-cache openssl

# Create SSL directory
RUN mkdir -p /etc/nginx/ssl

# Generate self-signed SSL certificates for local development
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/familyhub.key \
    -out /etc/nginx/ssl/familyhub.crt \
    -subj "/C=NZ/ST=Auckland/L=Auckland/O=FamilyHub/OU=Development/CN=familyhub.local" \
    -addext "subjectAltName=DNS:familyhub.local,DNS:localhost,IP:127.0.0.1"

# Create web root directories
RUN mkdir -p /var/www/html/static /var/www/html/media

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Create custom index page for status checking
RUN echo '<h1>FamilyHub Nginx - Ready</h1><p>Reverse proxy operational</p>' > /var/www/html/index.html

# Set proper permissions
RUN chown -R nginx:nginx /var/www/html \
    && chmod -R 755 /var/www/html

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
