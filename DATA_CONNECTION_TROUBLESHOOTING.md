# Data Connection Troubleshooting Guide

## 🔍 Diagnosing Data Connection Issues

If the frontend cannot load countries or data, follow these steps:

### Step 1: Check Backend Health

Test if the backend is running:
```bash
curl https://web-production-21904.up.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "policy-simulator-mvp",
  ...
}
```

### Step 2: Check Data Status

Test if data is loading correctly:
```bash
curl https://web-production-21904.up.railway.app/api/data/status
```

This will show:
- Data directory path
- Whether directory exists
- Available data files
- Number of countries loaded
- Any errors

**Expected Response:**
```json
{
  "status": "ok",
  "data_directory": "/app/data/raw",
  "data_directory_exists": true,
  "data_files": ["Life Expectancy.csv", "Density of Doctors.csv", ...],
  "countries_loaded": 50,
  "countries_error": null
}
```

### Step 3: Check Countries Endpoint

Test the countries endpoint directly:
```bash
curl https://web-production-21904.up.railway.app/api/simulations/countries
```

Should return an array of countries:
```json
[
  {
    "code": "PRT",
    "name": "Portugal",
    "baseline": {...}
  },
  ...
]
```

### Step 4: Check Frontend Environment Variable

1. **In Vercel Dashboard:**
   - Go to Settings → Environment Variables
   - Verify `VITE_API_BASE_URL` is set to: `https://web-production-21904.up.railway.app`
   - Make sure it's set for all environments (Production, Preview, Development)

2. **In Browser Console:**
   - Open your Vercel app
   - Open DevTools (F12) → Console
   - Check for API connection errors
   - Look for logs showing the API URL being used

### Step 5: Check Railway Logs

1. Go to Railway dashboard
2. Open your backend service
3. Check the logs for:
   - Data directory path
   - File existence messages
   - Any errors loading data
   - Countries count

Look for messages like:
```
DataLoader initialized with data_dir: /app/data/raw
Data directory exists: True
Files in data directory: ['Life Expectancy.csv', ...]
```

## 🐛 Common Issues

### Issue 1: "No countries available" in Frontend

**Possible Causes:**
1. Data files not copied to Railway
2. Data directory path incorrect
3. Data loader can't find files

**Solutions:**
1. Check Railway logs for data directory path
2. Verify data files are in the repository
3. Check `/api/data/status` endpoint response
4. Ensure Dockerfile copies data directory (it should with `COPY . .`)

### Issue 2: "API URL not configured" Error

**Cause:** `VITE_API_BASE_URL` not set in Vercel

**Solution:**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Add `VITE_API_BASE_URL` = `https://web-production-21904.up.railway.app`
3. Select all environments
4. Redeploy

### Issue 3: CORS Errors in Browser Console

**Cause:** Backend CORS not configured correctly

**Solution:**
- Backend already has `allow_origins=["*"]` which should allow all origins
- If still getting CORS errors, check Railway logs

### Issue 4: 404 Errors on API Calls

**Cause:** Wrong API URL or endpoint doesn't exist

**Solution:**
1. Verify Railway backend URL is correct
2. Test endpoint directly with curl
3. Check Railway logs for route registration

### Issue 5: Empty Countries Array

**Cause:** Data files not loading or no data found

**Solution:**
1. Check `/api/data/status` endpoint
2. Verify data files exist in `data/raw/` directory
3. Check Railway logs for data loading errors
4. Ensure CSV files have correct format

## 🔧 Quick Fixes

### Fix 1: Rebuild Railway Deployment

1. Go to Railway dashboard
2. Click on your service
3. Click "Redeploy"
4. Wait for build to complete
5. Check logs for data loading messages

### Fix 2: Verify Data Files in Repository

```bash
# Check if data files are in git
git ls-files data/raw/

# Should show:
# data/raw/Life Expectancy.csv
# data/raw/Density of Doctors.csv
# etc.
```

### Fix 3: Test Locally

```bash
# Start backend locally
cd policy_simulator
python src/backend/comprehensive_demo_server.py

# Test endpoints
curl http://localhost:8005/api/data/status
curl http://localhost:8005/api/simulations/countries
```

## 📊 Expected Data Files

The following files should exist in `data/raw/`:
- `Life Expectancy.csv`
- `Density of Doctors.csv`
- `Density of nurses and midwives.csv`
- `Density of pharmacists.csv`
- `Density.csv`
- `Government Spending.csv`
- `Access to affordable medicine.csv`
- `Cause of Death.xlsx`

## ✅ Verification Checklist

- [ ] Backend health check returns "healthy"
- [ ] `/api/data/status` shows data files exist
- [ ] `/api/data/status` shows countries_loaded > 0
- [ ] `/api/simulations/countries` returns array of countries
- [ ] `VITE_API_BASE_URL` set in Vercel dashboard
- [ ] Frontend shows countries in dropdown
- [ ] No CORS errors in browser console
- [ ] No 404 errors in browser console

## 🆘 Still Having Issues?

1. Check Railway logs for detailed error messages
2. Check Vercel build logs for frontend issues
3. Use browser DevTools Network tab to see API requests
4. Test endpoints directly with curl or Postman
5. Check `/api/data/status` for data loading diagnostics
