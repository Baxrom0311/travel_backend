#!/usr/bin/env bash
# Render.com build script
set -o errexit

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 Installing dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📄 Collecting static files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python manage.py collectstatic --no-input

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🗄️  Running migrations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python manage.py migrate --no-input

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌱 Seeding initial data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
# Faqat birinchi deploy'da yuklaymiz (agar Hotel table bo'sh bo'lsa)
python manage.py shell -c "
from hotels.models import Hotel
from attractions.models import Attraction
from events.models import Event
from news.models import News
from restaurants.models import Restaurant, Cuisine
from tours.models import Tour

import os
from django.core.management import call_command

# Initial JSON fixtures
if Hotel.objects.count() == 0 and os.path.exists('initial_data.json'):
    try:
        call_command('loaddata', 'initial_data.json')
        print('  ✅ Initial fixtures loaded')
    except Exception as e:
        print(f'  ⚠️  Fixtures skipped: {e}')

# Attraction images (media'dan yuklaydi)
if Attraction.objects.filter(images__isnull=False).count() == 0:
    try:
        call_command('seed_attraction_images')
        print('  ✅ Attraction images loaded')
    except Exception as e:
        print(f'  ⚠️  Attraction images skipped: {e}')

# Events va News demo data
if Event.objects.count() == 0:
    try:
        call_command('seed_demo_data')
        print('  ✅ Events/News demo loaded')
    except Exception as e:
        print(f'  ⚠️  Demo data skipped: {e}')

# Restaurants va Tours
if Restaurant.objects.count() == 0 or Tour.objects.count() == 0:
    try:
        call_command('seed_extras')
        print('  ✅ Restaurants/Tours loaded')
    except Exception as e:
        print(f'  ⚠️  Extras skipped: {e}')

# Superuser yaratish
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    User.objects.create_superuser(email='admin@visitkhorezm.uz', password=admin_password, first_name='Admin')
    print(f'  ✅ Superuser admin created')
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Build complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
