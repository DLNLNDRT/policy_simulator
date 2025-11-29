# Frontend-Backend Connection Guide

## 🔗 How They Connect - Step by Step

### Step 1: Frontend Reads Environment Variable
**Location:** `src/frontend/src/pages/SimulationPage.tsx` (line 49)
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
```

**What happens:**
- Vite reads `VITE_API_BASE_URL` from environment variables **at build time**
- This value gets embedded into the JavaScript bundle
- If not set, it defaults to empty string `''`

**⚠️ CRITICAL:** Vite environment variables must be available **during build**, not runtime!

### Step 2: Frontend Makes API Call
**Location:** `src/frontend/src/pages/SimulationPage.tsx` (line 71-72)
```typescript
console.log('Fetching countries from:', `${API_BASE_URL}/api/simulations/countries`)
const response = await fetch(`${API_BASE_URL}/api/simulations/countries`)
```

**What happens:**
- Frontend constructs URL: `{API_BASE_URL}/api/simulations/countries`
- Makes HTTP GET request to backend
- Example: `https://web-production-21904.up.railway.app/api/simulations/countries`

### Step 3: Backend Receives Request
**Location:** `src/backend/comprehensive_demo_server.py` (line 405)
```python
@app.get("/api/simulations/countries")
async def get_simulation_countries():
```

**What happens:**
- FastAPI receives GET request at `/api/simulations/countries`
- CORS middleware allows request (configured to allow all origins)
- Endpoint processes request

### Step 4: Backend Loads Data
**Location:** `src/backend/comprehensive_demo_server.py` (line 410)
```python
real_countries = get_countries_data()
```

**What happens:**
- Calls `data_loader.get_available_countries()`
- Loads data from CSV files in `data/raw/` directory
- Returns list of countries with baseline data

### Step 5: Backend Returns Response
**Location:** `src/backend/comprehensive_demo_server.py` (line 420)
```python
return countries  # Returns JSON array
```

**What happens:**
- FastAPI serializes Python list to JSON
- Returns HTTP 200 response with JSON body
- Example response:
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

### Step 6: Frontend Receives Response
**Location:** `src/frontend/src/pages/SimulationPage.tsx` (line 120-130)
```typescript
const countriesData = await response.json()
setCountries(countriesData)
```

**What happens:**
- Frontend parses JSON response
- Updates React state with countries
- Country dropdown gets populated

---

## 🐛 Debugging Steps

### Step 1: Verify Environment Variable in Vercel

1. **Go to Vercel Dashboard**
   - https://vercel.com/dashboard
   - Click your `policy_simulator` project

2. **Check Environment Variables**
   - Settings → Environment Variables
   - Look for `VITE_API_BASE_URL`
   - **Value should be:** `https://web-production-21904.up.railway.app` (or your Railway URL)
   - **Must be set for:** All environments (Production, Preview, Development)

3. **If Missing or Wrong:**
   - Click "Add New" or "Edit"
   - Key: `VITE_API_BASE_URL`
   - Value: Your Railway backend URL
   - Environment: Select ALL
   - Save

4. **Redeploy**
   - Go to Deployments tab
   - Click "Redeploy" on latest deployment
   - ⚠️ **IMPORTANT:** Environment variables only work if set BEFORE build!

### Step 2: Verify Railway Backend is Running

1. **Check Railway Dashboard**
   - https://railway.app/dashboard
   - Open your backend service
   - Verify it's "Active" and "Deployed"

2. **Get Correct Railway URL**
   - Service → Settings → Networking
   - Copy the "Public Domain" URL
   - It might be different from `web-production-21904.up.railway.app`

3. **Test Backend Health**
   ```bash
   curl https://YOUR-RAILWAY-URL/health
   ```
   Should return: `{"status":"healthy",...}`

4. **Test Countries Endpoint**
   ```bash
   curl https://YOUR-RAILWAY-URL/api/simulations/countries
   ```
   Should return array of countries

### Step 3: Check Browser Console

1. **Open Your Vercel App**
   - Go to your deployed Vercel URL

2. **Open Browser DevTools**
   - Press F12 or Right-click → Inspect
   - Go to "Console" tab

3. **Look for These Messages:**
   ```
   API_BASE_URL value: https://web-production-21904.up.railway.app
   Fetching countries from: https://web-production-21904.up.railway.app/api/simulations/countries
   Backend health check passed: {...}
   Countries loaded: 50
   ```

4. **Check for Errors:**
   - Red error messages
   - "Failed to fetch" errors
   - CORS errors
   - Network errors

### Step 4: Check Network Tab

1. **In DevTools, Go to "Network" Tab**
2. **Refresh the Page**
3. **Look for Request to `/api/simulations/countries`**
   - **Status:** Should be 200 (green), not red
   - **URL:** Should show full Railway URL
   - **Response:** Click to see if countries are returned

4. **If Request Fails:**
   - Check Status code (404, 500, CORS error?)
   - Check if URL is correct
   - Check Response tab for error message

### Step 5: Verify Data Files Exist

1. **Check Railway Logs**
   - Railway Dashboard → Your Service → Logs
   - Look for:
     ```
     DataLoader initialized with data_dir: /app/data/raw
     Data directory exists: True
     Files in data directory: ['Life Expectancy.csv', ...]
     ```

2. **Test Data Status Endpoint**
   ```bash
   curl https://YOUR-RAILWAY-URL/api/data/status
   ```
   Should show:
   ```json
   {
     "data_directory_exists": true,
     "data_files": ["Life Expectancy.csv", ...],
     "countries_loaded": 50
   }
   ```

---

## ✅ Complete Verification Checklist

- [ ] `VITE_API_BASE_URL` set in Vercel dashboard
- [ ] Environment variable set for ALL environments
- [ ] Vercel deployment completed AFTER setting env var
- [ ] Railway backend service is "Active" and "Deployed"
- [ ] Railway backend URL is correct (test with curl)
- [ ] Backend health check works: `/health` returns 200
- [ ] Backend countries endpoint works: `/api/simulations/countries` returns data
- [ ] Browser console shows correct API_BASE_URL value
- [ ] Browser console shows "Backend health check passed"
- [ ] Network tab shows successful API requests (status 200)
- [ ] Data files exist in Railway (check `/api/data/status`)
- [ ] No CORS errors in browser console
- [ ] No "Failed to fetch" errors

---

## 🔧 Common Issues & Fixes

### Issue 1: "API URL not configured"
**Cause:** `VITE_API_BASE_URL` not set in Vercel
**Fix:** Set it in Vercel dashboard and redeploy

### Issue 2: "Failed to fetch"
**Cause:** Backend not reachable or wrong URL
**Fix:** 
- Verify Railway backend is running
- Check Railway URL is correct
- Update `VITE_API_BASE_URL` in Vercel

### Issue 3: "Backend health check failed"
**Cause:** Backend is down or URL wrong
**Fix:** Check Railway dashboard, verify service is running

### Issue 4: "No countries returned from API"
**Cause:** Data files not loading in Railway
**Fix:** Check Railway logs, verify data files exist, check `/api/data/status`

### Issue 5: CORS Error
**Cause:** Backend CORS not configured (shouldn't happen - already configured)
**Fix:** Backend already has `allow_origins=["*"]`, but verify it's working

### Issue 6: Empty Countries Array
**Cause:** Data loader can't find files or no data
**Fix:** Check Railway logs for data loading errors, verify CSV files exist

---

## 🚀 Quick Test Commands

```bash
# Test backend health
curl https://YOUR-RAILWAY-URL/health

# Test data status
curl https://YOUR-RAILWAY-URL/api/data/status

# Test countries endpoint
curl https://YOUR-RAILWAY-URL/api/simulations/countries

# Test with verbose output (see headers)
curl -v https://YOUR-RAILWAY-URL/api/simulations/countries
```

---

## 📝 Next Steps

1. **Follow the checklist above** - check each item
2. **Test backend directly** - use curl commands
3. **Check browser console** - look for error messages
4. **Check Network tab** - see actual API requests
5. **Verify Railway logs** - check for data loading issues

If all checks pass but still not working, share:
- Browser console errors
- Network tab screenshot
- Railway logs
- curl test results
