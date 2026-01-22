# Monitoring & Observability Guide

## Overview

Your AirBnB backend includes comprehensive monitoring and observability features:

- **Sentry** - Error tracking and crash reporting
- **Health Checks** - Kubernetes-compatible liveness & readiness probes
- **Performance Monitoring** - Request/response tracking with slow request alerts
- **Metrics** - Prometheus-compatible metrics endpoint
- **Structured Logging** - Rotating file logs with configurable levels

## Health Check Endpoints

### 1. Overall Health Status
```bash
curl http://localhost:8000/health/
```

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "database": { "status": "ok" },
    "cache": { "status": "ok" },
    "celery": { "status": "ok" }
  }
}
```

Possible statuses:
- `healthy` - All critical systems operational
- `degraded` - Some non-critical systems down
- `unhealthy` - Critical systems down (HTTP 503)

### 2. Liveness Probe (Kubernetes)
```bash
curl http://localhost:8000/health/live/
```

Returns HTTP 200 if the application process is running. Used by Kubernetes to determine if the container should be restarted.

### 3. Readiness Probe (Kubernetes)
```bash
curl http://localhost:8000/health/ready/
```

Returns HTTP 200 only when the application is ready to serve traffic. Checks:
- Database connectivity
- Cache availability

Used by Kubernetes to determine if traffic should be routed to this instance.

### 4. Prometheus Metrics
```bash
curl http://localhost:8000/metrics/
```

Returns application metrics in Prometheus text format:

```
# HELP airbnb_users_total Total number of users
# TYPE airbnb_users_total gauge
airbnb_users_total 45

# HELP airbnb_properties_total Total number of properties
# TYPE airbnb_properties_total gauge
airbnb_properties_total 120

# HELP airbnb_bookings_total Total number of bookings
# TYPE airbnb_bookings_total gauge
airbnb_bookings_total 356
```

## Sentry Integration (Error Tracking)

### Setup

1. **Create a Sentry account:**
   - Go to https://sentry.io/
   - Sign up and create a new project
   - Select "Django" as platform
   - Copy your DSN

2. **Configure environment variable:**
   ```bash
   # In .env or Render dashboard
   SENTRY_DSN=https://your-key@sentry.io/project-id
   SENTRY_ENVIRONMENT=production
   SENTRY_RELEASE=1.0.0
   ```

3. **Install Sentry SDK:**
   ```bash
   pip install sentry-sdk
   ```

### How It Works

All unhandled exceptions are automatically captured and sent to Sentry:

- **Error tracking** - Stack traces with context
- **Release tracking** - Which version had the error
- **Environment** - Production/staging/dev
- **User context** - Who experienced the error
- **Breadcrumbs** - Action trail leading to error
- **Performance** - Transaction timing data

### Testing Sentry Integration

```bash
# Test error capture
curl -X GET http://localhost:8000/api/properties/invalid-id/
```

This will generate an error that Sentry captures automatically.

## Application Logging

### Log Files

Logs are stored in the `logs/` directory with automatic rotation:

```
logs/
├── django.log      # Application logs (errors + warnings)
├── celery.log      # Background task logs
└── ...
```

### Log Levels

Configure in `.env`:
```bash
LOG_LEVEL=INFO
```

Levels (lowest to highest verbosity):
- `CRITICAL` - Critical errors
- `ERROR` - Errors
- `WARNING` - Warnings (default in production)
- `INFO` - General information
- `DEBUG` - Detailed debugging info

### Log Format

```
INFO 2026-01-20 14:23:45,123 views 1234 5678 Request: GET /api/listings/ duration 0.045s, 3 queries, status 200
```

Format: `LEVEL TIMESTAMP MODULE PID THREAD MESSAGE`

### Custom Logging

```python
import logging

logger = logging.getLogger(__name__)

# In your views/functions
logger.info('User logged in', extra={'user_id': request.user.id})
logger.warning('Slow operation detected', extra={'duration': 2.5})
logger.error('Payment processing failed', exc_info=True)
```

## Performance Monitoring

### Slow Request Alerts

Requests taking longer than 1 second are logged with details:

```
WARNING Slow request: POST /api/reservations/ took 1.23s, 12 queries, status 201
```

### Response Headers

Every response includes performance metrics:

```
X-Response-Time: 0.045s
X-DB-Queries: 3
```

### Optimizing Performance

Track slow endpoints using logs:

```bash
# Find slow requests
grep "Slow request" logs/django.log
```

## Docker Compose Monitoring

### Health Checks in Docker

All services have health checks defined:

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Monitor Container Health

```bash
docker-compose ps
```

Shows health status of each container.

## Kubernetes Deployment

### Liveness Probe Configuration

```yaml
livenessProbe:
  httpGet:
    path: /health/live/
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe Configuration

```yaml
readinessProbe:
  httpGet:
    path: /health/ready/
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Render Deployment Monitoring

### Enable Sentry

1. In Render Dashboard → Environment:
   ```
   SENTRY_DSN=https://your-key@sentry.io/project-id
   SENTRY_ENVIRONMENT=production
   ```

2. Errors in production automatically sent to Sentry

### View Health Status

```bash
# Check production health
curl https://your-app.onrender.com/health/
curl https://your-app.onrender.com/metrics/
```

## Best Practices

1. **Sentry**: Set release version on each deployment
   ```bash
   SENTRY_RELEASE=$(git rev-parse --short HEAD)
   ```

2. **Logging**: Use structured logging with context
   ```python
   logger.info('Operation completed', extra={
       'user_id': user.id,
       'duration_ms': elapsed_time,
       'status': 'success'
   })
   ```

3. **Performance**: Monitor trends in slow requests
   ```bash
   grep "Slow request" logs/django.log | wc -l
   ```

4. **Metrics**: Scrape metrics regularly with Prometheus
   ```
   http://localhost:8000/metrics/
   ```

## Troubleshooting

### Sentry Not Receiving Events

1. Check `SENTRY_DSN` is set correctly
2. Verify network connectivity to `sentry.io`
3. Check Sentry project settings for allowed domains

### Health Checks Failing

```bash
# Check specific components
curl http://localhost:8000/health/
```

Common issues:
- Database not accessible → Check DB credentials
- Cache not accessible → Check Redis/Cache config
- Celery not running → Start Celery worker

### Logs Not Appearing

1. Check log directory exists: `mkdir -p logs/`
2. Verify `LOG_LEVEL` in `.env`
3. Check file permissions: `chmod 755 logs/`

## Summary

Your application now has:

✅ Error tracking via Sentry
✅ Health checks for container orchestration
✅ Performance monitoring with slow request alerts
✅ Prometheus-compatible metrics
✅ Structured logging with rotation
✅ Development and production ready

Monitor your application in production using these endpoints and logs!
