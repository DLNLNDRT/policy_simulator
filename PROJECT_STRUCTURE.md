# Project Structure

```
project_root/
├── README.md                          # Main project documentation
├── requirements.txt                   # Core Python dependencies
├── comprehensive_demo_server.py       # Main FastAPI server
├── data_loader.py                     # Data loading utilities
├── env.example                        # Environment variables template
│
├── data/                              # Data files
│   ├── raw/                          # Original CSV datasets
│   └── processed/                    # Processed data (if any)
│
├── src/                               # Source code
│   ├── frontend/                     # React frontend application
│   │   ├── src/                      # React source code
│   │   ├── package.json             # Frontend dependencies
│   │   └── vite.config.ts           # Vite configuration
│   └── backend/                      # Backend API code (unused in current setup)
│
├── deployment/                        # Deployment configurations
│   ├── configs/                      # Platform-specific configs
│   │   ├── vercel.json              # Vercel deployment
│   │   ├── railway.json             # Railway deployment
│   │   └── Dockerfile               # Docker configuration
│   └── guides/                       # Deployment guides
│
├── docs/                              # Documentation
│   ├── architecture/                 # Technical architecture docs
│   ├── features/                     # Feature documentation
│   └── deployment/                   # Deployment documentation
│
├── examples/                          # Example files
│   ├── streamlit_eda_dashboard.py    # Streamlit dashboard
│   └── full_interactive_demo.html    # HTML demo
│
├── scripts/                           # Utility scripts
│   ├── deploy/                       # Deployment scripts
│   └── test/                         # Testing scripts
│
└── requirements/                      # Additional requirements files
    ├── requirements_full_api.txt     # Full API requirements
    ├── requirements_streamlit.txt    # Streamlit requirements
    └── requirements_railway.txt      # Railway requirements
```

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Start server**: `python comprehensive_demo_server.py`
3. **Access frontend**: Visit the Vercel URL in README
4. **Access Streamlit**: Visit the Streamlit URL in README

## Key Files

- `comprehensive_demo_server.py` - Main FastAPI server with all 5 features
- `data_loader.py` - Loads health indicator data from CSV files
- `src/frontend/` - React frontend deployed on Vercel
- `examples/streamlit_eda_dashboard.py` - Streamlit dashboard
