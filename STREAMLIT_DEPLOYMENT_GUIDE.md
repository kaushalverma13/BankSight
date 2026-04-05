# STREAMLIT CLOUD DEPLOYMENT GUIDE

## Complete Step-by-Step Instructions

---

## PART 1: PREPARE YOUR LOCAL PROJECT

### Step 1.1: Update requirements.txt
Delete `psycopg2-binary` from requirements.txt since Streamlit Cloud uses SQLite by default.

```bash
# Remove PostgreSQL dependency
# Keep everything else
```

Current problematic packages to replace:
- Remove: `psycopg2-binary` (PostgreSQL specific)
- Keep: Everything else

### Step 1.2: Create `.gitignore`
Make sure these files are NOT uploaded to GitHub:

```
.venv/
__pycache__/
*.pyc
.env
*.log
*.db
.streamlit/secrets.toml
data/
models/
logs/
reports/
.DS_Store
*.egg-info/
dist/
build/
```

### Step 1.3: Create `secrets.toml` for local testing

```toml
# .streamlit/secrets.toml

# Database Configuration
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "banksight_db"
DB_USER = "postgres"
DB_PASSWORD = ""

# Application Settings
DEBUG = false
LOG_LEVEL = "INFO"
CACHE_ENABLED = true

# Security
SECRET_KEY = "your-secret-key-change-in-production"
ENCRYPTION_ENABLED = true
```

---

## PART 2: CREATE GITHUB REPOSITORY

### Step 2.1: Initialize Git Locally

```bash
cd d:\BankSight

# Initialize repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: BankSight Transaction Intelligence Dashboard"

# Add remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2.2: GitHub Repository Structure

Your repository should have:

```
BankSight/
├── .streamlit/
│   └── config.toml
├── .gitignore
├── src/
│   ├── analytics/
│   ├── database/
│   └── utils/
├── config/
│   └── settings.py
├── tests/
├── app.py
├── requirements.txt
├── README.md
├── DEVELOPMENT.md
└── setup-sqlite.py
```

---

## PART 3: DEPLOY ON STREAMLIT CLOUD

### Step 3.1: Create Streamlit Cloud Account

1. Go to: https://streamlit.io/cloud
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Streamlit to access your GitHub account

### Step 3.2: Deploy Your App

1. After login, click "New app" button
2. Fill in deployment details:
   - **Repository**: Select your BankSight repo
   - **Branch**: `main` (or your branch name)
   - **Main file path**: `app.py`
3. Click "Deploy!"
4. Wait for deployment (usually 2-3 minutes)

### Step 3.3: Configure Secrets (If Using External DB)

1. Go to your app's settings
2. Click "Secrets" section
3. Add your database credentials:

```toml
DB_HOST = "your-database-host"
DB_PORT = 5432
DB_NAME = "banksight_db"
DB_USER = "postgres"
DB_PASSWORD = "your-password"
```

---

## PART 4: OPTIMIZE FOR STREAMLIT CLOUD

### Step 4.1: Update config/settings.py

```python
import os
from dotenv import load_dotenv

# Load from environment or .streamlit/secrets.toml
load_dotenv()

# Database Configuration (with SQLite as default for cloud)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "banksight_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Use SQLite for Streamlit Cloud
import streamlit as st
if st.secrets.get("USE_SQLITE", True):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///data/banksight.db"
elif DB_PASSWORD:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

### Step 4.2: Update app.py for Cloud Deployment

Add this at the beginning of `app.py`:

```python
import os
import sys
from pathlib import Path

# Set up logging directory
Path("logs").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Load environment
from dotenv import load_dotenv
load_dotenv()
```

### Step 4.3: Use Streamlit Caching

Update your data loading functions:

```python
import streamlit as st

@st.cache_resource
def load_fraud_detection_engine():
    """Load fraud detection model once"""
    from src.analytics.fraud_detection import FraudDetectionEngine
    return FraudDetectionEngine()

@st.cache_data
def load_analytics():
    """Cache analytics engines"""
    from src.analytics.analytics import (
        TransactionAnalytics, 
        CustomerAnalytics, 
        RiskScoring
    )
    return {
        'transactions': TransactionAnalytics,
        'customers': CustomerAnalytics,
        'risk': RiskScoring,
    }
```

---

## PART 5: HANDLE STREAMLIT-SPECIFIC ISSUES

### Issue 1: Session State Persistence

Streamlit reruns entire script on each interaction. Use session state:

```python
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'transactions_df' not in st.session_state:
    st.session_state.transactions_df = None
```

### Issue 2: File Upload Handling

If adding file upload feature:

```python
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Process data
```

### Issue 3: Database Access Limits

Streamlit Cloud free tier has limitations:
- 1 GB disk space
- SQLite database limited to 1 GB
- No persistent external storage
- Use `st.secrets` for credentials

---

## PART 6: DEPLOYMENT COMMANDS

### Local Testing (Before Deployment)

```bash
# Test app locally
.venv\Scripts\streamlit.exe run app.py

# Build requirements
.venv\Scripts\pip freeze > requirements.txt

# Test with Streamlit config
.venv\Scripts\streamlit.exe run app.py --logger.level=debug
```

### GitHub Push

```bash
# Make changes locally
# Then push to GitHub

git add .
git commit -m "Update for Streamlit Cloud deployment"
git push origin main
```

### Redeploy from Streamlit Cloud

Simply push to GitHub, and Streamlit Cloud will automatically redeploy!

---

## PART 7: POST-DEPLOYMENT

### Monitor Your App

1. Go to: https://share.streamlit.io
2. Your app appears in dashboard
3. Click "Manage" for settings
4. View logs: Click the three dots → "Settings" → "View logs"

### Update Your App

1. Make changes locally
2. Push to GitHub: `git push origin main`
3. Streamlit Cloud will auto-redeploy (2-3 minutes)

### Share Your App

Your app will be available at:
```
https://your-username-banksight.streamlit.app
```

Or a custom URL if you configure it.

---

## PART 8: TROUBLESHOOTING

### App Won't Deploy

**Error**: "Requirements.txt not found"
```bash
# Solution: Ensure requirements.txt exists in root directory
ls requirements.txt
```

**Error**: "Module not found"
```bash
# Solution: Add missing packages to requirements.txt
# Then push to GitHub
```

### App Crashes After Deployment

**Check logs**:
1. Go to Streamlit Cloud dashboard
2. Click your app
3. Click three dots → "View logs"
4. Look for error messages

**Common issues**:
- Missing imports
- Database connection failed
- Memory limit exceeded

### Database Errors

If using SQLite:
```python
# Ensure data directory exists
Path("data").mkdir(exist_ok=True)

# Check database file
import os
print(os.path.exists("data/banksight.db"))
```

---

## PART 9: DEPLOYMENT CHECKLIST

Before deploying, verify:

- [ ] `.env` is in `.gitignore` (never upload secrets)
- [ ] `requirements.txt` is up to date
- [ ] `.streamlit/config.toml` is configured
- [ ] `app.py` works locally: `streamlit run app.py`
- [ ] GitHub repository is set up
- [ ] All imports are correct
- [ ] Database setup works
- [ ] No hardcoded credentials
- [ ] `README.md` has clear instructions
- [ ] App runs without errors locally

---

## PART 10: FINAL DEPLOYMENT STEPS

### Step 1: Clean Up Local Files

```bash
cd d:\BankSight

# Remove unnecessary files
rm -r __pycache__/
rm -r .pytest_cache/
rm -r .mypy_cache/
rm -r logs/*
rm -r data/*.db

# Verify required files exist
ls app.py requirements.txt README.md .gitignore
```

### Step 2: Update requirements.txt

```bash
# Generate clean requirements
.venv\Scripts\pip freeze > requirements.txt

# Remove psycopg2-binary from requirements.txt (manual edit)
# Keep everything else including:
# - streamlit
# - pandas
# - numpy
# - scikit-learn
# - plotly
# - python-dotenv
```

### Step 3: Create .gitignore

```
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
*.log
*.db
data/
logs/
models/
reports/
.DS_Store
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
```

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 5: Deploy on Streamlit Cloud

1. Visit: https://streamlit.io/cloud
2. Click "New app"
3. Select repository, branch (main), file (app.py)
4. Click "Deploy"
5. Wait 2-3 minutes

### Step 6: Access Your App

Your app will be available at:
```
https://<your-username>-banksight.streamlit.app
```

---

## PART 11: MONITORING & MAINTENANCE

### View App Metrics

- **Users**: How many people accessed
- **Performance**: Load times
- **Crashes**: Error frequency
- **Storage**: Disk usage

### Update App

1. Make code changes
2. Run locally to test
3. Push to GitHub
4. Auto-redeployment happens
5. App updates within 2-3 minutes

### Manage Resources

- Monitor storage usage (1 GB limit free tier)
- Clean up old data periodically
- Use `@st.cache_resource` for expensive operations

---

## SUCCESS INDICATORS

After deployment, you should see:

✅ App loads at https://your-username-banksight.streamlit.app
✅ "Load Sample Data" button works
✅ Charts render correctly
✅ No errors in logs
✅ Features functional (fraud detection, analytics, etc.)
✅ Export buttons work

---

## NEXT STEPS AFTER DEPLOYMENT

1. **Share with team**: Send app URL
2. **Collect feedback**: Make improvements
3. **Add authentication**: For production use
4. **Upgrade tier**: If exceeding limits
5. **Connect external DB**: For production data
6. **Monitor usage**: Check logs regularly

---

## CONTACT & SUPPORT

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/
- **Your GitHub Issues**: For tracking improvements

---

**Estimated deployment time: 15-20 minutes**

**Your BankSight app will be live and accessible worldwide!** 🚀
