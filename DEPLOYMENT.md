# Policy Simulator - Deployment Guide

## 🚀 Quick Start

### Local Development
```bash
# Backend (Terminal 1)
cd policy_simulator
python run_server.py

# Frontend (Terminal 2)  
cd policy_simulator/src/frontend
npm install
npm run dev

# Analytics Dashboard (Terminal 3)
cd policy_simulator
python run_dashboard.py
```

### URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Analytics Dashboard**: http://localhost:8501

## 🌐 Production Deployment

### 1. React Frontend (Vercel)
- **URL**: https://policy-simulator-68gdbw18t-dlnlndrts-projects.vercel.app/
- **Config**: `vercel.json`
- **Build**: Automatic from GitHub

### 2. FastAPI Backend (Railway)
- **Config**: `Dockerfile`, `requirements.txt`
- **Build**: Automatic from GitHub
- **Health Check**: `/health`

### 3. Streamlit Dashboard (Streamlit Cloud)
- **Config**: `requirements_streamlit_cloud.txt`
- **File**: `scripts/streamlit_eda_dashboard.py`

## 📁 Project Structure

```
policy_simulator/
├── src/
│   ├── backend/          # FastAPI backend
│   └── frontend/         # React frontend
├── data/                 # Health indicator datasets
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── deployment/           # Deployment configs
├── Dockerfile           # Railway deployment
├── requirements.txt     # Main dependencies
└── README.md           # Project overview
```

## 🔧 Configuration Files

- `Dockerfile` - Railway backend deployment
- `vercel.json` - Vercel frontend deployment  
- `Procfile` - Heroku deployment (if needed)
- `runtime.txt` - Python version specification
- `requirements_streamlit_cloud.txt` - Streamlit Cloud dependencies

## 🛠️ Troubleshooting

### Railway Issues
- Check build logs for dependency conflicts
- Ensure Dockerfile is in root directory
- Verify PORT environment variable usage

### Vercel Issues  
- Check build logs for TypeScript errors
- Verify environment variables are set
- Ensure API URLs are correct

### Streamlit Cloud Issues
- Check requirements_streamlit_cloud.txt
- Verify file paths in streamlit_eda_dashboard.py
- Check data file accessibility
