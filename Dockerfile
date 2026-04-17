# Dockerfile for seeshuraj-avatar-api
# Python 3.11 slim - fast build, small image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps needed by azure-cognitiveservices-speech
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libasound2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose port 8080 (Fly.io default)
EXPOSE 8080

# Start FastAPI with uvicorn on port 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
