# Use Python 3.11.9 base image (explicit version for compatibility)
FROM python:3.11.9-slim

# Install system dependencies for pandas compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Upgrade pip, setuptools, and wheel first to ensure we get pre-built wheels
# Use --prefer-binary to prefer wheels over source builds
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy the rest of the application
COPY . .

# Verify files are copied (for debugging)
RUN ls -la src/backend/comprehensive_demo_server.py || echo "File not found!" && \
    find . -name "comprehensive_demo_server.py" -type f || echo "File search failed"

# Expose port (Railway will set PORT environment variable automatically)
# Using default port 8005, but Railway will override with PORT env var
EXPOSE 8005

# Start the application using run_server.py which handles path setup correctly
CMD ["python", "run_server.py"]
