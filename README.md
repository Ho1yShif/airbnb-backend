# AirBnB Backend - Property Rental Platform

[![Django CI/CD](https://github.com/Martin-Mawien/airbnb-backend/actions/workflows/django-ci-cd.yml/badge.svg)](https://github.com/Martin-Mawien/airbnb-backend/actions/workflows/django-ci-cd.yml)

Professional Django REST API for Airbnb-like property rental platform with comprehensive features for property management, bookings, payments, and reviews.

**Author:** Martin Mawien  
**GitHub:** https://github.com/Martin-Mawien/airbnb-backend  
**License:** MIT  
**Copyright © 2026 Martin Mawien**

---

## Live Demo

**API Base URL:** [https://airbnb-backend-api.onrender.com](https://airbnb-backend-api.onrender.com)  
**API Documentation:** [https://airbnb-backend-api.onrender.com/api/docs/](https://airbnb-backend-api.onrender.com/api/docs/)  
**Admin Panel:** [https://airbnb-backend-api.onrender.com/admin/](https://airbnb-backend-api.onrender.com/admin/)

**Test Credentials:**
- **Admin:** `admin` / `demo123`
- **Host:** `host_demo` / `demo123`
- **Guest:** `guest_demo` / `demo123`

---

## Features

✅ **User Management**
- Role-based access control (Guest, Host, Admin)
- User profiles with avatar support
- Authentication & authorization

✅ **Property Management**
- Create, read, update, delete properties
- Multiple images per property with primary image support
- Advanced filtering (location, price range)
- Property search functionality

✅ **Booking System**
- Create and manage bookings
- Date validation and conflict detection
- Booking status tracking (pending, confirmed, cancelled, completed)
- Automatic price calculation based on duration

✅ **Payment Processing**
- Secure payment handling
- Multiple payment status tracking
- Transaction ID management
- Payment history

✅ **Review & Rating System**
- Rate properties (1-5 stars)
- Comment functionality
- Average rating calculation
- Prevent duplicate reviews per user

✅ **Wishlist Management**
- Create multiple wishlists
- Add/remove properties from wishlists
- View wishlist properties

✅ **Background Tasks**
- Celery integration for async operations
- Email notifications for bookings & payments
- Scheduled tasks for booking reminders

---

## Tech Stack

- **Framework:** Django 4.2+
- **API:** Django REST Framework 3.14+
- **Database:** PostgreSQL 15
- **Cache & Queue:** Redis 7
- **Background Tasks:** Celery 5.3+
- **Image Processing:** Pillow 10+
- **API Filtering:** django-filter 23+
- **CORS:** django-cors-headers 4+
- **Server:** Gunicorn 21+

---

## Project Structure

```
airbnb-backend/
├── airbnb/                    # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI application
│   ├── asgi.py               # ASGI application
│   └── celery.py             # Celery configuration
├── listings/                 # Main application
│   ├── models.py             # Database models
│   ├── views.py              # API viewsets
│   ├── serializers.py        # DRF serializers
│   ├── permissions.py        # Custom permissions
│   ├── urls.py               # App URL routing
│   ├── admin.py              # Admin configuration
│   ├── tasks.py              # Celery tasks
│   └── migrations/           # Database migrations
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (optional)

### Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Martin-Mawien/airbnb-backend.git
cd airbnb-backend
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=airbnb
DB_USER=airbnb_user
DB_PASSWORD=airbnb_pass
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

5. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Run development server:**
```bash
python manage.py runserver
```

### Docker Setup

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user

### User Profiles
- `GET /api/user-profiles/` - List all profiles (admin only)
- `GET /api/user-profiles/me/` - Get current user profile
- `GET /api/user-profiles/{id}/` - Get user profile
- `PUT /api/user-profiles/{id}/` - Update user profile
- `DELETE /api/user-profiles/{id}/` - Delete user profile

### Properties
- `GET /api/properties/` - List all properties
- `POST /api/properties/` - Create property (authenticated)
- `GET /api/properties/{id}/` - Get property details
- `PUT /api/properties/{id}/` - Update property (owner only)
- `DELETE /api/properties/{id}/` - Delete property (owner only)
- `GET /api/properties/my_properties/` - Get current user's properties
- `GET /api/properties/{id}/availability/` - Check availability

### Bookings
- `GET /api/bookings/` - List bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking
- `POST /api/bookings/{id}/confirm/` - Confirm booking (host only)
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `GET /api/bookings/my_bookings/` - Get user's bookings

### Payments
- `GET /api/payments/` - List payments
- `POST /api/payments/` - Create payment
- `GET /api/payments/{id}/` - Get payment details
- `POST /api/payments/{id}/process/` - Process payment

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review
- `GET /api/reviews/{id}/` - Get review
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review
- `GET /api/reviews/my_reviews/` - Get user's reviews

### Wishlists
- `GET /api/wishlists/` - List user's wishlists
- `POST /api/wishlists/` - Create wishlist
- `GET /api/wishlists/{id}/` - Get wishlist
- `PUT /api/wishlists/{id}/` - Update wishlist
- `DELETE /api/wishlists/{id}/` - Delete wishlist
- `POST /api/wishlists/{id}/add_property/` - Add property to wishlist
- `POST /api/wishlists/{id}/remove_property/` - Remove property from wishlist

---

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