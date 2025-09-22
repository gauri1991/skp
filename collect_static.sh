#!/bin/bash

# Script to collect static files for production deployment

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Static files collected successfully!"
echo "Location: staticfiles/"