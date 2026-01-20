@echo off
REM Database migration execution utility for Windows environments
setlocal enabledelayedexpansion

REM Configure database connection parameters
set DB_NAME=airbnb
set DB_USER=airbnb_user
set DB_PASSWORD=airbnb_pass
set DB_HOST=localhost
set DB_PORT=5432
set DEBUG=1

REM Navigate to project root directory
cd /d "C:\Users\pakok\OneDrive\Documents\airbnb-backend"

REM Activate Python virtual environment if available
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Execute migration utility script

pause
