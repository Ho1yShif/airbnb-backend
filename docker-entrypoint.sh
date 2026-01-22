#!/bin/bash
set -e

# Initialize database service connectivity verification
echo "Initiating database service availability check..."
until pg_isready -h ${DB_HOST:-db} -U ${DB_USER:-airbnb_user} -d ${DB_NAME:-airbnb}; do
  sleep 1
done
echo "✓ Database service operational"

# Execute pending schema migrations
echo "Applying database schema migrations..."
python manage.py migrate --verbosity=2

# Display migration execution summary
python manage.py showmigrations

# Enumerate schema objects
echo "Schema object inventory:"
psql -h ${DB_HOST:-db} -U ${DB_USER:-airbnb_user} -d ${DB_NAME:-airbnb} -c "\dt"

echo "✓ Schema initialization completed successfully"
