# Airbnb Clone Backend

A scalable, secure backend solution for a property rental platform inspired by Airbnb. Built with Django, Django REST Framework, PostgreSQL, GraphQL, Celery, and Redis.

## Features

- **User Management**: Registration, authentication, profiles with roles (Guest, Host, Admin)
- **Property Management**: Listing creation, image uploads, location-based search
- **Booking System**: Reservation management with status tracking
- **Payment Processing**: Secure payment handling with status tracking
- **Review System**: 1-5 star ratings and comments for properties
- **Wishlist**: User favorite property collections
- **REST API**: Full CRUD operations with filtering and search
- **GraphQL API**: Flexible querying capabilities
- **Admin Dashboard**: Django admin for content management
- **Asynchronous Tasks**: Celery for background processing
- **Caching**: Redis for performance optimization

## Technology Stack

- **Backend**: Django 6.0, Django REST Framework
- **Database**: PostgreSQL
- **GraphQL**: Graphene-Django
- **Task Queue**: Celery with Redis
- **Authentication**: Session-based with REST Framework
- **File Storage**: Local media files (configurable for cloud)
- **Containerization**: Docker-ready

## Models

### UserProfile
- Extends Django User with role, phone, bio, avatar

### Property
- Title, location, price, owner, description, status

### Booking
- User, property, check-in/out dates, status

### Payment
- Booking reference, amount, status, payment date

### Review
- User, property, booking, rating (1-5), comment

### Wishlist
- User collections of favorite properties

## API Endpoints

### REST API (`/api/`)
- `GET/POST /api/user-profiles/` - User profiles
- `GET/POST /api/properties/` - Properties
- `GET/POST /api/bookings/` - Bookings
- `GET/POST /api/payments/` - Payments
- `GET/POST /api/reviews/` - Reviews
- `GET/POST /api/wishlists/` - Wishlists
- `GET/POST /api/property-images/` - Property images

### GraphQL API (`/graphql/`)
- Flexible querying of all entities
- GraphiQL interface for testing

## Setup Instructions

1. **Clone and Install Dependencies**:
```bash
git clone https://github.com/martin-mawien/airbnb-clone-project.git
cd airbnb-clone-project
pip install -r requirements.txt
```

2. **Database Setup**:
   - Install PostgreSQL
   - Create database: `airbnb_clone`
   - Update `.env` with database credentials

3. **Redis Setup**:
   - Install Redis server
   - Ensure running on default port 6379

4. **Run Migrations**:
```bash
python manage.py migrate
```

5. **Create Superuser**:
```bash
python manage.py createsuperuser
```

6. **Start Services**:
```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A airbnb worker --loglevel=info

# Terminal 3: Redis server (if not running)
redis-server
```

## Environment Variables

Create a `.env` file:
```
DB_NAME=airbnb_clone
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

## API Usage

### Authentication
Use `/api/auth/login/` for session authentication.

### REST API Examples
```bash
# List properties
GET /api/properties/

# Create booking
POST /api/bookings/
{
  "property": 1,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20"
}
```

### GraphQL Example
```graphql
{
  properties {
    id
    title
    location
    price
    owner {
      username
    }
  }
}
```

## Security Features

- **Authentication**: Session-based with CSRF protection
- **Authorization**: Role-based permissions (Guest/Host/Admin)
- **Rate Limiting**: API throttling
- **Input Validation**: Comprehensive data validation
- **HTTPS Enforcement**: Secure connections
- **Audit Logging**: Request/response logging

## Development

- **Admin Interface**: `/admin/` for content management
- **API Documentation**: DRF browsable API at `/api/`
- **GraphQL Playground**: `/graphql/` with GraphiQL
- **Testing**: Run `python manage.py test`
- **Linting**: Follow PEP 8 standards

## Deployment

- **Docker**: Containerized deployment ready
- **CI/CD**: GitHub Actions pipeline configured
- **Monitoring**: Logging and error tracking
- **Scaling**: Horizontal scaling with load balancers

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

This project is for educational purposes. Ensure compliance with licensing requirements for any third-party integrations.