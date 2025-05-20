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

# AI dependencies
pip install torch \
    transformers \
    diffusers \
    Pillow


# SQLite is used by default. Docker installation is disabled.

echo "Environment setup complete. Activate with 'source venv/bin/activate'"
