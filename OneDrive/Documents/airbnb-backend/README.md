# Airbnb Clone Backend

A scalable, production-ready backend solution for a property rental platform inspired by Airbnb. Built with Django REST Framework and PostgreSQL, featuring role-based access control, comprehensive API endpoints, and Docker support.

## 🚀 Features

- **User Management**: Registration, authentication, and role-based profiles (Guest, Host, Admin)
- **Property Management**: Full CRUD operations, image uploads, location-based search with filtering
- **Booking System**: Reservation management with status tracking and conflict prevention
- **Payment Processing**: Secure payment handling with comprehensive status tracking
- **Review System**: 5-star rating system with comments linked to verified bookings
- **Wishlist**: User-curated collections of favorite properties
- **Admin Dashboard**: Full-featured Django admin interface for content management
- **API Documentation**: RESTful API with browsable interface

## 🛠️ Technology Stack

- **Framework**: Django 4.2+ with Django REST Framework 3.14+
- **Database**: PostgreSQL 13+
- **Task Queue**: Celery with Redis backend
- **Authentication**: Django built-in authentication with role-based permissions
- **File Storage**: Local media files (AWS S3 ready)
- **Containerization**: Docker & Docker Compose
- **API Features**: Filtering, searching, pagination, and CORS support


## 📊 Database Models

### UserProfile
- Extends Django User model
- Fields: role (Guest/Host/Admin), phone_number, bio, profile_picture
- Automatic profile creation on user registration

### Property
- Fields: title, description, location, price_per_night, bedrooms, bathrooms, max_guests
- Status tracking: Available, Unavailable, Archived
- Owner relationship (Host users only)
- Average rating calculation from reviews

### PropertyImage
- Multiple images per property
- Image upload with caption support
- Primary image designation

### Booking
- Date range validation (check-in/check-out)
- Status: Pending, Confirmed, Cancelled, Completed
- Total price and nights calculation
- Conflict prevention logic

### Payment
- Linked to bookings
- Status: Pending, Completed, Failed, Refunded
- Payment date tracking
- Amount validation

### Review
- 1-5 star rating system
- Comment field for detailed feedback
- Linked to verified bookings
- One review per booking constraint

### Wishlist
- User-specific property collections
- Many-to-many relationship with properties
- Creation date tracking

## 🔌 API Endpoints

All endpoints are prefixed with `/api/`

### Authentication & Users
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/user-profiles/` - List user profiles
- `GET /api/user-profiles/{id}/` - Retrieve user profile
- `PUT /api/user-profiles/{id}/` - Update user profile

### Properties
- `GET /api/properties/` - List all properties (with filters)
- `POST /api/properties/` - Create property (Host only)
- `GET /api/properties/{id}/` - Retrieve property details
- `PUT /api/properties/{id}/` - Update property (Owner only)
- `DELETE /api/properties/{id}/` - Delete property (Owner only)
- `GET /api/properties/?location={city}` - Search by location
- `GET /api/properties/?min_price={amount}&max_price={amount}` - Filter by price

### Property Images
- `GET /api/property-images/` - List property images
- `POST /api/property-images/` - Upload property image
- `DELETE /api/property-images/{id}/` - Delete image (Owner only)

### Bookings
- `GET /api/bookings/` - List user bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Retrieve booking details
- `PUT /api/bookings/{id}/` - Update booking
- `POST /api/bookings/{id}/confirm/` - Confirm booking (Host only)
- `POST /api/bookings/{id}/cancel/` - Cancel booking

### Payments
- `GET /api/payments/` - List user payments
- `POST /api/payments/` - Create payment
- `GET /api/payments/{id}/` - Retrieve payment details

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review (verified bookings only)
- `GET /api/reviews/{id}/` - Retrieve review details
- `PUT /api/reviews/{id}/` - Update review (Owner only)
- `DELETE /api/reviews/{id}/` - Delete review (Owner only)

### Wishlists
- `GET /api/wishlists/` - List user wishlists
- `POST /api/wishlists/` - Create wishlist
- `POST /api/wishlists/{id}/add_property/` - Add property to wishlist
- `POST /api/wishlists/{id}/remove_property/` - Remove property from wishlist


## 🚀 Setup Instructions

### Option 1: Docker Setup (Recommended)

1. **Prerequisites**:
   - Docker and Docker Compose installed
   - Git installed

2. **Clone and Start**:
```bash
git clone https://github.com/Martin-Mawien/airbnb-backend.git
cd airbnb-backend
docker-compose up --build
```

3. **Access the Application**:
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - Default superuser: `admin` / `admin123`

### Option 2: Local Development Setup

1. **Clone Repository**:
```bash
git clone https://github.com/Martin-Mawien/airbnb-backend.git
cd airbnb-backend
```

2. **Create Virtual Environment**:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Database Setup**:
```bash
# Install PostgreSQL and create database
createdb airbnb_clone
createuser airbnb_user -P  # Password: airbnb_pass
psql -c "GRANT ALL PRIVILEGES ON DATABASE airbnb_clone TO airbnb_user;"
```

5. **Environment Configuration**:
Create a `.env` file in the project root:
```env
DB_NAME=airbnb_clone
DB_USER=airbnb_user
DB_PASSWORD=airbnb_pass
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

6. **Run Migrations**:
```bash
python manage.py migrate
```

7. **Create Superuser**:
```bash
python manage.py createsuperuser
```

8. **Start Development Server**:
```bash
python manage.py runserver
```

9. **Start Celery Worker** (in separate terminal):
```bash
celery -A airbnb worker -l info
```

10. **Run Tests**:
```bash
python manage.py test
```


## 🔒 Security Features

- Role-based access control (Guest, Host, Admin)
- Object-level permissions (users can only modify their own content)
- CORS configuration for cross-origin requests
- Environment-based secret key management
- SQL injection protection via Django ORM
- XSS protection with Django templates
- CSRF protection on state-changing operations

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test listings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

Test files:
- [listings/test_models.py](listings/test_models.py) - Model validation tests
- [listings/test_api.py](listings/test_api.py) - API endpoint tests

## 📁 Project Structure

```
airbnb-backend/
├── airbnb/                 # Django project configuration
│   ├── settings.py        # Main settings
│   ├── urls.py           # URL routing
│   ├── celery.py         # Celery configuration
│   └── wsgi.py           # WSGI configuration
├── listings/              # Main application
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── permissions.py    # Custom permissions
│   ├── tasks.py          # Celery tasks
│   └── tests.py          # Unit tests
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md            # This file
```


## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_NAME=airbnb_clone
DB_USER=airbnb_user
DB_PASSWORD=airbnb_pass
DB_HOST=localhost          # Use 'db' for Docker
DB_PORT=5432

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True                 # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery/Redis (optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### API Usage Examples

#### Authentication
```bash
# Register new user
POST /api/auth/register/
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}

# Login
POST /api/auth/login/
{
  "username": "john_doe",
  "password": "securepassword"
}
```

#### Property Management
```bash
# List all properties with filters
GET /api/properties/?location=New York&min_price=50&max_price=200

# Create new property (Host only)
POST /api/properties/
{
  "title": "Cozy Downtown Apartment",
  "description": "Beautiful 2BR apartment in city center",
  "location": "New York",
  "price_per_night": 120.00,
  "bedrooms": 2,
  "bathrooms": 1,
  "max_guests": 4
}
```

#### Booking Flow
```bash
# Create booking
POST /api/bookings/
{
  "property": 1,
  "check_in_date": "2026-02-15",
  "check_out_date": "2026-02-20"
}

# Confirm booking (Host only)
POST /api/bookings/5/confirm/
```

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Configure `SECRET_KEY` with strong random value
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use production database (managed PostgreSQL)
- [ ] Configure static/media file storage (AWS S3, Azure Blob)
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Enable rate limiting
- [ ] Review security settings

### Docker Deployment

```bash
# Build and run production containers
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
- Verify PostgreSQL is running: `pg_isready`
- Check `.env` credentials match your database user
- For Docker: ensure `DB_HOST=db`

**Migration Issues**
```bash
# Reset migrations (development only)
python manage.py migrate listings zero
python manage.py migrate
```

**Port Already in Use**
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

**Docker Issues**
```bash
# Rebuild containers
docker-compose down -v
docker-compose up --build
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors & Acknowledgments

### Project Lead
**Martin Mawien**  
- GitHub: [@Martin-Mawien](https://github.com/Martin-Mawien)
- Project: [airbnb-backend](https://github.com/Martin-Mawien/airbnb-backend)

### Acknowledgments

This project was developed as a comprehensive backend solution demonstrating best practices in Django REST Framework development. Special thanks to:

- **Django Software Foundation** - For the Django framework
- **Django REST Framework** - For excellent API development tools
- **PostgreSQL Community** - For the robust database system
- **Celery Project** - For distributed task queue system
- **GitHub Copilot** - For AI-assisted development support

### Educational Purpose

This project is designed for educational and portfolio purposes, showcasing:
- RESTful API design patterns
- Django ORM best practices
- Authentication and authorization systems
- Database modeling and relationships
- Docker containerization
- Test-driven development
- API documentation

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Martin-Mawien/airbnb-backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Martin-Mawien/airbnb-backend/discussions)
- **Email**: Contact via GitHub profile

## 🗺️ Roadmap

### Planned Features

- [ ] Email notifications for bookings
- [ ] Advanced search with Elasticsearch
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Real-time messaging between hosts and guests
- [ ] Property availability calendar
- [ ] Multi-language support
- [ ] Mobile API optimization
- [ ] GraphQL API endpoint
- [ ] Advanced analytics dashboard
- [ ] Automated backup system

### Recent Updates

- ✅ Role-based access control implementation
- ✅ Comprehensive test suite
- ✅ Docker containerization
- ✅ API filtering and search
- ✅ Image upload functionality
- ✅ Celery task queue integration

---

**Built with ❤️ using Django REST Framework**

*Last Updated: January 2026*

