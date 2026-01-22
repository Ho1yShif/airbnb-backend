#!/bin/bash
set -e

echo "========================================"
echo "AIRBNB BACKEND - INITIALIZATION SCRIPT"
echo "========================================"

# Phase 1: Verify container orchestration
echo -e "\nPhase 1: Container status verification..."
docker-compose ps

# Phase 2: Database service readiness check
echo -e "\nPhase 2: Database service initialization..."
until docker-compose exec -T db pg_isready -U airbnb_user -d airbnb; do
  echo "Awaiting PostgreSQL readiness..."
  sleep 2
done
echo "✓ Database service is operational"

# Phase 3: Apply database schema migrations
echo -e "\nPhase 3: Schema migration application..."
docker-compose exec -T web python manage.py migrate --verbosity=2

# Phase 4: Display migration inventory
echo -e "\nPhase 4: Migration record review..."
docker-compose exec -T web python manage.py showmigrations

# Phase 5: Validate schema structure
echo -e "\nPhase 5: Database structure validation..."
docker-compose exec -T db psql -U airbnb_user -d airbnb << 'EOF'
\echo '=== Database Tables ==='
\dt
\echo ''
\echo '=== Migration History ==='
SELECT app, name, applied FROM django_migrations ORDER BY applied DESC LIMIT 10;
EOF

echo -e "\n========================================"
echo "✓ INITIALIZATION COMPLETED"
echo "========================================"
echo ""
echo "To start the application:"
echo "  docker-compose up web"
echo ""
echo "Access administrative interface:"
