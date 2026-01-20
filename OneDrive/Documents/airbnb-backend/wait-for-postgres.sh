#!/bin/sh
# PostgreSQL service availability verification script
set -e

db_host="$1"
shift

until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$db_host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  >&2 echo "Database service unavailable - waiting for readiness"
  sleep 1
done

>&2 echo "Database service is operational - executing target command"
