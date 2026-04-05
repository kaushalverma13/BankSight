@echo off
REM BankSight PostgreSQL Setup Script for Windows
REM This script installs PostgreSQL and creates the banksight_db database

echo ================================================
echo BankSight PostgreSQL Setup
echo ================================================
echo.

REM Check if PostgreSQL is already installed
echo Checking for PostgreSQL installation...
psql --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] PostgreSQL is already installed
    goto database_setup
) else (
    echo [INFO] PostgreSQL not found. Installing PostgreSQL 15...
    echo.
    echo Press Y to continue with PostgreSQL installation via Windows Package Manager
    echo Or manually download from: https://www.postgresql.org/download/windows/
    echo.
    REM Try to install via winget
    winget install PostgreSQL.PostgreSQL
    if %ERRORLEVEL% EQU 0 (
        echo [OK] PostgreSQL installed successfully
    ) else (
        echo [ERROR] PostgreSQL installation failed or was cancelled
        echo Please install PostgreSQL manually from: https://www.postgresql.org/download/windows/
        echo After installation, restart this script
        pause
        exit /b 1
    )
)

:database_setup
echo.
echo ================================================
echo Setting up BankSight Database
echo ================================================
echo.

REM Create database and user
echo Creating banksight_db database...
psql -U postgres -h localhost -c "CREATE DATABASE banksight_db;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Database created successfully
) else (
    echo [INFO] Database may already exist or connection failed
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Make sure .env file exists in d:\BankSight\.env
echo 2. Verify database connection:
echo    psql -U postgres -h localhost -d banksight_db
echo 3. Start BankSight:
echo    cd d:\BankSight
echo    .venv\Scripts\streamlit.exe run app.py
echo.
pause
