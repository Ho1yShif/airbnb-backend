#!/bin/bash
set -e

echo "🚀 AirBnB Backend - Render Deployment Script"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo -e "${RED}❌ Error: render.yaml not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found render.yaml${NC}"

# Check if user has Render CLI installed
if ! command -v render &> /dev/null; then
    echo -e "${YELLOW}⚠ Render CLI not found. Installing...${NC}"
    echo "Visit: https://render.com/docs/cli for installation instructions"
    echo ""
    echo "Quick install:"
    echo "  macOS: brew install render"
    echo "  Linux/WSL: npm install -g @render/cli"
    exit 1
fi

echo -e "${GREEN}✓ Render CLI found${NC}"

# Authenticate with Render
echo ""
echo -e "${YELLOW}→ Authenticating with Render...${NC}"
render login

# Create/Update services from render.yaml
echo ""
echo -e "${YELLOW}→ Deploying services to Render...${NC}"
render blueprint launch

echo ""
echo -e "${GREEN}✅ Deployment initiated successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Visit https://dashboard.render.com to monitor deployment"
echo "2. Once deployed, run migrations via Render Shell:"
echo "   python manage.py migrate"
echo "   python manage.py createsuperuser"
echo "3. Your app will be available at: https://airbnb-backend-web.onrender.com"
echo ""
