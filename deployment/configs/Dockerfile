# Use Python 3.11 base image with build tools
FROM python:3.11-slim

# Install system dependencies for pandas compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (Railway will set PORT environment variable)
EXPOSE $PORT

# Start the application
CMD ["python", "comprehensive_demo_server.py"]
