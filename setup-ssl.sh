#!/bin/bash
# SSL Certificate Setup Script using Let's Encrypt

set -e

echo "=================================================="
echo "  SSL Certificate Setup with Let's Encrypt"
echo "=================================================="

# Get domain from user
read -p "Enter your domain name (e.g., yourdomain.com): " DOMAIN
read -p "Enter your email address for Let's Encrypt: " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Error: Domain and email are required!"
    exit 1
fi

echo ""
echo "Setting up SSL for: $DOMAIN"
echo "Contact email: $EMAIL"
echo ""

# Update nginx configuration with domain
echo "[1/4] Updating nginx configuration..."
sed -i "s/yourdomain.com/$DOMAIN/g" nginx/conf.d/app.conf
echo "✓ Nginx configuration updated"

# Create directories for certbot
echo "[2/4] Creating certbot directories..."
mkdir -p certbot/conf certbot/www
echo "✓ Directories created"

# Get SSL certificate
echo "[3/4] Obtaining SSL certificate..."
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

echo "✓ SSL certificate obtained"

# Reload nginx
echo "[4/4] Reloading nginx..."
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
echo "✓ Nginx reloaded"

echo ""
echo "=================================================="
echo "  ✓ SSL CERTIFICATE SETUP COMPLETE"
echo "=================================================="
echo ""
echo "Your site is now accessible at:"
echo "  https://$DOMAIN"
echo "  https://www.$DOMAIN"
echo ""
echo "Certificate auto-renewal is configured."
echo "Certbot will automatically renew certificates before expiry."
echo ""
