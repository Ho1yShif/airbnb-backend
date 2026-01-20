# Database migration execution utility for PowerShell
# Applies pending migrations and validates database connectivity

# Configure database connection parameters
$env:DB_NAME = "airbnb"
$env:DB_USER = "airbnb_user"
$env:DB_PASSWORD = "airbnb_pass"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DEBUG = "1"

# Execute database schema migrations
Write-Host "Applying database schema migrations..." -ForegroundColor Green
python manage.py migrate --verbosity=2

# Verify connectivity to database instance
Write-Host "`nValidating database connectivity..." -ForegroundColor Green
$sql = "\dt`n\q"
$result = $sql | python manage.py dbshell 2>&1
Write-Host $result

Write-Host "`nMigration process completed" -ForegroundColor Green
