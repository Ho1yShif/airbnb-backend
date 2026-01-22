# AirBnB Backend Test Suite Documentation

## Overview

Comprehensive test suite covering:
- Email notification endpoint with request/response validation
- CRUD operations for all major resources (Property, Booking, Review, Wishlist)
- Celery task execution with mocking
- Email sending with mock backend
- Authentication and authorization
- Data validation and error handling

## Test Structure

### 1. Email Notification Tests

#### `EmailNotificationSerializerTest`
Tests for request data validation:

```python
# Valid email
data = {
    'subject': 'Test Subject',
    'message': 'Test message content',
    'recipient': 'test@example.com'
}
```

**Test Cases:**
- `test_valid_email_notification()` - Valid data passes validation
- `test_invalid_email_format()` - Rejects malformed emails
- `test_missing_required_fields()` - Requires all fields
- `test_empty_subject()` - Rejects empty subject
- `test_long_subject()` - Enforces 255 character limit

#### `EmailNotificationEndpointTest`
Tests for API endpoint functionality:

```bash
POST /api/send-email/
Content-Type: application/json

{
    "subject": "Welcome",
    "message": "Welcome to AirBnB!",
    "recipient": "user@example.com"
}
```

**Response (202 Accepted):**
```json
{
    "status": "success",
    "task_id": "task-123"
}
```

**Test Cases:**
- `test_send_email_success()` - Successfully queues task
- `test_send_email_invalid_data()` - Returns 400 for invalid data
- `test_send_email_invalid_email()` - Validates email format
- `test_send_email_task_error()` - Handles Celery errors (500)
- `test_send_email_get_not_allowed()` - Only POST allowed

### 2. Celery Email Task Tests

#### `CeleryEmailTaskTest`
Tests for email task execution:

**Test Cases:**
- `test_send_notification_email_task()` - Task sends email successfully
  - Verifies email in Django outbox
  - Checks recipient, subject, and message
  
- `test_send_notification_email_multiple()` - Sends multiple emails
  - Verifies all emails queued
  - Checks each email properties
  
- `test_send_notification_email_failure()` - Handles SMTP failures
  - Mocks send_mail failure
  - Verifies exception handling

**How It Works:**
```python
# Tasks execute synchronously in tests (CELERY_TASK_ALWAYS_EAGER=True)
result = send_notification_email(subject, message, recipient)
# Email immediately available in mail.outbox
self.assertEqual(len(mail.outbox), 1)
```

### 3. Property CRUD Tests

#### `PropertyCRUDTest`
Tests for property management endpoints:

**Create:**
```bash
POST /api/properties/
Authorization: Token <token>

{
    "listing_title": "Modern Apartment",
    "property_location": "123 Main St",
    "nightly_rate": "150.00",
    "property_description": "Beautiful modern apartment",
    "listing_status": "available"
}
```

**Test Cases:**
- `test_create_property()` - Creates property successfully
- `test_list_properties()` - Lists all properties
- `test_retrieve_property()` - Gets single property
- `test_update_property()` - Patches property fields
- `test_delete_property()` - Deletes property
- `test_create_property_invalid_rate()` - Validates nightly rate > 0

### 4. Booking CRUD Tests

#### `BookingCRUDTest`
Tests for booking management:

**Create:**
```bash
POST /api/bookings/
Authorization: Token <token>

{
    "reserved_property": 1,
    "arrival_date": "2026-02-01",
    "departure_date": "2026-02-06"
}
```

**Test Cases:**
- `test_create_booking()` - Creates booking with valid dates
- `test_create_booking_invalid_dates()` - Rejects departure before arrival
- `test_create_booking_past_date()` - Rejects past dates
- `test_list_bookings()` - Lists user's bookings
- `test_update_booking_status()` - Updates reservation state

### 5. Review CRUD Tests

#### `ReviewCRUDTest`
Tests for review management:

**Create:**
```bash
POST /api/reviews/
Authorization: Token <token>

{
    "reviewed_property": 1,
    "rating": 5,
    "comment": "Excellent property!"
}
```

**Test Cases:**
- `test_create_review()` - Creates review successfully
- `test_create_review_invalid_rating()` - Rejects rating > 5
- `test_list_reviews()` - Lists reviews

### 6. Wishlist CRUD Tests

#### `WishlistCRUDTest`
Tests for wishlist management:

**Add to Wishlist:**
```bash
POST /api/wishlist/
Authorization: Token <token>

{
    "property": 1
}
```

**Test Cases:**
- `test_add_to_wishlist()` - Adds property to wishlist
- `test_list_wishlist()` - Lists user's wishlist
- `test_remove_from_wishlist()` - Removes from wishlist

### 7. Authentication Tests

#### `AuthenticationTest`
Tests for token-based authentication:

**Test Cases:**
- `test_unauthenticated_access_denied()` - 401 without token
- `test_token_authentication()` - 200 with valid token
- `test_invalid_token()` - 401 with invalid token

## Test Utilities

### `TestDataFactory`
Helper class for creating test data:

```python
from listings.test_utils import TestDataFactory

# Create users
host = TestDataFactory.create_host_user()
guest = TestDataFactory.create_guest_user()

# Create property
prop = TestDataFactory.create_property(owner=host, listing_title='Test')

# Create booking
booking = TestDataFactory.create_booking(guest, prop, arrival_days=5, duration=5)

# Create review
review = TestDataFactory.create_review(guest, prop, rating=5, comment='Great!')

# Create wishlist entry
wishlist = TestDataFactory.create_wishlist(guest, prop)

# Get auth token
token = TestDataFactory.get_auth_token(guest)
```

### `APITestMixin`
Mixin for common API testing functionality:

```python
class MyTest(APITestCase, APITestMixin):
    def setUp(self):
        self.user = TestDataFactory.create_guest_user()
        self.client = APIClient()
    
    def test_something(self):
        # Authenticate client
        self.authenticate(self.user)
        
        # Assert valid JSON
        response = self.client.get('/api/some-endpoint/')
        self.assert_valid_json(response)
        
        # Assert specific fields present
        self.assert_property_fields(response.data, ['id', 'name', 'email'])
        
        # Assert error response
        self.assert_error_response(response, status_code=400, error_field='email')
```

### `CeleryTestMixin`
Mixin for Celery task testing:

```python
class MyTaskTest(TestCase, CeleryTestMixin):
    def setUp(self):
        self.setup_celery_test()
    
    def test_task(self):
        # Task executes synchronously
        result = my_task.delay(arg1, arg2)
        # Assert result immediately
        self.assertEqual(result, expected)
```

## Running Tests

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Class
```bash
python manage.py test listings.tests.EmailNotificationEndpointTest
```

### Run Specific Test Method
```bash
python manage.py test listings.tests.EmailNotificationEndpointTest.test_send_email_success
```

### Run With Verbose Output
```bash
python manage.py test --verbosity=2
```

### Run With Coverage
```bash
pip install coverage
coverage run --source='listings' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Run Tests in Docker
```bash
# Development environment
docker-compose exec web python manage.py test

# Production environment with services
docker-compose -f docker-compose.prod.yml exec web python manage.py test
```

### Run Tests with Celery
Tests use `CELERY_TASK_ALWAYS_EAGER=True` to execute tasks synchronously.

**In settings.py for tests:**
```python
if 'test' in sys.argv:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
```

## Test Configuration

### Django Test Settings
Key settings in `settings.py`:

```python
# Celery - Execute tasks synchronously in tests
if 'test' in sys.argv:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

# Email - Use console backend for testing
if 'test' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Database - Use in-memory SQLite
# DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
# DATABASES['default']['NAME'] = ':memory:'
```

### Environment Variables for Testing
```bash
DJANGO_SETTINGS_MODULE=airbnb.settings
SECRET_KEY=test-secret-key-not-for-production
DEBUG=True
CELERY_BROKER_URL=memory://
CELERY_RESULT_BACKEND=cache+memory://
```

## Mocking Examples

### Mock Celery Task
```python
from unittest.mock import patch

def test_email_endpoint(self):
    with patch('listings.tasks.send_notification_email.delay') as mock_task:
        mock_task.return_value.id = 'task-123'
        
        response = self.client.post('/api/send-email/', data)
        
        self.assertEqual(response.data['task_id'], 'task-123')
        mock_task.assert_called_once()
```

### Mock Email Send
```python
from unittest.mock import patch

def test_email_failure(self):
    with patch('django.core.mail.send_mail') as mock_send:
        mock_send.side_effect = Exception('SMTP error')
        
        with self.assertRaises(Exception):
            send_notification_email('Subject', 'Message', 'test@example.com')
        
        mock_send.assert_called_once()
```

### Mock External API
```python
from unittest.mock import patch

def test_payment_processing(self):
    with patch('listings.views.process_payment') as mock_api:
        mock_api.return_value = {'status': 'success', 'id': '123'}
        
        response = self.client.post('/api/process-payment/', payment_data)
        
        self.assertEqual(response.data['status'], 'success')
```

## Test Data

### Sample User Accounts

**Host User:**
- Username: `testhost`
- Email: `host@example.com`
- Password: `testpass123`
- Role: `host`

**Guest User:**
- Username: `testguest`
- Email: `guest@example.com`
- Password: `testpass123`
- Role: `guest`

### Sample Property
```json
{
    "listing_title": "Test Property",
    "property_location": "Test Location",
    "nightly_rate": "100.00",
    "property_description": "Test description",
    "listing_status": "available"
}
```

### Sample Booking
- Arrival: 5 days from today
- Departure: 10 days from today (5-day duration)
- Status: `awaiting_approval`

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Push to `main` branch
- Pull requests
- Manual trigger

**Test Job:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      rabbitmq:
        image: rabbitmq:3-management
        options: >-
          --health-cmd rabbitmq-diagnostics ping
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python manage.py test --verbosity=2
```

## Troubleshooting

### Test Database Not Created
**Issue:** `OperationalError: database does not exist`

**Solution:**
```bash
# Ensure PostgreSQL is running
sudo service postgresql start

# Run migrations for test database
python manage.py migrate --run-syncdb
```

### Celery Tasks Not Executing
**Issue:** Tasks queued but not executed in tests

**Solution:** Ensure `CELERY_TASK_ALWAYS_EAGER=True` in test settings:
```python
# settings.py
if 'test' in sys.argv:
    CELERY_TASK_ALWAYS_EAGER = True
```

### Import Errors in Tests
**Issue:** `ModuleNotFoundError` when importing models/views

**Solution:**
1. Verify `__init__.py` exists in all directories
2. Ensure Django app is in `INSTALLED_APPS`
3. Use absolute imports: `from listings.models import Property`

### Async Test Failures
**Issue:** Tests fail intermittently with async operations

**Solution:** Use `TestCase` instead of `TransactionTestCase` for transaction handling, and ensure all async operations complete before assertions.

## Best Practices

1. **Use Factory Pattern:** Use `TestDataFactory` to create consistent test data
2. **Mock External Services:** Mock email, payments, external APIs
3. **Test Edge Cases:** Invalid dates, missing fields, unauthorized access
4. **Keep Tests Isolated:** Each test should be independent
5. **Use Descriptive Names:** Test names should describe what they test
6. **Arrange-Act-Assert:** Structure tests clearly with setup, action, verification
7. **Test Permissions:** Verify users can only access their own data
8. **Test Status Codes:** Verify correct HTTP status codes returned
9. **Validate Responses:** Check response format and required fields
10. **Document Complex Tests:** Add comments explaining test logic

## Code Coverage

### Generate Coverage Report
```bash
coverage run --source='listings' manage.py test
coverage report

# Sample output:
# Name                                    Stmts   Miss  Cover
# ─────────────────────────────────────────────────────────
# listings/__init__.py                       0      0   100%
# listings/models.py                       120     10    92%
# listings/serializers.py                   85      5    94%
# listings/views.py                        150     15    90%
# listings/tasks.py                         30      0   100%
# ─────────────────────────────────────────────────────────
# TOTAL                                    450     35    92%
```

### Coverage Goals
- Overall: 85%+
- Critical paths (auth, payments): 95%+
- Utils/helpers: 80%+

## Performance Testing

### Load Test Email Endpoint
```bash
# Using Apache Bench
ab -n 1000 -c 10 -p email_data.json http://localhost:8000/api/send-email/

# Using Locust
pip install locust
# Create locustfile.py with test scenarios
locust -f locustfile.py --host=http://localhost:8000
```

### Load Test CRUD Operations
```python
import concurrent.futures
from listings.test_utils import TestDataFactory

def create_property(host_id):
    host = User.objects.get(id=host_id)
    return TestDataFactory.create_property(host)

# Create 100 properties concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(create_property, host_id) for _ in range(100)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
```

## Additional Resources

- [Django Test Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Celery Testing Guide](https://docs.celeryproject.org/en/stable/userguide/testing.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Mock Library Documentation](https://docs.python.org/3/library/unittest.mock.html)
