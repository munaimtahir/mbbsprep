@echo off
setlocal
echo Starting MedPrep development server at http://127.0.0.1:8000/staff/login/

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 manage.py runserver
) else (
    python manage.py runserver
)
