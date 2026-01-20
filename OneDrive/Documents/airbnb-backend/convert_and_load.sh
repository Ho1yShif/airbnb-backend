#!/bin/bash
# Database schema conversion and data loading utility
# Syntax: ./convert_and_load.sh <source_file> <postgres_user> <postgres_db> <postgres_password>
# Converts relational database schema to PostgreSQL format and loads data

set -e

MYSQL_SQL="$1"
PG_USER="$2"
PG_DB="$3"
PG_PASS="$4"

if [ ! -f "$MYSQL_SQL" ]; then
  echo "Source data file not found: $MYSQL_SQL"
  exit 1
fi


# Execute schema conversion and data migration
if command -v pgloader >/dev/null 2>&1; then
  echo "Initiating database conversion and migration pipeline..."
  pgloader "$MYSQL_SQL" postgresql://$PG_USER:$PG_PASS@db/$PG_DB
  echo "Data migration completed successfully"
else
  echo "Database migration tool not available. Install pgloader from: https://pgloader.io/"
fi
