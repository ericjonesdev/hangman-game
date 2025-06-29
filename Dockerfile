# Use official Python 3.9 image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies (needed for gspread)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy all files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    gspread \
    google-auth \
    google-auth-oauthlib \
    google-api-python-client

# Make sure creds.json exists (critical for Google Sheets)
RUN if [ ! -f "creds.json" ]; then \
    echo "ERROR: creds.json missing! Please mount this file." && exit 1; \
    fi

# Set environment variable for Python output
ENV PYTHONUNBUFFERED=1

# Run the game
CMD ["python", "hangman.py"]