#!/usr/bin/env bash
set -euo pipefail

# Create Python virtual environment for the project
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
python -m pip install --upgrade pip
pip install fastapi \
    uvicorn \
    sqlalchemy \
    jinja2 \
    python-multipart \
    "passlib[bcrypt]" \
    pytest \
    httpx \
    itsdangerous \
    psycopg2-binary

# # Install Docker if apt-get is available
# if command -v apt-get >/dev/null; then
#     sudo apt-get update
#     sudo apt-get install -y docker.io
# fi

# # Set database environment variables for PostgreSQL
# export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/testdb"
# export DATABASE_URL="$TEST_DATABASE_URL"
# echo "Configured DATABASE_URL=$DATABASE_URL"

# # Start a PostgreSQL container if Docker is available
# if command -v docker >/dev/null; then
#     if ! docker ps --format '{{.Names}}' | grep -q '^codex-postgres$'; then
#         echo "Starting PostgreSQL container..."
#         docker run --name codex-postgres -e POSTGRES_PASSWORD=postgres \
#             -e POSTGRES_DB=testdb -p 5432:5432 -d postgres:15
#     else
#         echo "PostgreSQL container already exists. Starting it."
#         docker start codex-postgres
#     fi
#     echo "Checking PostgreSQL status..."
#     docker exec codex-postgres pg_isready -U postgres
# else
#     echo "Docker not found; skipping PostgreSQL startup."
# fi

echo "Environment setup complete. Activate with 'source venv/bin/activate'"
