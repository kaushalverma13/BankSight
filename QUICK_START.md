# 🚀 BankSight Enhanced Local Setup - Quick Start

## ✅ Current Status

| Component | Status | Details |
|-----------|--------|---------|
| **Streamlit App** | ✅ RUNNING | http://localhost:8501 |
| **Python Setup** | ✅ READY | Virtual environment configured |
| **ML Libraries** | ✅ READY | scikit-learn, scipy working |
| **Analytics Engine** | ✅ READY | Fraud detection, risk scoring |
| **Database Config** | ✅ CREATED | `.env` file with all settings |
| **PostgreSQL** | ⏳ PENDING | Need to install |
| **Setup Scripts** | ✅ CREATED | Automating PostgreSQL setup |

---

## 📋 IMMEDIATE NEXT STEPS (In Order)

### 1️⃣ **Install PostgreSQL** (5 minutes)

**Option A: Automatic**
```bash
# Run this command:
cd d:\BankSight
setup-postgres.bat
# This will guide you through installation
```

**Option B: Manual Download**
- Download from: https://www.postgresql.org/download/windows/
- Install PostgreSQL 15
- Set password to: `postgres` (or update in `.env`)

**Verify Installation**:
```bash
psql --version
# Should show: psql (PostgreSQL) 15.x
```

---

### 2️⃣ **Create Database** (2 minutes)

After PostgreSQL is installed:

```bash
# Make sure you're in the project directory
cd d:\BankSight

# Activate virtual environment
.venv\Scripts\activate

# Run database setup
python setup-db.py
```

**This will**:
- ✓ Test PostgreSQL connection
- ✓ Create `banksight_db` database
- ✓ Create all 5 tables (Customers, Transactions, etc.)
- ✓ Set up required directories

---

### 3️⃣ **Restart BankSight** (1 minute)

If the app stopped, restart it:

```bash
cd d:\BankSight
.venv\Scripts\streamlit.exe run app.py
```

Then open: **http://localhost:8501**

---

### 4️⃣ **Test Everything** (2 minutes)

In the Streamlit app:
1. Click **"Load Sample Data"** button
2. Watch the data load and calculate fraud scores
3. Browse each view:
   - ✓ Dashboard
   - ✓ Fraud Detection
   - ✓ Customer Analytics
   - ✓ Risk Scoring
   - ✓ Transaction Analysis

---

## 📂 Files I Created for You

| File | Purpose |
|------|---------|
| `.env` | Database & application configuration |
| `setup-postgres.bat` | Windows batch script to install PostgreSQL |
| `setup-db.py` | Python script to create database & tables |
| `POSTGRES_SETUP.md` | Complete setup documentation |

---

## 🔑 Key Configuration (`.env`)

```ini
DB_HOST=localhost       # PostgreSQL location
DB_PORT=5432           # PostgreSQL port
DB_NAME=banksight_db   # Database to create
DB_USER=postgres       # Default PostgreSQL user
DB_PASSWORD=postgres   # Default PostgreSQL password
```

**Note**: If you set a different PostgreSQL password during installation, update the `.env` file accordingly.

---

## 📊 What Each File Does

### `setup-postgres.bat`
- Checks if PostgreSQL is installed
- If not, installs via Windows Package Manager
- Creates initial database connection

### `setup-db.py`
- Connects to PostgreSQL
- Creates all 5 data models:
  - `Customers` - Customer profiles
  - `Transactions` - Transaction records
  - `TransactionFraudData` - Fraud analysis details
  - `FraudAlerts` - Alert management
  - `DeviceInfo` - Device trust scores
- Creates required directories
- Verifies everything works

---

## 🎯 Benefits After Setup

✅ **Data Persistence**
- All data saved to PostgreSQL
- Survives app restart
- Multiple sessions can work with same data

✅ **Production Features**
- Audit logging
- Compliance reporting
- Historical data analysis
- Real fraud pattern learning

✅ **Scaling Ready**
- Handle millions of transactions
- Multi-user access
- Backup & recovery
- Performance optimization

---

## ⚡ Quick Reference

```bash
# ===== SETUP =====
cd d:\BankSight
setup-postgres.bat              # Install PostgreSQL
.venv\Scripts\activate          # Activate venv
python setup-db.py              # Create database

# ===== RUN APPLICATION =====
.venv\Scripts\streamlit.exe run app.py

# ===== VERIFY =====
psql -U postgres -h localhost   # Test connection
python setup-db.py              # Check setup status

# ===== DEVELOPMENT =====
pytest tests/ -v                # Run tests
black src/ tests/ *.py          # Format code
flake8 src/                      # Check quality
```

---

## ✨ Success Indicators

After setup is complete, you should see:

```
✓ App running at http://localhost:8501
✓ Database connection successful
✓ All 5 tables created
✓ Sample data loads instantly
✓ Fraud detection works
✓ Charts render properly
✓ No errors in logs
```

---

## 🆘 If Something Goes Wrong

### PostgreSQL Won't Install
- Check: https://www.postgresql.org/download/windows/
- Manual download & install required
- Make sure to set password: `postgres`

### Database Connection Failed
```bash
# Test connection manually
psql -U postgres -h localhost
# Password: postgres

# Check .env file has correct settings
type .env
```

### Setup Script Fails
```bash
# Run with error details
python setup-db.py
# Read the error message carefully

# Check logs
type logs/banksight.log
```

### App Crashes
```bash
# Stop current app (Ctrl+C in terminal)
# Check what crashed
type logs/banksight.log

# Restart
.venv\Scripts\streamlit.exe run app.py
```

---

## 📞 Need Help?

1. **Check the logs**:
   ```bash
   type logs/banksight.log
   ```

2. **Run verification**:
   ```bash
   python setup-db.py
   ```

3. **Review documentation**:
   - `POSTGRES_SETUP.md` - Complete guide
   - `README.md` - Project overview
   - `DEVELOPMENT.md` - Development guide

---

## 🎉 YOU'RE READY!

The hard part is done. Just follow the 4 steps above and you'll have a fully functional production-ready BankSight system with PostgreSQL!

**Estimated total time: 15-20 minutes**

Good luck! 🚀
