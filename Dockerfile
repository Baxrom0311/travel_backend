FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Project code
COPY . .

# Static files yig'ish
RUN python manage.py collectstatic --noinput || echo "skip collectstatic at build (no DB)"

# Port (Northflank uchun)
EXPOSE 8000

# Migrations + seed + start (PostgreSQL ulansa)
CMD ["sh", "-c", "python manage.py migrate --noinput && (python manage.py shell -c 'from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(is_superuser=True).exists() or U.objects.create_superuser(email=\"admin@visitkhorezm.uz\", password=\"admin123\", first_name=\"Admin\")' || true) && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 60"]
