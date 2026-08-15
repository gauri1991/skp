#!/usr/bin/env python
"""
Script to create Django superuser for production deployment
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_production')

# Change to the project directory (wherever this script lives)
project_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_path)

# Setup Django
django.setup()

from django.contrib.auth.models import User

# Superuser credentials
username = 'admin'
email = 'admin@sumithrakp.com'
password = 'Sumi#420'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔐 Password: {password}")
        print(f"🌐 Admin URL: https://sumithrakp.com/admin/")
    else:
        print(f"⚠️  Superuser '{username}' already exists.")
        print(f"🌐 Admin URL: https://sumithrakp.com/admin/")
        
except Exception as e:
    print(f"❌ Error creating superuser: {e}")
    
print("\n🎉 Script completed!")