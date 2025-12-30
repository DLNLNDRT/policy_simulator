# Project Review - Issues & Recommendations

**Date:** December 30, 2024  
**Reviewer:** AI Code Review  
**Status:** Issues Identified

## 🔴 Critical Issues

### 1. Missing `env.example` File
**Location:** Referenced in README.md line 105, 123  
**Issue:** README mentions `cp env.example .env` but the file doesn't exist  
**Impact:** Users can't set up environment variables properly  
**Fix:** Create `env.example` with all required environment variables

### 2. Port Number Inconsistency
**Location:** Multiple files  
**Issue:** 
- README.md says backend runs on port 8000 (line 135)
- `comprehensive_demo_server.py` defaults to port 8005 (line 1714)
- `run_server.py` defaults to port 8005 (line 18)
- DEPLOYMENT.md says port 8000 (line 23)

**Impact:** Confusion for developers, documentation doesn't match code  
**Fix:** Standardize on port 8005 (or update code to use 8000) and update all documentation

### 3. Dockerfile CMD Issue
**Location:** `Dockerfile` line 35  
**Issue:** Dockerfile runs `python src/backend/comprehensive_demo_server.py` directly, but this file needs to be run as a module or the working directory needs to be set correctly  
**Impact:** May fail in Docker container if Python path isn't set correctly  
**Fix:** Use `run_server.py` instead, or set PYTHONPATH, or use `python -m` syntax

## 🟡 Medium Priority Issues

### 4. Missing Procfile
**Location:** PROJECT_STRUCTURE.md line 38, DEPLOYMENT.md line 62  
**Issue:** Documentation mentions Procfile but it doesn't exist in the repository  
**Impact:** Confusion, but not critical since Railway uses Dockerfile  
**Fix:** Either create Procfile for Heroku compatibility, or remove references from docs

### 5. Import Path Fragility
**Location:** `comprehensive_demo_server.py` line 20  
**Issue:** Uses `from utils.data_loader import data_loader` which relies on Python path being set correctly  
**Impact:** May fail if run from different directories  
**Fix:** Use absolute imports or ensure PYTHONPATH is set, or use `run_server.py` which handles this

### 6. Dockerfile EXPOSE Issue
**Location:** `Dockerfile` line 32  
**Issue:** `EXPOSE $PORT` won't work - EXPOSE needs a numeric value  
**Impact:** Docker build warning, but Railway handles port mapping automatically  
**Fix:** Use `EXPOSE 8005` or remove EXPOSE (Railway doesn't need it)

## 🟢 Low Priority / Documentation Issues

### 7. README Installation Instructions
**Location:** README.md line 127  
**Issue:** Says `python comprehensive_demo_server.py` but should be `python run_server.py`  
**Impact:** Users might run the wrong file  
**Fix:** Update to use `run_server.py`

### 8. Inconsistent Server Startup Methods
**Location:** Multiple files  
**Issue:** 
- `run_server.py` exists and handles path setup
- `comprehensive_demo_server.py` has `if __name__ == "__main__"` block
- Dockerfile runs server directly

**Impact:** Multiple ways to start server, some may not work in all contexts  
**Fix:** Standardize on `run_server.py` for local dev, update Dockerfile to use it

### 9. Documentation References to Old Project Name
**Location:** `src/backend/core/config.py` line 15  
**Issue:** Still says "Policy Simulation Assistant" instead of "Policy Simulator"  
**Impact:** Minor branding inconsistency  
**Fix:** Update to "Policy Simulator"

## ✅ What's Working Well

1. ✅ Project structure is well organized
2. ✅ Requirements.txt is comprehensive
3. ✅ Frontend configuration looks good
4. ✅ Railway and Vercel configs are present
5. ✅ Data loader handles path resolution gracefully
6. ✅ CORS is properly configured
7. ✅ Health check endpoint exists
8. ✅ No linter errors found

## 📋 Recommended Fixes Priority

1. **High Priority:**
   - Create `env.example` file
   - Fix port number inconsistency
   - Fix Dockerfile CMD

2. **Medium Priority:**
   - Standardize server startup method
   - Fix Dockerfile EXPOSE
   - Update README installation instructions

3. **Low Priority:**
   - Create or remove Procfile references
   - Update branding in config.py
   - Clean up documentation inconsistencies

## 🔧 Quick Fixes Summary

```bash
# 1. Create env.example
# 2. Update README port references to 8005
# 3. Update Dockerfile CMD to use run_server.py
# 4. Fix Dockerfile EXPOSE to use numeric value
# 5. Update README installation to use run_server.py
```
