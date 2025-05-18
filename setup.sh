#!/usr/bin/env bash
set -euo pipefail

# Create Python virtual environment for the project
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. Activate with 'source venv/bin/activate'"
