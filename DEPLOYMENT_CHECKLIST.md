# 🚀 BankSight - Streamlit Cloud Deployment Checklist

## Pre-Deployment: Local Validation ✅

- [x] **Virtual Environment**: Python 3.11+ installed and activated
- [x] **Dependencies**: All packages installed (`pip install -r requirements.txt`)
- [x] **App Running Locally**: `streamlit run app.py` works on http://localhost:8501
- [x] **Database**: SQLite database created at `data/banksight.db`
- [x] **Sample Data**: "Load Sample Data" button works
- [x] **Analytics**: All 7 dashboard views operational:
  - Dashboard (overall metrics)
  - Fraud Detection (Isolation Forest results)
  - Customer Analytics (RFM segmentation)
  - Risk Scoring (multi-component model)
  - Transaction Analysis (patterns & trends)
  - Reports (data export)
  - Settings (app configuration)
- [x] **No Errors**: Check logs for any warnings/errors
- [x] **Requirements Updated**: `psycopg2-binary` removed (Streamlit Cloud compatible)

## Step 1: Prepare GitHub Repository

### 1.1 Initialize Git (Run in project root)
```bash
git init
git add .
git commit -m "Initial commit: BankSight Transaction Intelligence Dashboard"
```

### 1.2 Create GitHub Account
- Go to https://github.com/signup
- Create free account if needed
- Verify email

### 1.3 Create New Repository on GitHub
- Go to https://github.com/new
- Repository name: `BankSight` (or your preferred name)
- Description: "Transaction Intelligence Dashboard with Fraud Detection"
- Choose: **Public** (required for Streamlit Cloud free tier)
- Do NOT initialize with README (we have one)
- Click "Create Repository"

### 1.4 Add Remote and Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/BankSight.git
git branch -M main
git push -u origin main
```

**Verify**: Check https://github.com/YOUR_USERNAME/BankSight - should show your code

## Step 2: Set Up Streamlit Cloud Account

### 2.1 Create Streamlit Account
- Go to https://streamlit.io/cloud
- Click "Sign up for free"
- Choose: **GitHub** authentication (easier for linking repos)
- Authorize Streamlit to access your GitHub account

### 2.2 Grant GitHub Permissions
- Streamlit will request access to your repositories
- Click "Authorize streamlit-cloud[bot]"
- This allows Streamlit Cloud to read and deploy your repo

**Verify**: You should see "Deploy an app" button on Streamlit Cloud dashboard

## Step 3: Deploy Your App

### 3.1 Click "Deploy an app"
- Click the blue "Deploy an app" button
- You'll see a form with 3 fields:
  1. **GitHub repo**: `YOUR_USERNAME/BankSight`
  2. **Branch**: `main`
  3. **Main file path**: `app.py`

### 3.2 Configure Deployment
- Click "Advanced settings" (optional but recommended)
- Under "Runtime":
  - Python version: `3.11` (or auto-detect)
- Click "Deploy!"

### 3.3 Watch Deployment
- Streamlit will create your app and install dependencies
- Status shows: "⏳ Please wait..."
- Wait 3-5 minutes for first deployment
- You'll see "🎈 Your app is ready!" when complete

**Your app will be live at**: `https://YOUR_USERNAME-banksight.streamlit.app`

## Step 4: First Access & Testing

### 4.1 Verify App Access
- Navigate to: https://YOUR_USERNAME-banksight.streamlit.app
- Wait for page to load (may take 10-15 seconds first time)
- Should see BankSight logo and navigation menu

### 4.2 Test Core Features
1. **Dashboard**
   - Click "Dashboard" in sidebar
   - Should show metrics immediately

2. **Load Sample Data**
   - Click "Settings" in sidebar
   - Click "Load Sample Data" button
   - Wait 2-3 seconds for data to load
   - Return to Dashboard - should show populated charts

3. **Fraud Detection**
   - Click "Fraud Detection"
   - Should show fraud scores for transactions

4. **Customer Analytics**
   - Click "Customer Analytics"
   - Should show RFM segmentation chart

5. **Export Features**
   - Go to "Reports"
   - Try exporting data (CSV/JSON/Excel)
   - Download should work in your browser

### 4.3 Monitor App Performance
- Check sidebar in Streamlit Cloud:
  - ℹ️ View logs: Shows any errors/warnings
  - ⚙️ Settings: Configure app name, repo visibility
  - 🔄 Rerun on push: Enable auto-redeploy when you push code

## Step 5: Configuration & Optimization (Optional)

### 5.1 Create Streamlit Config
Create `.streamlit/config.toml` in your repository:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
```

### 5.2 Enable Caching for Performance
Already implemented in `app.py`:
- `@st.cache_resource`: Fraud detection engine (loaded once)
- `@st.cache_data`: Sample data and analytics (reused across reruns)

### 5.3 Set Session Timeout
Already configured in `app.py`:
- Rerun automatically on navigation
- Session state persists between interactions

## Step 6: Post-Deployment Monitoring

### 6.1 Check Logs
- On Streamlit Cloud dashboard
- Click your app → View logs
- Look for errors or warnings
- Common issues:
  - "ModuleNotFoundError": Check requirements.txt
  - "FileNotFoundError": Check file paths
  - "Connection refused": Database issues (use SQLite)

### 6.2 Performance Tips
For optimal performance on Streamlit Cloud free tier:
- Avoid loading large files directly
- Use `@st.cache_data` for expensive computations
- Limit sample data to 1000 transactions (currently 2000)
- Profile with: `streamlit run app.py -- --logger.level=debug`

### 6.3 Share Your App
- **Direct link**: https://YOUR_USERNAME-banksight.streamlit.app
- **Share on social media**: Streamlit has built-in share buttons
- **Embed in website**: Use iframe or share link

## Troubleshooting

### App Not Loading / Shows Blank Page
✅ **Solution**:
1. Check Streamlit Cloud logs
2. Verify `app.py` has no syntax errors (`python -m py_compile app.py`)
3. Test locally: `streamlit run app.py`
4. Push fix: `git add .` → `git commit -m "Fix"` → `git push`
5. Streamlit auto-redeployes in 1-2 minutes

### "ModuleNotFoundError: No module named 'X'"
✅ **Solution**:
1. Add module to `requirements.txt`
2. Run locally: `pip install -r requirements.txt`
3. Test: `streamlit run app.py`
4. Commit and push: `git add requirements.txt` → `git commit` → `git push`
5. App redeploys automatically

### "FileNotFoundError: [Errno 2] No such file or directory: 'data/banksight.db'"
✅ **Solution**:
1. This is normal on first run - app creates it automatically
2. Click "Load Sample Data" in Settings
3. Database persists between runs in Streamlit Cloud
4. If it keeps failing, check `setup-sqlite.py` execution

### App Runs Slowly / Times Out
✅ **Solution**:
1. Reduce sample data size (line in `app.py`): `NUM_CUSTOMERS = 500` (was 100)
2. Enable caching with `@st.cache_resource`
3. Avoid recomputing fraud detection on every run
4. Use `st.session_state` to persist computations

### Database Locked / Multiple Access
✅ **Solution**:
1. SQLite on Streamlit Cloud is single-user only
2. No multiple simultaneous connections
3. App manages this automatically via connection pool
4. For production: Upgrade to PostgreSQL on Azure/AWS

## Emergency Redeploy

If app breaks after push:
```bash
# Locally, revert last commit:
git revert HEAD
git push

# Streamlit auto-redeployes within 1-2 minutes
```

Or manually trigger redeploy in Streamlit Cloud:
1. Go to app settings
2. Click "Reboot app"
3. App restarts within 30 seconds

## Success Metrics ✅

Your deployment is successful when:
- ✅ App loads at `https://YOUR_USERNAME-banksight.streamlit.app`
- ✅ All 7 navigation tabs work
- ✅ "Load Sample Data" populates the database
- ✅ Fraud detection generates scores
- ✅ Charts and analytics render properly
- ✅ Data export downloads files
- ✅ No errors in Streamlit Cloud logs

## Next Steps After Deployment

1. **Customize Styling** (optional):
   - Modify CSS in `app.py` lines 100-200
   - Change colors, fonts, spacing
   - Push changes to auto-redeploy

2. **Add Real Data** (advanced):
   - Modify `load_sample_data()` to connect to real database
   - Use environment secrets for credentials
   - Implement data refresh schedule

3. **Monitor Usage** (optional):
   - Streamlit Cloud shows app metrics
   - Track user visits and reruns
   - Monitor resource usage (CPU, memory, disk)

4. **Scale Up** (when needed):
   - Upgrade to Streamlit Community Cloud Pro ($10/month)
   - Get dedicated resources
   - Higher CPU, memory, storage limits

---

## Quick Command Reference

```bash
# Local testing
streamlit run app.py

# Git operations
git add .
git commit -m "Your message"
git push

# Check status
git status
git log --oneline -5

# Update requirements
pip freeze > requirements.txt
```

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **GitHub Help**: https://docs.github.com
- **BankSight Docs**: See `DEVELOPMENT.md` and `README.md`

---

**Deployment Date**: [Today's Date]
**Status**: Ready for Production ✅
**Next Review**: After first 100 users or 1 week
