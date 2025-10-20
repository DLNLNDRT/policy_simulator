#!/usr/bin/env python3
"""
Policy Simulator - Server Startup Script
Run this script to start the main FastAPI server.
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))

# Import and run the server
from comprehensive_demo_server import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8005))
    print(f"🚀 Starting Policy Simulator Server...")
    print(f"📊 Server will be available at: http://localhost:{port}")
    print(f"📚 API Documentation at: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
