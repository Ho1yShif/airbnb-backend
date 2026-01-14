# Airbnb Clone Backend

A scalable, secure backend solution for a property rental platform inspired by Airbnb. Built with Django and PostgreSQL.

## Features

- **User Management**: Registration, authentication, profiles with roles (Guest, Host, Admin)
- **Property Management**: Listing creation, image uploads, location-based search
- **Booking System**: Reservation management with status tracking
- **Payment Processing**: Secure payment handling with status tracking
- **Review System**: 1-5 star ratings and comments for properties
- **Wishlist**: User favorite property collections
- **Admin Dashboard**: Django admin for content management

## Technology Stack

- **Backend**: Django 6.0
- **Database**: PostgreSQL
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

3. **Run Migrations**:
```bash
python manage.py migrate
```

4. **Create Superuser**:
```bash
python manage.py createsuperuser
```

5. **Start Services**:
```bash
# Terminal 1: Django server
python manage.py runserver
```

## Environment Variables

Create a `.env` file:
```
DB_NAME=airbnb_clone
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
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


## Project Maintenance & Contact

Maintained by **Martin Mawien**.  
For questions, issues, or collaboration requests, please use the repository's issue tracker or contact via GitHub: [Martin-Mawien](https://github.com/martin-mawien).

This project is for educational purposes. Ensure compliance with licensing requirements for any third-party integrations.