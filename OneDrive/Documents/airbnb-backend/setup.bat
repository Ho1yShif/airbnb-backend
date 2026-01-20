@echo off
echo ============================================
echo   AirBnB Backend - Environment Configuration
echo ============================================
echo.

REM Verify virtual environment presence and create if necessary
if not exist ".venv" (
    echo Initializing Python virtual environment...
    python -m venv .venv
    echo.
)

REM Activate Python virtual environment
echo Loading virtual environment configuration...
call .venv\Scripts\activate.bat
echo.

REM Install and update project dependencies
echo Installing project dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Generate database migration files
echo Generating database migration definitions...
python manage.py makemigrations
echo.

REM Apply generated migrations to database
echo Applying migration definitions to database...
python manage.py migrate
echo.

REM Consolidate application static resources
echo Consolidating static resources...
python manage.py collectstatic --noinput
echo.

echo ============================================
echo   Configuration Complete
echo ============================================
echo.
echo Next steps:
echo   1. Create superuser account: python manage.py createsuperuser
echo   2. Start development server: python manage.py runserver
echo   3. Access admin interface: http://localhost:8000/admin/
echo.
echo Alternative containerized deployment:
echo   docker-compose up --build
echo.

pause
