# Property Rental Platform Backend

Enterprise-grade REST API for managing property rentals, reservations, and guest interactions.

## Overview

A production-ready Django application providing comprehensive property management capabilities including listing management, reservation processing, payment tracking, and guest feedback systems.

## Core Capabilities

**Account Management**
- Multi-tier access control
- Profile customization
- Secure authentication

**Listing Operations**
- Property catalog management
- Multi-image support with primary designation
- Advanced search and filtering
- Location-based queries

**Reservation Engine**
- Real-time availability checking
- Automated conflict resolution
- Dynamic pricing calculation
- State management workflow

**Transaction Processing**
- Payment status monitoring
- Transaction audit trails
- Financial reporting

**Feedback System**
- Rating aggregation
- Comment moderation
- Duplicate prevention
- Statistical analysis

**Collections**
- Personalized property lists
- Batch operations
- Organization tools

**Asynchronous Processing**
- Background job execution
- Notification delivery
- Scheduled maintenance tasks

## Technology Foundation

- Django 4.2+ with REST Framework 3.14+
- PostgreSQL 15 (Primary datastore)
- Redis 7 (Caching and queue backend)
- Celery 5.3+ (Task orchestration)
- Pillow 10+ (Image manipulation)
- Gunicorn 21+ (Production server)

## Architecture

```
airbnb-backend/
├── airbnb/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── listings/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── urls.py
│   ├── admin.py
│   ├── tasks.py
│   └── migrations/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

## Setup Instructions

### System Requirements
- Python 3.8 or higher
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Development Environment

**1. Repository Setup**
```bash
git clone <repository-url>
cd airbnb-backend
```

**2. Python Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Environment Configuration**

Create `.env`:
```env
SECRET_KEY=<generate-unique-key>
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=airbnb
DB_USER=airbnb_user
DB_PASSWORD=<secure-password>
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

**4. Database Initialization**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**5. Start Server**
```bash
python manage.py runserver
```

### Container Deployment

**Using Docker Compose:**
```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## API Reference

### Account Operations
- `POST /api/account-auth/create_account/` - New account registration
- `POST /api/account-auth/authenticate/` - Login
- `POST /api/account-auth/terminate_session/` - Logout

### Profile Management
- `GET /api/profiles/` - Profile directory
- `GET /api/profiles/current_profile/` - Active user profile
- `GET /api/profiles/{id}/` - Specific profile details
- `PUT /api/profiles/{id}/` - Update profile
- `DELETE /api/profiles/{id}/` - Remove profile

### Listing Catalog
- `GET /api/listings/` - Browse available listings
- `POST /api/listings/` - Create listing (authenticated)
- `GET /api/listings/{id}/` - Retrieve listing details
- `PUT /api/listings/{id}/` - Modify listing (owner)
- `DELETE /api/listings/{id}/` - Remove listing (owner)
- `GET /api/listings/owner_listings/` - Owner's property portfolio

### Image Management
- `GET /api/photos/` - Image inventory
- `POST /api/photos/` - Upload property image
- `GET /api/photos/{id}/` - Image metadata
- `PUT /api/photos/{id}/` - Update image attributes
- `DELETE /api/photos/{id}/` - Delete image

### Reservation Management
- `GET /api/reservations/` - Reservation directory
- `POST /api/reservations/` - Create reservation
- `GET /api/reservations/{id}/` - Reservation details
- `PUT /api/reservations/{id}/` - Modify reservation
- `DELETE /api/reservations/{id}/` - Cancel reservation
- `POST /api/reservations/{id}/approve_reservation/` - Approve (owner)
- `POST /api/reservations/{id}/cancel_reservation/` - Cancel (owner)

### Transaction Tracking
- `GET /api/transactions/` - Transaction history
- `POST /api/transactions/` - Record transaction
- `GET /api/transactions/{id}/` - Transaction details
- `PUT /api/transactions/{id}/` - Update transaction status

### Feedback System
- `GET /api/feedback/` - Browse reviews
- `POST /api/feedback/` - Submit review
- `GET /api/feedback/{id}/` - Review details
- `PUT /api/feedback/{id}/` - Edit review
- `DELETE /api/feedback/{id}/` - Remove review

### Collection Management
- `GET /api/saved-collections/` - User collections
- `POST /api/saved-collections/` - Create collection
- `GET /api/saved-collections/{id}/` - Collection details
- `PUT /api/saved-collections/{id}/` - Update collection
- `DELETE /api/saved-collections/{id}/` - Delete collection
- `POST /api/saved-collections/{id}/add_to_list/` - Add property
- `POST /api/saved-collections/{id}/remove_from_list/` - Remove property

### Location Registry
- `GET /api/locations/` - Address directory
- `POST /api/locations/` - Add address
- `GET /api/locations/{id}/` - Address details
- `PUT /api/locations/{id}/` - Update address
- `DELETE /api/locations/{id}/` - Remove address

### User Preferences
- `GET /api/user-preferences/` - Preference list
- `POST /api/user-preferences/` - Set preferences
- `GET /api/user-preferences/current_preferences/` - Active settings
- `PUT /api/user-preferences/{id}/` - Update settings

## Query Parameters

**Filtering:**
- `?listing_status=available` - Filter by availability
- `?nightly_rate__gte=100&nightly_rate__lte=500` - Price range
- `?city_name=Paris` - Location filtering
- `?reservation_state=approved` - Status filtering

**Pagination:**
- `?page=2&page_size=20` - Control result sets

**Ordering:**
- `?ordering=-registration_date` - Sort by date descending
- `?ordering=nightly_rate` - Sort by price ascending

## Security

**Authentication:** Token-based (Django REST Framework)
**Authorization:** Role-based access control
**CORS:** Configurable origin whitelist
**HTTPS:** Enforced in production
**Session Security:** Secure cookie settings
**File Uploads:** Type and size validation
**Password:** Enhanced strength validation

## Performance Optimization

- Database query optimization via select_related/prefetch_related
- Redis caching for frequently accessed data
- Asynchronous task processing with Celery
- Connection pooling
- Static file compression
- Image optimization pipeline

## Monitoring & Logging

Comprehensive logging configured for:
- Application errors
- Security events
- Database queries
- API requests
- Background tasks

## Production Deployment

**Environment Variables:**
- `DEBUG=0`
- `ALLOWED_HOSTS` - Comma-separated domain list
- `SECRET_KEY` - Unique 50+ character string
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CORS_ALLOWED_ORIGINS` - Comma-separated frontend URLs

**Static Files:**
```bash
python manage.py collectstatic --noinput
```

**Process Manager:**
```bash
gunicorn airbnb.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Background Workers:**
```bash
celery -A airbnb worker --loglevel=info
celery -A airbnb beat --loglevel=info
```

## Database Schema

**Core Models:**
- UserProfile (Account attributes)
- Property (Listing inventory)
- PropertyImage (Media assets)
- Booking (Reservation records)
- Payment (Financial transactions)
- Review (Guest feedback)
- Wishlist (User collections)
- Address (Location data)
- CustomerPreferences (User settings)

## Testing

```bash
python manage.py test
python manage.py test listings
python manage.py test listings.tests.test_models
```

## License

Proprietary - All rights reserved

## Database Models

### UserProfile
- Extended user information
- Role-based access (Guest, Host, Admin)
- Avatar support

### Property
- Property listings
- Owner, title, location, price
- Multiple images support
- Status tracking

### PropertyImage
- Property images
- Primary image marking
- Image metadata

### Booking
- User bookings for properties
- Date validation
- Status tracking
- Automatic price calculation

### Payment
- Payment tracking
- Multiple payment statuses
- Transaction ID support

### Review
- Property reviews and ratings
- Comment functionality
- User and property association

### Wishlist
- User wishlists
- Multiple properties per wishlist
- Wishlist naming

---

## Authentication & Permissions

- **IsAuthenticated** - User must be logged in
- **IsAuthenticatedOrReadOnly** - Read for everyone, write for authenticated
- **IsOwnerOrReadOnly** - Only object owner can edit
- **IsHostOrReadOnly** - Only hosts and admins can create properties
- **IsBookingOwner** - Only booking/property owner can access

---

## Testing

Run tests with pytest:

```bash
pytest
pytest -v                    # Verbose output
pytest listings/test_*.py    # Run specific tests
pytest --cov=listings       # Coverage report
```

---

## Production Deployment

1. **Set environment variables:**
```bash
SECRET_KEY=<generate-new-key>
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **Run migrations:**
```bash
python manage.py migrate
```

3. **Collect static files:**
```bash
python manage.py collectstatic --no-input
```

4. **Start with Gunicorn:**
```bash
gunicorn airbnb.wsgi:application --bind 0.0.0.0:8000
```

---

## Development Guidelines

### Code Style
- Follow PEP 8
- Use meaningful variable/function names
- Add docstrings to all functions/classes

### Git Workflow
1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Push to origin: `git push origin feature/your-feature`
4. Create Pull Request

### Database Changes
Always create migrations for model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Troubleshooting

**Issue:** Port 8000 already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Issue:** Database connection error
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Verify database exists
psql -l
```

**Issue:** Redis connection error
```bash
# Check Redis service
redis-cli ping  # Should respond with PONG
```

---

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: martin@example.com
- Discord/Slack: [Your community channel]

---

## License

MIT License - See LICENSE file for details

**Copyright © 2026 Martin Mawien**
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = f'Booking Confirmation - {booking.property.title}'
        message = f"""
        Dear {booking.user.username},
        
        Your booking has been confirmed!
        
        Property: {booking.property.title}
        Check-in: {booking.check_in_date}
        Check-out: {booking.check_out_date}
        Total Price: ${booking.total_price}
        
        Thank you for using our platform!
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return f"Email sent to {booking.user.email}"
    except Booking.DoesNotExist:
        return f"Booking {booking_id} not found"


@shared_task
def send_payment_confirmation_email(payment_id):
    """Send payment confirmation email"""
    try:
        payment = Payment.objects.get(id=payment_id)
        subject = 'Payment Confirmation'
        message = f"""
        Dear {payment.booking.user.username},
        
        Your payment has been processed successfully!
        
        Transaction ID: {payment.transaction_id}
        Amount: ${payment.amount}
        Payment Method: {payment.get_payment_method_display()}
        
        Thank you!
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [payment.booking.user.email],
            fail_silently=False,
        )
        return f"Payment confirmation sent to {payment.booking.user.email}"
    except Payment.DoesNotExist:
        return f"Payment {payment_id} not found"


@shared_task
def check_expired_bookings():
    """Mark completed bookings as completed"""
    today = datetime.date.today()
    expired_bookings = Booking.objects.filter(
        check_out_date__lt=today,
        status='confirmed'
    )
    
    count = expired_bookings.update(status='completed')
    return f"Marked {count} bookings as completed"


@shared_task
def send_reminder_emails():
    """Send reminder emails for upcoming bookings"""
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    upcoming_bookings = Booking.objects.filter(
        check_in_date=tomorrow,
        status='confirmed'
    )
    
    for booking in upcoming_bookings:
        subject = 'Reminder: Upcoming Booking Tomorrow'
        message = f"""
        Dear {booking.user.username},
        
        This is a reminder that your booking is tomorrow!
        
        Property: {booking.property.title}
        Check-in: {booking.check_in_date}
        Location: {booking.property.location}
        
        Have a great stay!
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=True,
        )
    
    return f"Sent {upcoming_bookings.count()} reminder emails"

