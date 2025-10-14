#!/bin/bash

# Streamlit EDA Dashboard Launcher
# Policy Simulation Assistant - ADAPT Framework Analysis

echo "🚀 Starting Policy Simulation Assistant EDA Dashboard..."
echo "📊 Loading data from adapt_context/data and adapt_context/artifacts"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing requirements..."
    pip install -r requirements_streamlit.txt
fi

# Check if data directory exists
if [ ! -d "adapt_context/data" ]; then
    echo "❌ Data directory not found: adapt_context/data"
    echo "Please ensure the data files are in the correct location."
    exit 1
fi

# Check if artifacts directory exists
if [ ! -d "adapt_context/artifacts" ]; then
    echo "❌ Artifacts directory not found: adapt_context/artifacts"
    echo "Please ensure the artifact files are in the correct location."
    exit 1
fi

echo "✅ Data and artifacts directories found"
echo "🌐 Starting Streamlit dashboard..."
echo "📱 Dashboard will be available at: http://localhost:8501"
echo ""

# Start the Streamlit dashboard
streamlit run streamlit_eda_dashboard.py --server.port 8501 --server.address localhost
