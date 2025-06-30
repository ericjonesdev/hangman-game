FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy ONLY necessary files (change if your filename is different)
COPY run.py .
COPY hangman_art.py .
COPY hangman_words.py .
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir \
    gspread \
    google-auth \
    google-auth-oauthlib \
    google-api-python-client

# Run the game
CMD ["python", "-u", "run.py"]