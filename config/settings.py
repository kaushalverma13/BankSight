"""
BankSight Configuration Settings
Project: Transaction Intelligence Dashboard
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Application Configuration
APP_NAME = "BankSight: Transaction Intelligence Dashboard"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5433))
DB_NAME = os.getenv("DB_NAME", "banksight_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "") or None  # Allow empty password
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 10))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 20))

# SQLAlchemy Configuration
if DB_PASSWORD:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", "logs/banksight.log")

# Analytics Configuration
ROLLING_WINDOW_DAYS = 30
ANOMALY_THRESHOLD = 2.5  # Standard deviations
MIN_TRANSACTIONS_FOR_PATTERN = 10

# Fraud Detection Configuration
FRAUD_DETECTION_MODEL = "isolation_forest"
FRAUD_SCORE_THRESHOLD = 0.7
TRANSACTION_AMOUNT_PERCENTILE = (1, 99)
VELOCITY_CHECK_WINDOW = timedelta(hours=24)
GEOLOCATION_IMPOSSIBLE_SPEED_KMH = 1000

# Streamlit Configuration
STREAMLIT_PAGE_CONFIG = {
    "page_title": "BankSight Dashboard",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Cache Configuration
CACHE_TTL = 3600  # 1 hour
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"

# API Configuration (if needed)
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Data Configuration
DATA_DIR = "data"
REPORTS_DIR = "reports"
MODELS_DIR = "models"

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "development-key-change-in-production")
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "False").lower() == "true"
ENCRYPTION_ENABLED = os.getenv("ENCRYPTION_ENABLED", "True").lower() == "true"

# Feature Flags
ENABLE_FRAUD_DETECTION = True
ENABLE_CUSTOMER_ANALYTICS = True
ENABLE_RISK_SCORING = True
ENABLE_REAL_TIME_MONITORING = True

# Export configurations
EXPORT_FORMATS = ["CSV", "EXCEL", "PDF", "JSON"]

# Thresholds and Limits
MAX_TRANSACTION_AMOUNT = 1_000_000
MIN_TRANSACTION_AMOUNT = 0.01
MAX_DAILY_TRANSACTIONS = 10_000
ALERT_THRESHOLD_AMOUNT = 50_000
