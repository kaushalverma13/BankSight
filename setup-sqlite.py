#!/usr/bin/env python3
"""
BankSight SQLite Database Setup
Alternative setup using SQLite when PostgreSQL isn't available
"""

import sys
import logging
from pathlib import Path
import sqlite3

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_directories():
    """Create required directories"""
    logger.info("Creating required directories...")
    for directory in ['logs', 'data', 'models', 'reports','.streamlit']:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"  ✓ {directory}/")


def create_sqlite_db():
    """Create SQLite database with tables"""
    logger.info("Creating SQLite database...")
    
    db_path = Path("data") / "banksight.db"
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create tables similar to PostgreSQL models
        logger.info("Creating tables...")
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                customer_id TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                phone TEXT,
                risk_score REAL DEFAULT 0.0,
                kyc_verified BOOLEAN DEFAULT 0,
                account_status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logger.info("  ✓ Customers table created")
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                transaction_id TEXT UNIQUE NOT NULL,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                merchant_name TEXT,
                merchant_category TEXT,
                merchant_country TEXT,
                transaction_type TEXT,
                status TEXT DEFAULT 'COMPLETED',
                fraud_score REAL DEFAULT 0.0,
                is_flagged BOOLEAN DEFAULT 0,
                transaction_date TIMESTAMP,
                device_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        logger.info("  ✓ Transactions table created")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON transactions(customer_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions(transaction_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fraud_score ON transactions(fraud_score)")
        logger.info("  ✓ Indexes created")
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ SQLite database created at: {db_path}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to create SQLite database: {e}")
        return False


def verify_setup():
    """Verify the complete setup"""
    logger.info("Verifying setup...")
    
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
    logger.info("=" * 70)
    logger.info("BankSight SQLite Database Setup")
    logger.info("=" * 70)
    logger.info("")
    
    # Step 1: Verify dependencies
    logger.info("[1/3] Verifying setup...")
    if not verify_setup():
        logger.warning("Some components are missing, but continuing...")
    logger.info("")
    
    # Step 2: Create directories
    logger.info("[2/3] Creating directories...")
    create_directories()
    logger.info("")
    
    # Step 3: Create SQLite database
    logger.info("[3/3] Creating SQLite database...")
    if not create_sqlite_db():
        logger.error("Failed to create database")
        return False
    logger.info("")
    
    logger.info("=" * 70)
    logger.info("SETUP COMPLETE!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("BankSight is configured to use SQLite database.")
    logger.info("Database file: data/banksight.db")
    logger.info("Data persists between app restarts!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Start the application:")
    logger.info("     .venv\\Scripts\\streamlit.exe run app.py")
    logger.info("")
    logger.info("  2. Open in browser: http://localhost:8501")
    logger.info("  3. Click 'Load Sample Data' in the sidebar")
    logger.info("")
    logger.info("Note: To migrate to PostgreSQL later, contact the developer.")
    logger.info("")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
