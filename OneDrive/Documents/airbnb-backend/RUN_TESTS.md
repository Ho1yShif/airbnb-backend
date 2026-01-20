# Quick Test Run Guide

## Test Suite Overview

**Total Tests**: 33 covering email, CRUD, Celery, and authentication

```
✅ EmailNotificationSerializerTest (5 tests)
   - Validates request data for email endpoint
   
✅ EmailNotificationEndpointTest (5 tests)
   - Tests POST endpoint with mocked Celery tasks
   
✅ CeleryEmailTaskTest (3 tests)
   - Tests task execution and email sending
   
✅ PropertyCRUDTest (6 tests)
   - Create, read, update, delete property operations
   
✅ BookingCRUDTest (5 tests)
   - Booking creation with date validation
   
✅ ReviewCRUDTest (3 tests)
   - Review creation with rating validation
   
✅ WishlistCRUDTest (3 tests)
   - Add/remove properties from wishlist
   
✅ AuthenticationTest (3 tests)
   - Token auth and authorization checks
```

## Running Tests Locally

### Prerequisites
```bash
# Install test dependencies
pip install -r requirements.txt

# Ensure services are running (or use test settings)
```

### Run All Tests with SQLite (Recommended for Local Dev)
```bash
python manage.py test listings.tests --settings=airbnb.test_settings
```

**Output:**
```
Found 33 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................
----------------------------------------------------------------------
Ran 33 tests in 4.059s

OK
```

### Run Specific Test Class
```bash
# Email serializer tests only
python manage.py test listings.tests.EmailNotificationSerializerTest --settings=airbnb.test_settings

# Property CRUD tests
python manage.py test listings.tests.PropertyCRUDTest --settings=airbnb.test_settings
```

### Run Specific Test Method
```bash
python manage.py test listings.tests.EmailNotificationEndpointTest.test_send_email_success --settings=airbnb.test_settings
```

### Run with Verbose Output
```bash
python manage.py test listings.tests --settings=airbnb.test_settings -v 2
```

### Generate Coverage Report
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='listings' manage.py test listings.tests --settings=airbnb.test_settings

# Generate report
coverage report

# Generate HTML report
coverage html
open htmlcov/index.html
```

## Running Tests in Docker

### Development Container
```bash
# Build and run tests
docker-compose exec web python manage.py test listings.tests --settings=airbnb.test_settings

# With coverage
docker-compose exec web coverage run --source='listings' manage.py test listings.tests --settings=airbnb.test_settings
docker-compose exec web coverage report
```

### Production Services (PostgreSQL + RabbitMQ)
```bash
# Run against actual databases (requires credentials)
docker-compose -f docker-compose.prod.yml exec web python manage.py test listings.tests
```

## Running in GitHub Actions

Tests run automatically on:
- Push to `main` branch
- Pull requests to `main`
- Manual trigger via GitHub UI

**Workflow File**: `.github/workflows/django-ci-cd.yml`

View results:
1. Go to repository → Actions tab
2. Click on workflow run
3. Expand "test" job to see output

## Test Examples

### Email Endpoint Test
```python
def test_send_email_success(self):
    data = {
        'subject': 'Welcome',
        'message': 'Welcome to AirBnB!',
        'recipient': 'user@example.com'
    }
    
    # Mock Celery task
    with patch('listings.tasks.send_notification_email.delay') as mock_task:
        mock_task.return_value.id = 'task-123'
        
        response = self.client.post('/api/send-email/', data, format='json')
        
        assert response.status_code == 202  # ACCEPTED
        assert response.data['status'] == 'success'
```

### Property CRUD Test
```python
def test_create_property(self):
    data = {
        'listing_title': 'Modern Apartment',
        'property_location': '123 Main St',
        'nightly_rate': '150.00',
    }
    
    response = self.client.post('/api/properties/', data, format='json')
    
    assert response.status_code == 201  # CREATED
    assert Property.objects.filter(listing_title='Modern Apartment').exists()
```

### Celery Task Test
```python
def test_send_notification_email_task(self):
    # Task executes synchronously (CELERY_TASK_ALWAYS_EAGER=True)
    result = send_notification_email(
        'Subject',
        'Message content',
        'test@example.com'
    )
    
    # Email immediately available in outbox
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ['test@example.com']
```

## Test Data Factory Usage

```python
from listings.test_utils import TestDataFactory

# Create users
host = TestDataFactory.create_host_user()
guest = TestDataFactory.create_guest_user()

# Create property
prop = TestDataFactory.create_property(
    owner=host,
    listing_title='Test Property',
    nightly_rate=Decimal('100.00')
)

# Create booking
booking = TestDataFactory.create_booking(
    guest=guest,
    property=prop,
    arrival_days=5,
    duration=5
)

# Authenticate
self.authenticate(guest)  # Uses APITestMixin
```

## Common Issues & Solutions

### "No such table: user_profiles"
**Cause**: Migrations not run in test database

**Solution**: Use test settings with SQLite:
```bash
python manage.py test --settings=airbnb.test_settings
```

### "Connection refused" to PostgreSQL
**Cause**: Database not running locally

**Solution**: Use test settings (in-memory SQLite):
```bash
python manage.py test --settings=airbnb.test_settings
```

### "ModuleNotFoundError: No module named 'health_check'"
**Cause**: Missing dependencies

**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### Tests Pass Locally But Fail in CI
**Cause**: Environment variable differences

**Solution**: Check `.env.example` and GitHub Secrets are configured

## Performance Tips

### Faster Test Runs
```bash
# Run only tests that failed last time
python manage.py test --failfast --settings=airbnb.test_settings

# Run single test class (faster than all)
python manage.py test listings.tests.EmailNotificationSerializerTest --settings=airbnb.test_settings
```

### Parallel Test Execution
```bash
# Using pytest-xdist (requires pytest)
pytest listings/tests.py -n 4  # 4 parallel workers
```

### Profile Slow Tests
```bash
python manage.py test --settings=airbnb.test_settings --debug-sql
```

## Debugging Tests

### Print Debug Info in Tests
```python
def test_something(self):
    response = self.client.post('/api/endpoint/', data)
    
    # Print response for debugging
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    
    assert response.status_code == 200
```

### Run With PDB Debugger
```bash
python -m pdb manage.py test listings.tests.EmailNotificationEndpointTest.test_send_email_success --settings=airbnb.test_settings
```

### Stop on First Failure
```bash
python manage.py test --failfast --settings=airbnb.test_settings
```

## Next Steps

1. **Add more tests** for edge cases and error scenarios
2. **Set up code coverage** minimum threshold (e.g., 85%)
3. **Add performance tests** for load testing
4. **Configure pre-commit hooks** to run tests before commits
5. **Document test patterns** for team consistency

## Resources

- [Django Test Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Full Test Suite Documentation](TEST_SUITE.md)
