#!/bin/sh
set -e

echo "🔧 Migrations..."
python manage.py migrate --noinput

echo "👤 Superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
U = get_user_model()
if not U.objects.filter(is_superuser=True).exists():
    U.objects.create_superuser(email='admin@visitkhorezm.uz', password='admin123', first_name='Admin')
    print('Admin created')
else:
    print('Admin exists')
" || true

echo "🌱 Initial fixtures..."
python manage.py shell -c "
from hotels.models import Hotel
import os
if Hotel.objects.count() == 0 and os.path.exists('initial_data.json'):
    from django.core.management import call_command
    call_command('loaddata', 'initial_data.json')
    print('Loaded initial fixtures')
else:
    print('Fixtures already loaded or missing')
" || true

echo "🌱 Demo data (events, news)..."
python manage.py shell -c "
from events.models import Event
from django.core.management import call_command
if Event.objects.count() == 0:
    call_command('seed_demo_data')
" || true

echo "🌱 Restaurants & Tours..."
python manage.py shell -c "
from restaurants.models import Restaurant
from tours.models import Tour
from django.core.management import call_command
if Restaurant.objects.count() == 0 or Tour.objects.count() == 0:
    call_command('seed_extras')
" || true

echo "🌱 R2 image links (attractions, hotels)..."
python manage.py link_r2_images || true

echo "🌱 Testimonials..."
python manage.py seed_testimonials || true

echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 60
