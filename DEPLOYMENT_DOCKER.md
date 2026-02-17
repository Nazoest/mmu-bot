# Docker Deployment Instructions for MMU Bot

This guide explains how to run the MMU Student Portal Bot in a Docker container. This is the most reliable way to run the bot in the background as it handles all dependencies (Python, Chrome, WebDriver) automatically.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

## Quick Start (with Docker Compose)

1. **Configure Credentials**:
   Ensure you have a `.env` file in the project directory with your credentials. If not, copy `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env and add your MMU_REG_NUMBER and MMU_PASSWORD
   ```

2. **Build and Run**:
   Open a terminal in the project directory and run:
   ```bash
   docker-compose up -d --build
   ```
   - `-d` runs it in detached mode (background).
   - `--build` ensures the image is rebuilt if you changed files.

3. **Check Logs**:
   To see what the bot is doing:
   ```bash
   docker-compose logs -f
   ```
   (Press `Ctrl+C` to exit logs)

4. **Stop the Bot**:
   ```bash
   docker-compose down
   ```

## Manual Docker Run (without Compose)

If you prefer using raw Docker commands:

1. **Build the Image**:
   ```bash
   docker build -t mmubot .
   ```

2. **Run the Container**:
   You need to pass your credentials as environment variables:
   ```bash
   docker run -d \
     --name mmubot_container \
     --restart unless-stopped \
     --shm-size=2gb \
     -e MMU_REG_NUMBER="your_reg_number" \
     -e MMU_PASSWORD="your_password" \
     mmubot
   ```

   *Note: `--shm-size=2gb` is important for Chrome stability.*

## Troubleshooting

- **Chrome Crashes**: If you see errors about Chrome crashing, ensure you are using `--shm-size=2gb` (already handled in `docker-compose.yml`).
- **Timezone**: The container uses UTC by default. To use your local time, add this to `docker-compose.yml`:
  ```yaml
  environment:
    - TZ=Africa/Nairobi  # Or your timezone
  ```
- **Login Failures**: Check `docker-compose logs` to see the screenshots or error messages (if screenshot saving is enabled).
