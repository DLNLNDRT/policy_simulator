# Quick Fix: "Failed to fetch" Error

## 🚨 Immediate Steps

### Step 1: Set Environment Variable in Vercel (MOST COMMON FIX)

1. **Go to Vercel Dashboard**
   - https://vercel.com/dashboard
   - Click on your `policy_simulator` project

2. **Open Settings → Environment Variables**
   - Click **Settings** (gear icon)
   - Click **Environment Variables** in left sidebar

3. **Add the Variable**
   - Click **Add New**
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://web-production-21904.up.railway.app`
   - **Environment**: Select **ALL** (Production, Preview, Development)
   - Click **Save**

4. **Redeploy**
   - Go to **Deployments** tab
   - Click **⋯** (three dots) on latest deployment
   - Click **Redeploy**
   - Wait for deployment to complete

### Step 2: Verify Backend is Running

Test if Railway backend is accessible:
```bash
curl https://web-production-21904.up.railway.app/health
```

**Expected Response:**
```json
{"status":"healthy","service":"policy-simulator-mvp",...}
```

**If this fails:**
- Backend is down or Railway URL changed
- Check Railway dashboard for service status
- Get the correct Railway URL from Railway dashboard

### Step 3: Check Browser Console

1. Open your Vercel app
2. Open DevTools (F12)
3. Go to **Console** tab
4. Look for:
   - `API_BASE_URL value: ...` - Should show the Railway URL
   - `Fetching countries from: ...` - Should show full URL
   - Any CORS errors
   - Any network errors

### Step 4: Check Network Tab

1. In DevTools, go to **Network** tab
2. Refresh the page
3. Look for requests to `/api/simulations/countries`
4. Check:
   - **Status**: Should be 200 (not CORS error or failed)
   - **URL**: Should be `https://web-production-21904.up.railway.app/api/simulations/countries`
   - **Response**: Should show countries array

## 🔍 What the New Error Messages Mean

### "Backend server timeout"
- Backend is not responding
- Check Railway dashboard - service might be down
- Check Railway logs for errors

### "Cannot reach backend server"
- Network issue or wrong URL
- Verify Railway URL is correct
- Check if backend is running

### "Network error: Cannot connect to backend"
- CORS issue or network problem
- Backend CORS should allow all origins (already configured)
- Check browser console for CORS errors

### "HTTP error! status: XXX"
- Backend is reachable but returned an error
- Check Railway logs for the error
- Status 404 = endpoint not found
- Status 500 = server error

## ✅ Verification Checklist

After setting the environment variable and redeploying:

- [ ] Environment variable `VITE_API_BASE_URL` set in Vercel
- [ ] Variable set for all environments (Production, Preview, Development)
- [ ] Vercel deployment completed successfully
- [ ] Backend health check works: `curl https://web-production-21904.up.railway.app/health`
- [ ] Browser console shows correct API URL
- [ ] Network tab shows successful API requests
- [ ] Countries dropdown is populated

## 🆘 Still Not Working?

1. **Check Railway Backend:**
   - Go to Railway dashboard
   - Verify service is running
   - Check logs for errors
   - Get the correct Railway URL

2. **Verify Environment Variable:**
   - In Vercel, check Environment Variables again
   - Make sure it's spelled exactly: `VITE_API_BASE_URL`
   - Make sure value is exactly: `https://web-production-21904.up.railway.app`
   - No trailing slashes!

3. **Test Backend Directly:**
   ```bash
   # Test health
   curl https://web-production-21904.up.railway.app/health
   
   # Test countries endpoint
   curl https://web-production-21904.up.railway.app/api/simulations/countries
   ```

4. **Check Browser Console:**
   - Look for the exact error message
   - Check what API URL is being used
   - Look for CORS errors

5. **Check Railway Logs:**
   - Look for data loading errors
   - Check if data files are found
   - Verify server started correctly
