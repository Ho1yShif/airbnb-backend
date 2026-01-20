

# Professional Dockerfile for Django + PostgreSQL
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

# Install PostgreSQL client only
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

