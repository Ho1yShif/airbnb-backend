#!/bin/bash
# REST API endpoint validation utility
# Performs comprehensive testing of all API routes with curl requests

API_ROOT="http://localhost:8000/api"
ADMIN_ACCOUNT="admin"
ADMIN_CREDENTIAL="admin123456"

echo "=========================================="
echo "   REST API VALIDATION TEST SUITE"
echo "=========================================="
echo ""

# Output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Verify API service availability
echo -e "${YELLOW}[TEST 1] API Root Endpoint${NC}"
curl -s "$API_ROOT/" | head -20
echo ""
echo ""

# Test 2: Retrieve properties collection
echo -e "${YELLOW}[TEST 2] GET /api/properties/${NC}"
curl -s "$API_ROOT/properties/" | python -m json.tool | head -30
echo ""
echo ""

# Test 3: Retrieve user profile collection
echo -e "${YELLOW}[TEST 3] GET /api/user-profiles/${NC}"
curl -s "$API_ROOT/user-profiles/" | python -m json.tool | head -30
echo ""
echo ""

# Test 4: Access bookings endpoint (authenticated)
echo -e "${YELLOW}[TEST 4] GET /api/bookings/ (authenticated)${NC}"
curl -s -u "$ADMIN_ACCOUNT:$ADMIN_CREDENTIAL" "$API_ROOT/bookings/" | python -m json.tool | head -30
echo ""
echo ""

# Test 5: Retrieve reviews collection
echo -e "${YELLOW}[TEST 5] GET /api/reviews/${NC}"
curl -s "$API_ROOT/reviews/" | python -m json.tool | head -30
echo ""
echo ""

# Test 6: Access payments endpoint (authenticated)
echo -e "${YELLOW}[TEST 6] GET /api/payments/ (authenticated)${NC}"
curl -s -u "$ADMIN_ACCOUNT:$ADMIN_CREDENTIAL" "$API_ROOT/payments/" | python -m json.tool | head -30
echo ""
echo ""

# Test 7: Access wishlists endpoint (authenticated)
echo -e "${YELLOW}[TEST 7] GET /api/wishlists/ (authenticated)${NC}"
curl -s -u "$ADMIN_ACCOUNT:$ADMIN_CREDENTIAL" "$API_ROOT/wishlists/" | python -m json.tool | head -30
echo ""
echo ""

# Test 8: Retrieve property images collection
echo -e "${YELLOW}[TEST 8] GET /api/property-images/${NC}"
curl -s "$API_ROOT/property-images/" | python -m json.tool | head -30
echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "   API VALIDATION COMPLETED"
echo "==========================================${NC}"
echo ""
echo "Administrative Credentials:"
echo "  Account: $ADMIN_ACCOUNT"
echo "  Password: $ADMIN_CREDENTIAL"
echo ""
echo "Administrative Interface:"
echo "  http://localhost:8000/admin"
echo ""
echo "API Endpoint Documentation:"
