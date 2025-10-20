# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_railway.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_railway.txt

# Copy the rest of the application
COPY . .

# Expose port (Railway will set PORT environment variable)
EXPOSE $PORT

# Start the application
CMD ["python", "comprehensive_demo_server.py"]
