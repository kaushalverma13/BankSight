# BankSight PostgreSQL Setup Guide

## ✅ What I've Done

1. **Created `.env` file** - Configuration file with all DB settings
2. **Created `setup-postgres.bat`** - Windows batch script for PostgreSQL installation
3. **Created `setup-db.py`** - Python script to create tables and verify setup

---

## 📋 Installation Steps

### Step 1: Install PostgreSQL

**Option A: Automatic Installation (Recommended)**
```bash
# Run the batch script
cd d:\BankSight
setup-postgres.bat
```

**Option B: Manual Installation**
1. Download PostgreSQL 15 from: https://www.postgresql.org/download/windows/
2. Run the installer with these settings:
   - **Installation Directory**: `C:\Program Files\PostgreSQL\15` (default)
   - **Port**: 5432 (default)
   - **Password**: `postgres` (must match `.env` file)
   - **Locale**: English, United States (or your preference)
3. Complete the installation
4. Restart your computer or add PostgreSQL to PATH

**Verify Installation**:
```bash
psql --version
# Should output: psql (PostgreSQL) 15.x.x
```

---

### Step 2: Create BankSight Database

After PostgreSQL is installed, run:

```bash
# Navigate to project
cd d:\BankSight

# Activate virtual environment
.venv\Scripts\activate

# Run database setup
python setup-db.py
```

**What this does**:
- ✓ Tests database connection
- ✓ Creates `banksight_db` database
- ✓ Creates all tables (Customers, Transactions, etc.)
- ✓ Creates required directories (logs, data, models)
- ✓ Verifies all components are installed

**Expected Output**:
```
[1/4] Verifying setup...
  ✓ Python
  ✓ Virtual Environment
  ✓ Fraud Detection Engine
  ✓ Analytics Engine
  ✓ Utilities
  ✓ Directory: logs
  ✓ Directory: data
  ✓ Directory: models
  ✓ Directory: reports

[2/4] Testing database connection...
✓ Database connection successful!

[3/4] Creating database tables...
✓ All tables created successfully!

[4/4] Creating required directories...
  ✓ logs/
  ✓ data/
  ✓ models/
  ✓ reports/
  ✓ .streamlit/

SETUP COMPLETE!
```

---

### Step 3: Verify Database Connection

Test that PostgreSQL is working:

```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# You should see the PostgreSQL prompt:
# postgres=#

# Exit
postgres=# \q
```

---

### Step 4: Restart BankSight App

The BankSight app should already be running from before. If not:

```bash
cd d:\BankSight
.venv\Scripts\streamlit.exe run app.py
```

Then open: http://localhost:8501

---

## 🔧 Environment Variables (`.env` file)

Your `.env` file contains:

```
# Database connection
DB_HOST=localhost          # PostgreSQL server address
DB_PORT=5432              # PostgreSQL port (default)
DB_NAME=banksight_db      # Database name
DB_USER=postgres          # Database user (created by PostgreSQL)
DB_PASSWORD=postgres      # Database password

# Connection pooling
DB_POOL_SIZE=10           # Min connections to maintain
DB_MAX_OVERFLOW=20        # Extra connections when needed

# Application
DEBUG=False               # Production mode
LOG_LEVEL=INFO            # Logging verbosity
CACHE_ENABLED=True        # Enable caching for performance

# Security
SECRET_KEY=...            # Session encryption key
ENCRYPTION_ENABLED=True   # Encrypt sensitive data
ENABLE_AUTH=False         # User authentication

# Features
ENABLE_FRAUD_DETECTION=True
ENABLE_CUSTOMER_ANALYTICS=True
ENABLE_RISK_SCORING=True
ENABLE_REAL_TIME_MONITORING=True
```

---

## 📊 What You Can Now Do

After PostgreSQL is set up, you can:

### ✓ Load Real Data
- Upload transaction files (CSV, Excel)
- Import customer data
- Data persists in PostgreSQL

### ✓ Use Full Features
- Transaction history retention
- Customer profiles updated over time
- Fraud detection models trained on historical data
- Risk scores calculated from patterns

### ✓ Monitor Production
- Audit logs of all transactions
- Compliance reports
- Performance metrics
- Data quality monitoring

---

## 🐛 Troubleshooting

### Problem: "psql is not recognized"
**Solution**: PostgreSQL not in PATH
- Restart your computer after PostgreSQL installation
- Or manually add PostgreSQL to PATH: `C:\Program Files\PostgreSQL\15\bin`

### Problem: "FATAL: password authentication failed"
**Solution**: Check `.env` file
- Verify `DB_PASSWORD` matches PostgreSQL password
- Default is `postgres`

### Problem: "Error: database 'banksight_db' does not exist"
**Solution**: Run database setup again
```bash
python setup-db.py
```

### Problem: App crashes on startup
**Solution**: Check logs
```bash
# View log file
type logs/banksight.log

# Or run with debug
DEBUG=True python setup-db.py
```

---

## 📱 Quick Commands

```bash
# Activate virtual environment
cd d:\BankSight
.venv\Scripts\activate

# Start BankSight
streamlit run app.py

# Run tests
pytest tests/ -v

# View database
psql -U postgres -d banksight_db

# Format code
black src/ tests/ *.py

# Check for issues
flake8 src/
```

---

## 🎯 Next Steps

1. **Run `setup-postgres.bat`** to install PostgreSQL
2. **Run `python setup-db.py`** to create database
3. **Open http://localhost:8501** in browser
4. **Click "Load Sample Data"** to test
5. **Start uploading real data** to PostgreSQL

---

## 💡 Need Help?

### Check Setup Status
```bash
python setup-db.py
```

### View Application Logs
```bash
type logs/banksight.log
```

### Reset Everything
```bash
# Drop all tables (WARNING: Deletes all data!)
python -c "from src.database.connection import DatabaseManager; DatabaseManager.drop_all_tables()"

# Recreate tables
python setup-db.py
```

---

**Your BankSight setup is ready to go!** 🚀
