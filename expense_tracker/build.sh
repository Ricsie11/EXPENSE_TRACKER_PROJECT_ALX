#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Collect static files (safe even if you don't have any)
python manage.py collectstatic --noinput  

# Run database migrations
python manage.py migrate
