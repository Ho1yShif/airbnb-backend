#!/bin/bash

# Configure database connection parameters
export DB_NAME=airbnb
export DB_USER=airbnb_user
export DB_PASSWORD=airbnb_pass
export DB_HOST=db
export DB_PORT=5432
export DJANGO_SETTINGS_MODULE=airbnb.settings
export DEBUG=1

# Await database service availability
echo "Initiating database readiness check..."
until pg_isready -h $DB_HOST -U $DB_USER -d $DB_NAME; do
  sleep 1
done
echo "Database service is available"

# Apply pending schema migrations
echo "Applying database schema migrations..."
python manage.py migrate

# Validate migration execution
if [ $? -eq 0 ]; then
    echo "✓ Schema migrations applied successfully"
    
    # Display schema objects
    echo "Schema object inventory:"
    python manage.py dbshell << EOF
\dt
\q
EOF
else
    echo "✗ Migration execution failed"
