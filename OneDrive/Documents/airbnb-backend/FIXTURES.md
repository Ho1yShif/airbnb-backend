# Database Fixtures Guide

## Overview

The `load_fixtures` management command populates your database with sample data for development and testing.

## What Gets Created

When you run the fixtures command, it creates:

- **3 Host Accounts** (property owners)
- **4 Guest Accounts** (travelers/renters)
- **6 Properties** (listings with descriptions, rates, locations)
- **5 Bookings** (reservations in various states)
- **3 Payment Records** (transaction data)
- **3 Reviews** (ratings and comments)
- **5 Wishlist Items** (saved properties by guests)

## Usage

### Basic Setup

1. **Ensure database is running:**
   ```bash
   # With Docker Compose
   docker-compose up -d db
   
   # Or PostgreSQL running locally
   psql -U airbnb_user -d airbnb
   ```

2. **Run migrations first:**
   ```bash
   python manage.py migrate
   ```

3. **Load sample data:**
   ```bash
   python manage.py load_fixtures
   ```

### With Existing Data

To clear existing data and reload fresh fixtures:
```bash
python manage.py load_fixtures --clear
```

## Sample Accounts for Testing

After running the command, use these credentials to test the API:

### Hosts (Property Owners)
| Username | Email | Password |
|----------|-------|----------|
| alice_host | alice@example.com | password123 |
| bob_host | bob@example.com | password123 |
| carol_host | carol@example.com | password123 |

### Guests (Travelers)
| Username | Email | Password |
|----------|-------|----------|
| john_guest | john@example.com | password123 |
| jane_guest | jane@example.com | password123 |
| mike_guest | mike@example.com | password123 |
| sarah_guest | sarah@example.com | password123 |

## Sample Properties

| Title | Owner | Rate | Location |
|-------|-------|------|----------|
| Modern Downtown Apartment | alice_host | $150/night | New York, NY |
| Cozy Studio Loft | alice_host | $95/night | New York, NY |
| Luxury Penthouse Suite | bob_host | $350/night | New York, NY |
| Beachfront Beach House | bob_host | $250/night | Miami, FL |
| Mountain Cabin Retreat | carol_host | $180/night | Aspen, CO |
| Historic Victorian Home | carol_host | $200/night | Boston, MA |

## Testing API Endpoints

### 1. Get Authentication Token (Login)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_guest", "password": "password123"}'
```

### 2. List Properties
```bash
curl http://localhost:8000/api/listings/
```

### 3. View Property Details
```bash
curl http://localhost:8000/api/listings/1/
```

### 4. Send Email Notification
```bash
curl -X POST http://localhost:8000/api/send-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Welcome to AirBnB",
    "message": "Thanks for booking with us!",
    "recipient": "guest@example.com"
  }'
```

### 5. Create Booking (as Guest)
```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "guest": 1,
    "reserved_property": 1,
    "arrival_date": "2026-02-01",
    "departure_date": "2026-02-05"
  }'
```

### 6. View Bookings
```bash
curl http://localhost:8000/api/reservations/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Booking States

Fixtures create bookings in these states for testing:

- **awaiting_approval** - New booking pending host review
- **approved** - Host accepted the booking
- **rejected** - Host declined (testable)
- **completed** - Past booking that finished

## Payment Status

Payments are created with status:
- **successful** - Completed transactions

## Review Ratings

Sample reviews range from 4-5 stars with comments describing guest experience.

## Docker Compose Workflow

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Load fixtures
docker-compose exec web python manage.py load_fixtures

# Check logs
docker-compose logs -f web
```

## Clearing Data

To reset to a clean database:

```bash
# Drop all tables and recreate
python manage.py flush

# Or use the --clear flag with load_fixtures
python manage.py load_fixtures --clear
```

## Notes

- All sample passwords are `password123`
- Dates are relative to today (bookings scheduled future/past)
- Images are not created (model supports but not populated)
- Wishlist items link guests to properties
- Ready for API testing immediately after loading

## Troubleshooting

**Database Connection Error:**
```
psycopg2.OperationalError: connection to server at "localhost"
```
→ Ensure PostgreSQL is running: `sudo service postgresql start`

**ModuleNotFoundError: No module named 'drf_yasg'**
```
pip install -r requirements.txt
```

**Fixtures already exist:**
```
python manage.py load_fixtures --clear
```
Then reload fresh data.
