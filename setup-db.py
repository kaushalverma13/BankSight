#!/usr/bin/env python3
"""
BankSight Database Setup Script
Creates tables and initializes the database
Run this after PostgreSQL is installed and configured
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_database_connection():
    """Test database connection"""
    logger.info("Testing database connection...")
    try:
        from src.database.connection import DatabaseManager
        
        engine = DatabaseManager.get_engine()
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(__import__('sqlalchemy').text("SELECT 1"))
            logger.info("✓ Database connection successful!")
            return True
            
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        logger.error("Make sure PostgreSQL is running and .env is configured correctly")
        return False


def create_tables():
    """Create all database tables"""
    logger.info("Creating database tables...")
    try:
        from src.database.connection import DatabaseManager
        from src.database.models import Base
        
        DatabaseManager.initialize()
        DatabaseManager.create_all_tables()
        logger.info("✓ All tables created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Table creation failed: {e}")
        return False


def verify_setup():
    """Verify the complete setup"""
    logger.info("Verifying BankSight setup...")
    
    checks = {
        "Python": True,
        "Virtual Environment": True,
    }
    
    # Check imports
    try:
        from src.analytics.fraud_detection import FraudDetectionEngine
        checks["Fraud Detection Engine"] = True
    except:
        checks["Fraud Detection Engine"] = False
    
    try:
        from src.analytics.analytics import TransactionAnalytics
        checks["Analytics Engine"] = True
    except:
        checks["Analytics Engine"] = False
    
    try:
        from src.utils.helpers import Logger
        checks["Utilities"] = True
    except:
        checks["Utilities"] = False
    
    # Check directories
    for directory in ['logs', 'data', 'models', 'reports']:
        Path(directory).mkdir(exist_ok=True)
        checks[f"Directory: {directory}"] = True
    
    logger.info("\nSetup Verification:")
    all_ok = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        logger.info(f"  {status} {check_name}")
        if not result:
            all_ok = False
    
    return all_ok


def main():
    """Main setup"""
    logger.info("=" * 60)
    logger.info("BankSight Database Setup")
    logger.info("=" * 60)
    logger.info("")
    
    # Step 1: Verify setup
    logger.info("[1/4] Verifying setup...")
    if not verify_setup():
        logger.warning("Some components are missing, but continuing...")
    logger.info("")
    
    # Step 2: Test connection
    logger.info("[2/4] Testing database connection...")
    if not test_database_connection():
        logger.error("")
        logger.error("SETUP INCOMPLETE")
        logger.error("Please ensure:")
        logger.error("  1. PostgreSQL is installed and running")
        logger.error("  2. .env file exists with correct DB credentials")
        logger.error("  3. Try: psql -U postgres -h localhost")
        logger.error("")
        return False
    logger.info("")
    
    # Step 3: Create tables
    logger.info("[3/4] Creating database tables...")
    if not create_tables():
        logger.error("Failed to create tables")
        return False
    logger.info("")
    
    # Step 4: Create directories
    logger.info("[4/4] Creating required directories...")
    for directory in ['logs', 'data', 'models', 'reports', '.streamlit']:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"  ✓ {directory}/")
    logger.info("")
    
    logger.info("=" * 60)
    logger.info("SETUP COMPLETE!")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Start the application:")
    logger.info("     .venv\\Scripts\\streamlit.exe run app.py")
    logger.info("")
    logger.info("  2. Open in browser: http://localhost:8501")
    logger.info("  3. Click 'Load Sample Data' in the sidebar")
    logger.info("")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
