# AirBnB Backend - Quick Start Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.12+
- Git

## Quick Setup (< 5 minutes)

### 1. Start Containers
```bash
cd airbnb-backend
docker-compose up -d
```

### 2. Run Migrations & Setup (Steps 1-5)
```bash
docker-compose exec web python /app/full_setup.py
```

This single command:
✅ Verifies all database migrations
✅ Creates admin superuser
✅ Creates test fixtures (users, properties, bookings)
✅ Configures Django admin
✅ Tests all API relationships

### 3. Access Services

**Django Admin:**
- URL: http://localhost:8000/admin
- Username: `admin`
- Password: `admin123456`

**Database:**
- Host: localhost:5432
- Database: airbnb
- User: airbnb_user
- Password: airbnb_pass

**Redis:**
- Host: localhost:6379

## Development Commands

### Start Web Server
```bash
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

### Create Migrations
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Run Tests
```bash
docker-compose exec web python manage.py test listings
```

### Create Superuser (Additional)
```bash
docker-compose exec web python manage.py createsuperuser
```

### Access Django Shell
```bash
docker-compose exec web python manage.py shell
```

## Project Structure

```
airbnb-backend/
├── airbnb/              # Main project settings
│   ├── settings.py      # Django configuration
│   ├── urls.py         # URL routing
│   ├── asgi.py         # ASGI config
│   └── wsgi.py         # WSGI config
├── listings/           # Main app
│   ├── models.py       # Database models
│   ├── views.py        # API views (to be created)
│   ├── serializers.py  # DRF serializers (to be created)
│   ├── urls.py         # App URLs
│   ├── admin.py        # Admin config
│   └── migrations/     # Database migrations
├── docker-compose.yml  # Docker configuration
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## Models & Relationships

### User
- `OneToOneField` → UserProfile
- `ForeignKey` → Property (as owner)
- `ForeignKey` → Booking (as guest)
- `ForeignKey` → Review (as reviewer)
- `ForeignKey` → Wishlist

### Property
- `ForeignKey` → User (owner)
- `ForeignKey` ← Booking
- `ForeignKey` ← Review
- `ForeignKey` ← PropertyImage

### Booking
- `ForeignKey` → User (guest)
- `ForeignKey` → Property
- `OneToOneField` ← Payment
- `ForeignKey` ← Review

### Payment
- `OneToOneField` → Booking

### Review
- `ForeignKey` → User
- `ForeignKey` → Property
- `ForeignKey` → Booking

### Wishlist
- `ForeignKey` → User
- `ManyToManyField` → Property

## Test Data

After running `full_setup.py`, you have:

**Users:**
- admin / admin123456 (superuser)
- testhost / testpass123 (property owner)
- testguest / testpass123 (property guest)
- admin_user / admin123456 (admin role)

**Properties:**
- Beautiful Beach House - Miami ($150/night)
- Modern Downtown Loft - New York ($200/night)
- Mountain Cabin Retreat - Aspen ($180/night)

**Bookings:**
- testguest booking Beautiful Beach House for 7 nights
- Payment created automatically

## Common Issues & Solutions

### Issue: "No module named 'corsheaders'"
**Solution**: Already fixed! Requirements installed in Docker

### Issue: Database connection refused
**Solution**: 
```bash
docker-compose restart db
# Wait 30 seconds
docker-compose exec db psql -U airbnb_user -d airbnb -c "\dt"
```

### Issue: Migrations not applied
**Solution**:
```bash
docker-compose exec web python manage.py migrate --verbosity=2
```

## Next Steps

1. ✅ **Database Setup** - DONE
2. ⏳ **Create API Serializers** - In `listings/serializers.py`
3. ⏳ **Create API Views** - In `listings/views.py`
4. ⏳ **Add URL Routing** - In `listings/urls.py`
5. ⏳ **Write Unit Tests** - In `listings/test_*.py`
6. ⏳ **Deploy** - To production

## Support

For detailed setup information, see: `SETUP_COMPLETE.md`
For model documentation, see: `listings/models.py`
