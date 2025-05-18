#!/usr/bin/env bash
set -euo pipefail

# Install PostgreSQL if available (may require sudo privileges)
if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y postgresql
    sudo service postgresql start
fi

# Create Python virtual environment for the project
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. Activate with 'source venv/bin/activate'"
