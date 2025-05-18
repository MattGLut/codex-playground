#!/usr/bin/env bash
set -euo pipefail
# Print each command before executing to aid debugging
set -x

echo "Starting environment setup..."

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip
echo "Installing Python dependencies..."
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

# SQLite is used by default. Docker installation is disabled.
# If you need PostgreSQL, install Docker manually and configure
# the DATABASE_URL environment variable.
#
# The lines below were previously used to automatically install
# Docker and run a PostgreSQL container. They are left commented
# out for reference.
#
# echo "Checking for apt-get to install Docker..."
# if command -v apt-get >/dev/null; then
#     echo "Removing any apt.llvm.org sources..."
#     ./remove_llvm_source.sh
#     echo "Running apt-get update..."
#     sudo apt-get update
#     echo "Installing docker.io via apt-get..."
#     sudo apt-get install -y docker.io
# else
#     echo "apt-get not found; skipping Docker installation."
# fi

# # Set database environment variables for PostgreSQL
# echo "Configuring PostgreSQL environment variables..."
# export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/testdb"
# export DATABASE_URL="$TEST_DATABASE_URL"
# echo "Configured DATABASE_URL=$DATABASE_URL"

# # Start a PostgreSQL container if Docker is available
# echo "Checking for Docker to manage PostgreSQL..."
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
