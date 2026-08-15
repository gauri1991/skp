#!/usr/bin/env python
"""
WSGI config for cPanel deployment using Phusion Passenger.
This file is required for deploying Django on cPanel with Python apps support.
"""

import os
import sys

# Project root is wherever this file lives (works on any host/username)
project_home = os.path.dirname(os.path.abspath(__file__))

# Add project to Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to project directory
os.chdir(project_home)

# Set Django settings module (override via env var in the cPanel Python App UI)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_production')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
