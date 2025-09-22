#!/bin/bash

# Deployment script for cPanel
# This script runs after git pull to update the application

echo "Starting deployment..."

# Navigate to application directory
cd /home/meenvstf/public_html/sumithrakp

# Pull latest changes from GitHub
echo "Pulling latest changes..."
git pull origin main

# Activate virtual environment (if using one)
source venv/bin/activate 2>/dev/null || true

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Restart the application (for Passenger)
echo "Restarting application..."
touch passenger_wsgi.py

# Clear any cache
echo "Clearing cache..."
python manage.py clear_cache 2>/dev/null || true

echo "Deployment completed successfully!"
echo "Time: $(date)"

# Optional: Send notification
# curl -X POST https://your-webhook-url.com/notify -d "status=deployed"