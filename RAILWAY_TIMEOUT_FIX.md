# Railway Backend Timeout - Troubleshooting Guide

## 🐛 Problem
Backend at `https://web-production-98ab3.up.railway.app` is timing out - not responding to requests.

## 🔍 Step-by-Step Diagnosis

### Step 1: Check Railway Logs

1. **Go to Railway Dashboard**
   - https://railway.app/dashboard
   - Click on your backend service

2. **Open Logs Tab**
   - Look for error messages
   - Check if the application started successfully
   - Look for these messages:
     ```
     🚀 Starting Policy Simulator - Complete MVP Demo Server...
     DataLoader initialized with data_dir: /app/data/raw
     ```

3. **Common Issues in Logs:**
   - **Import errors**: Missing dependencies
   - **Data loading errors**: Can't find CSV files
   - **Port errors**: PORT environment variable not set
   - **Python errors**: Syntax errors or exceptions

### Step 2: Check Railway Service Status

1. **In Railway Dashboard:**
   - Check if service shows "Active" and "Deployed"
   - Check if there are any deployment errors
   - Look at the "Metrics" tab for resource usage

2. **Check Environment Variables:**
   - Settings → Variables
   - Verify `PORT` is set (Railway usually sets this automatically)
   - Check if any required variables are missing

### Step 3: Test Backend Directly

```bash
# Test health endpoint (should be fast)
curl --max-time 5 https://web-production-98ab3.up.railway.app/health

# If this times out, the app isn't starting
```

### Step 4: Common Causes & Fixes

#### Cause 1: Data Loading Hanging
**Symptom:** Logs show "DataLoader initialized" but then nothing
**Fix:** Data files might be missing or path is wrong

#### Cause 2: Import Errors
**Symptom:** Logs show "ModuleNotFoundError" or "ImportError"
**Fix:** Check `requirements.txt` has all dependencies

#### Cause 3: Port Not Set
**Symptom:** Logs show port errors
**Fix:** Railway should set PORT automatically, but verify in Settings → Variables

#### Cause 4: Application Crash
**Symptom:** Logs show Python traceback/error
**Fix:** Check the specific error and fix the code

## 🔧 Quick Fixes

### Fix 1: Restart Railway Service

1. Go to Railway Dashboard
2. Click on your service
3. Click "Redeploy" or "Restart"
4. Wait 2-3 minutes
5. Test again: `curl https://web-production-98ab3.up.railway.app/health`

### Fix 2: Check Data Files

1. In Railway, check if `data/raw/` directory exists
2. Verify CSV files are in the repository
3. Check Railway logs for "Data directory exists: True/False"

### Fix 3: Simplify Health Check

The health endpoint should work even if data isn't loaded. If it's timing out, the app isn't starting at all.

## 📋 What to Check in Railway Logs

Look for these messages (in order):

1. ✅ **Build successful**: "Successfully built..."
2. ✅ **Container started**: "Container started"
3. ✅ **Python starting**: "🚀 Starting Policy Simulator..."
4. ✅ **Data loader**: "DataLoader initialized with data_dir: /app/data/raw"
5. ✅ **Server running**: "Uvicorn running on..."

If any step is missing, that's where the problem is.

## 🆘 If Still Not Working

1. **Share Railway Logs**: Copy the last 50-100 lines of logs
2. **Check Build Logs**: Look for errors during Docker build
3. **Verify Dockerfile**: Make sure it's correct
4. **Test Locally**: Try running locally to see if same issue occurs

## 🧪 Test Commands

```bash
# Test 1: Health check (should be instant)
curl --max-time 5 https://web-production-98ab3.up.railway.app/health

# Test 2: Data status (might be slower)
curl --max-time 10 https://web-production-98ab3.up.railway.app/api/data/status

# Test 3: Countries (might be slow if data loading)
curl --max-time 15 https://web-production-98ab3.up.railway.app/api/simulations/countries
```

If Test 1 fails, the app isn't starting. Check Railway logs.
