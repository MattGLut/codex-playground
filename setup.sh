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

# Install Docker if apt-get is available
if command -v apt-get >/dev/null; then
    sudo apt-get update
    sudo apt-get install -y docker.io
fi

echo "Environment setup complete. Activate with 'source venv/bin/activate'"
