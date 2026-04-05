#!/usr/bin/env python3
"""
BankSight Setup and Initialization Script
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.connection import DatabaseManager
from src.database.models import Base
from config.settings import DEBUG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_database():
    """Initialize database"""
    logger.info("Initializing database...")
    try:
        DatabaseManager.initialize()
        DatabaseManager.create_all_tables()
        logger.info("✓ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


def verify_dependencies():
    """Verify all required dependencies are installed"""
    logger.info("Verifying dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'sqlalchemy',
        'psycopg2',
        'scikit-learn',
        'plotly',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.error(f"✗ Missing dependencies: {', '.join(missing)}")
        logger.error("Install them with: pip install -r requirements.txt")
        return False
    
    logger.info("✓ All dependencies verified")
    return True


def create_directories():
    """Create required directories"""
    logger.info("Creating directories...")
    
    directories = [
        'data',
        'logs',
        'models',
        'reports',
        '.streamlit',
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"  ✓ {directory}/")


def test_database_connection():
    """Test database connection"""
    logger.info("Testing database connection...")
    
    if DatabaseManager.health_check():
        logger.info("✓ Database connection successful")
        return True
    else:
        logger.error("✗ Database connection failed")
        return False


def main():
    """Main initialization"""
    logger.info("="*50)
    logger.info("BankSight Initialization")
    logger.info("="*50)
    
    steps = [
        ("Dependencies", verify_dependencies),
        ("Directories", create_directories),
        ("Database", initialize_database),
        ("Connection", test_database_connection),
    ]
    
    results = {}
    for name, step in steps:
        try:
            results[name] = step()
            status = "✓" if results[name] else "✗"
            logger.info(f"{status} {name} initialization")
        except Exception as e:
            logger.error(f"✗ {name} initialization failed: {e}")
            results[name] = False
    
    logger.info("="*50)
    
    if all(results.values()):
        logger.info("✓ All systems initialized successfully!")
        logger.info("\nTo start the application:")
        logger.info("  streamlit run app.py")
        return 0
    else:
        logger.error("✗ Some initialization steps failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
