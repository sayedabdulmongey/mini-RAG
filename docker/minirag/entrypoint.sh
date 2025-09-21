#!/bin/bash
set -e 

echo "Starting database migrations..."
cd /app/models/db_schemas/miniRAG/
alembic upgrade head
echo "Database migrations completed."

cd /app


exec "$@"
