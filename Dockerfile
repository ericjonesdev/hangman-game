# Use official Python 3.9 image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies (needed for gspread)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary files (excludes creds.json)
COPY *.py ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    gspread \
    google-auth \
    google-auth-oauthlib \
    google-api-python-client

# Set environment variables
ENV PYTHONUNBUFFERED=1
# ENV GOOGLE_CREDS=""  # Not needed - Fly.io secrets auto-inject

# Run the game
CMD ["python", "hangman.py"]