# Use the official Python image as a base
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements if present, else use pyproject.toml
COPY pyproject.toml ./
COPY uv.lock ./
# Copy requirements.txt if present
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Copy .env file for environment variables
COPY .env .env

# Expose port (if your server runs on 8000, change as needed)
EXPOSE 8000

# Default command (update as needed)
CMD ["python", "main.py"]
