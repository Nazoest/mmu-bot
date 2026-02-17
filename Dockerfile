# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Webdriver manager config
    WDM_LOCAL=1 \
    # Chrome options for Docker
    CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/bin/google-chrome

# Install system dependencies including Google Chrome
# Install system dependencies including Chromium and Chromium Driver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome options env vars
ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_PATH=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security (optional but recommended, though Selenium sometimes needs permissions)
# For simplicity with Chrome sandbox issues, we'll run as root but verify sandbox settings in code
# Or we can create a user:
# RUN useradd -m appuser
# USER appuser

# Environment variables should be passed at runtime, but we can set defaults
ENV MMU_LOGIN_INTERVAL=45

# Command to run the course registration bot
CMD ["python", "course_registration_bot.py"]
