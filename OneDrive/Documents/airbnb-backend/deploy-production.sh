#!/bin/bash
# Production deployment orchestration for AirBnB Backend containerized environment

set -e

echo "=================================================="
echo "  AirBnB Backend - Production Deployment"
echo "=================================================="

# Output formatting definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verify production environment configuration file
if [ ! -f .env.production ]; then
    echo -e "${RED}Configuration file missing: .env.production${NC}"
    echo "Initialize configuration:"
    echo "  cp .env.example .env.production"
    echo "  nano .env.production"
    exit 1
fi

# Load production environment parameters
echo -e "${YELLOW}Phase 1: Environment configuration loading${NC}"
export $(cat .env.production | grep -v '^#' | xargs)

# Validate required configuration parameters
required_vars=("SECRET_KEY" "DB_PASSWORD" "ALLOWED_HOSTS")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}Configuration error: $var undefined in .env.production${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓ Environment parameters validated${NC}"

# Build production container images
echo -e "${YELLOW}Phase 2: Production image compilation${NC}"
docker-compose -f docker-compose.prod.yml build
echo -e "${GREEN}✓ Container images compiled${NC}"

# Terminate existing container instances
echo -e "${YELLOW}Phase 3: Container instance cleanup${NC}"
docker-compose -f docker-compose.prod.yml down
echo -e "${GREEN}✓ Existing containers terminated${NC}"

# Initialize database and cache layers
echo -e "${YELLOW}Phase 4: Infrastructure service initialization${NC}"
docker-compose -f docker-compose.prod.yml up -d db redis
sleep 10
echo -e "${GREEN}✓ Database and cache services operational${NC}"

# Apply database schema migrations
echo -e "${YELLOW}Phase 5: Database schema migration${NC}"
docker-compose -f docker-compose.prod.yml run --rm web python manage.py migrate --noinput
echo -e "${GREEN}✓ Schema migrations applied${NC}"

# Consolidate application static assets
echo -e "${YELLOW}Phase 6: Static asset collection${NC}"
docker-compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static assets consolidated${NC}"

# Provision administrative user account
echo -e "${YELLOW}Phase 7: Administrative account provisioning${NC}"
docker-compose -f docker-compose.prod.yml run --rm web python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
email = '${DJANGO_SUPERUSER_EMAIL:-admin@localhost}'
password = '${DJANGO_SUPERUSER_PASSWORD:-admin123456}'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Administrative account provisioned: {username}')
else:
    print(f'Administrative account exists: {username}')
EOF
echo -e "${GREEN}✓ Administrative account configured${NC}"

# Activate all application services
echo -e "${YELLOW}Phase 8: Application service activation${NC}"
docker-compose -f docker-compose.prod.yml up -d
echo -e "${GREEN}✓ All services activated${NC}"

# Allow services to reach operational state
echo -e "${YELLOW}Waiting for service stability...${NC}"
sleep 15

# Display deployment summary
echo ""
echo "=================================================="
echo -e "${GREEN}  ✓ PRODUCTION DEPLOYMENT COMPLETED${NC}"
echo "=================================================="
echo ""
echo "Running services:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "Application endpoints:"
echo "  - Administrative interface: https://yourdomain.com/admin"
echo "  - API root: https://yourdomain.com/api/"
echo ""
echo "Management operations:"
echo "  View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  Restart services: docker-compose -f docker-compose.prod.yml restart"
echo "  Shutdown services: docker-compose -f docker-compose.prod.yml down"
echo ""
echo "Post-deployment configuration:"
echo "  1. Configure domain DNS routing to this host"
echo "  2. Provision SSL certificate using certbot utility"
echo "  3. Update nginx configuration: nginx/conf.d/app.conf"
echo "  4. Execute SSL setup: bash setup-ssl.sh"
echo ""
