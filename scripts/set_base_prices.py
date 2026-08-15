#!/usr/bin/env python
"""
Set starting prices for services that have none (idempotent).
Only fills NULL base_price — never overwrites a price set in the dashboard.
"""

import os
import sys

import django

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)
os.chdir(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumithrakp_website.settings')
django.setup()

from main.models import Service

PRICES = {
    'cad-drafting-modeling': 15000,
    'cost-estimation-boq': 20000,
    'building-permit-drawings': 35000,
    '3d-rendering-visualization': 18000,
}

for slug, price in PRICES.items():
    updated = Service.objects.filter(slug=slug, base_price__isnull=True).update(base_price=price)
    state = f'set to ₹{price:,}' if updated else 'already priced — untouched'
    print(f'{slug}: {state}')
