"""
WSGI config for cPanel deployment using Phusion Passenger.
This file is required for deploying Django on cPanel with Python apps support.
"""

import os
import sys

# Add your project directory to the sys.path
project_home = '/home/meenvstf/public_html/sumithrakp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'sumithrakp_website.settings'

# Import and configure Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()