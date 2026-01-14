#!/bin/bash
# Usage: ./convert_and_load.sh input.sql postgres_user postgres_db postgres_password
# Converts MySQL SQL to PostgreSQL and loads it into the running Docker Compose db service

set -e

MYSQL_SQL="$1"
PG_USER="$2"
PG_DB="$3"
PG_PASS="$4"

if [ ! -f "$MYSQL_SQL" ]; then
  echo "Input SQL file not found: $MYSQL_SQL"
  exit 1
fi


# Step 1: Convert and load MySQL SQL to PostgreSQL using pgloader
if command -v pgloader >/dev/null 2>&1; then
  echo "Using pgloader for conversion and loading..."
  pgloader "$MYSQL_SQL" postgresql://$PG_USER:$PG_PASS@db/$PG_DB
  echo "Conversion and load complete via pgloader."
else
  echo "pgloader is not installed. Please install pgloader (https://pgloader.io/download.html) and try again."
  exit 1
fi
