# 🚀 AirBnB Backend - Production Deployment Guide

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Server Requirements](#server-requirements)
3. [Quick Deployment](#quick-deployment)
4. [Detailed Setup](#detailed-setup)
5. [SSL Configuration](#ssl-configuration)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

- [ ] Server with Docker & Docker Compose installed
- [ ] Domain name configured and pointing to server IP
- [ ] Server firewall configured (ports 80, 443, 22)
- [ ] SSH access to production server
- [ ] Database backup strategy planned
- [ ] Environment variables configured

---

## Server Requirements

### Minimum Specifications
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04+ / Debian 10+ / CentOS 8+

### Software Requirements
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

---

## Quick Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/Martin-Mawien/airbnb-backend.git
cd airbnb-backend
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env.production

# Edit with your settings
nano .env.production
```

**Critical settings to update:**
```bash
SECRET_KEY=your-super-secret-key-50-chars-minimum
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=strong-database-password
DJANGO_SUPERUSER_PASSWORD=secure-admin-password
```

### Step 3: Deploy
```bash
# Make deployment script executable
chmod +x deploy-production.sh

# Run deployment
./deploy-production.sh
```

### Step 4: Setup SSL
```bash
# Make SSL script executable
chmod +x setup-ssl.sh

# Run SSL setup
./setup-ssl.sh
```

---

## Detailed Setup

### 1. Environment Configuration

#### Required Environment Variables

**Security Settings:**
```env
SECRET_KEY=generate-with-python-command
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Generate SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Database Settings:**
```env
DB_NAME=airbnb_production
DB_USER=airbnb_prod_user
DB_PASSWORD=use-strong-password-min-20-chars
DB_HOST=db
DB_PORT=5432
```

**Email Configuration (for notifications):**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-specific-password
```

**CORS Settings:**
```env
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Build and Deploy

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 3. Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test database connection
docker-compose -f docker-compose.prod.yml exec db psql -U airbnb_prod_user -d airbnb_production -c "\dt"
```

---

## SSL Configuration

### Method 1: Automated (Recommended)

```bash
./setup-ssl.sh
```

### Method 2: Manual Setup

```bash
# Update nginx configuration with your domain
sed -i 's/yourdomain.com/youractualdomain.com/g' nginx/conf.d/app.conf

# Obtain certificate
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email your-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d yourdomain.com \
    -d www.yourdomain.com

# Reload nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

### Certificate Auto-Renewal

Certificates auto-renew via the certbot container. Verify setup:
```bash
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates
```

---

## Monitoring & Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f db
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Database Backup

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U airbnb_prod_user airbnb_production > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
cat backup_file.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U airbnb_prod_user airbnb_production
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Health Checks

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check disk usage
docker system df

# Check container resources
docker stats
```

---

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Rebuild if needed
docker-compose -f docker-compose.prod.yml up -d --build
```

### Database Connection Issues

```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Test connection
docker-compose -f docker-compose.prod.yml exec db psql -U airbnb_prod_user -d airbnb_production

# Check environment variables
docker-compose -f docker-compose.prod.yml exec web env | grep DB_
```

### Static Files Not Loading

```bash
# Collect static files again
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

### SSL Certificate Issues

```bash
# Check certificate status
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates

# Renew certificate manually
docker-compose -f docker-compose.prod.yml exec certbot certbot renew

# Check nginx SSL configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Increase workers (in .env.production)
WEB_CONCURRENCY=8

# Restart services
docker-compose -f docker-compose.prod.yml restart web
```

---

## Security Best Practices

### 1. Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Firewall Configuration
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### 3. SSH Hardening
```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Use SSH keys only
# Set: PasswordAuthentication no

# Restart SSH
sudo systemctl restart sshd
```

### 4. Database Security
- Use strong passwords (20+ characters)
- Regular backups
- Encrypt backups
- Store backups off-server

### 5. Application Security
- Keep DEBUG=0 in production
- Use strong SECRET_KEY
- Regular security updates
- Monitor error logs

---

## Production Checklist

### Before Going Live
- [ ] All environment variables configured
- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=0
- [ ] Database password is strong
- [ ] Domain DNS configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Error logging configured

### After Deployment
- [ ] Test all major features
- [ ] Verify SSL certificate
- [ ] Test admin panel access
- [ ] Verify API endpoints
- [ ] Check email notifications
- [ ] Monitor performance
- [ ] Set up automated backups
- [ ] Configure monitoring alerts

---

## Support & Resources

- **Documentation**: See `SETUP_COMPLETE.md` for detailed setup
- **Quick Start**: See `QUICKSTART.md` for development guide
- **Repository**: https://github.com/Martin-Mawien/airbnb-backend
- **Issues**: Report bugs on GitHub Issues

---

## Deployment Platforms

### AWS EC2
1. Launch Ubuntu 20.04 instance
2. Configure security groups (ports 80, 443, 22)
3. Follow Quick Deployment steps
4. Use Elastic IP for stable IP address

### Digital Ocean
1. Create Ubuntu droplet
2. Add domain to droplet
3. Follow Quick Deployment steps
4. Use managed databases for production

### Heroku
See separate guide for Heroku deployment

### Docker Swarm / Kubernetes
For high-availability deployments, see advanced deployment docs

---

**Author**: Martin Mawien  
**License**: MIT  
**Version**: 1.0.0  
**Last Updated**: January 19, 2026
