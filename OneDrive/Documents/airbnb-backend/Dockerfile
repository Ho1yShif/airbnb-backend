FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "airbnb.wsgi:application", "--bind", "0.0.0.0:8000"]

# Dockerfile for Django + PostgreSQL + Celery + Redis
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (uncomment if using staticfiles)
# RUN python manage.py collectstatic --noinput

# Healthcheck (optional, for Docker Compose)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["gunicorn", "airbnb.wsgi:application", "--bind", "0.0.0.0:8000"]
