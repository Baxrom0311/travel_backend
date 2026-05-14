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

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Static files yig'ish
RUN python manage.py collectstatic --noinput || echo "skip collectstatic at build (no DB)"

# Port (Northflank uchun)
EXPOSE 8000

# Entrypoint - migrations + seeds + gunicorn
CMD ["/app/entrypoint.sh"]
