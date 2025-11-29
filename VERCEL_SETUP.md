# Vercel Frontend Setup Guide

## 🔧 Environment Variable Configuration

The frontend needs the `VITE_API_BASE_URL` environment variable to connect to the Railway backend.

### ⚠️ IMPORTANT: Set Environment Variable in Vercel Dashboard

Vite environment variables must be available at **build time**, so they need to be set in Vercel's dashboard, not just in `vercel.json`.

### Steps to Set Environment Variable:

1. **Go to Vercel Dashboard**
   - Navigate to your project: https://vercel.com/dashboard
   - Click on your `policy_simulator` project

2. **Open Settings**
   - Click on **Settings** (gear icon) in the top menu
   - Click on **Environment Variables** in the left sidebar

3. **Add Environment Variable**
   - Click **Add New**
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://web-production-21904.up.railway.app` (or your Railway URL)
   - **Environment**: Select all (Production, Preview, Development)
   - Click **Save**

4. **Redeploy**
   - Go to **Deployments** tab
   - Click the three dots (⋯) on the latest deployment
   - Click **Redeploy**
   - Or push a new commit to trigger automatic redeploy

## 🔍 Verify Configuration

After redeploying, check:

1. **Build Logs**: The environment variable should be available during build
2. **Browser Console**: Open your Vercel app and check the browser console
   - Look for any API connection errors
   - Check if `import.meta.env.VITE_API_BASE_URL` has a value

## 🐛 Troubleshooting

### Issue: Countries not loading / API calls failing

**Possible Causes:**
1. Environment variable not set in Vercel dashboard
2. Wrong Railway URL
3. Backend not running or CORS issues
4. Environment variable not available at build time

**Solutions:**
1. ✅ Set `VITE_API_BASE_URL` in Vercel dashboard (not just vercel.json)
2. ✅ Verify Railway backend is running: Check `https://web-production-21904.up.railway.app/health`
3. ✅ Check browser console for CORS errors
4. ✅ Redeploy after setting environment variable

### Check Railway Backend

Test if backend is accessible:
```bash
curl https://web-production-21904.up.railway.app/health
```

Should return: `{"status":"healthy"}`

### Check Environment Variable in Build

In Vercel build logs, you should see the environment variable being used. If not, it wasn't set correctly in the dashboard.

## 📝 Current Configuration

- **Frontend URL**: https://policy-simulator-68gdbw18t-dlnlndrts-projects.vercel.app/
- **Backend URL**: https://web-production-21904.up.railway.app
- **Root Directory**: `src/frontend` (set in Vercel dashboard)
- **Environment Variable**: `VITE_API_BASE_URL` (must be set in dashboard)
