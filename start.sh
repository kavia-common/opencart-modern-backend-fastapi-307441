#!/bin/bash
# Startup script for FastAPI backend with proxy support

# Exit on error
set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Set default values if not provided
PORT=${PORT:-3003}
HOST=${HOST:-0.0.0.0}
WORKERS=${WORKERS:-1}
LOG_LEVEL=${LOG_LEVEL:-info}

echo "========================================="
echo "Starting OpenCart Modern API Backend"
echo "========================================="
echo "Host: $HOST"
echo "Port: $PORT"
echo "Workers: $WORKERS"
echo "Log Level: $LOG_LEVEL"
echo "Root Path: ${ROOT_PATH:-(not set)}"
echo "========================================="

# Start uvicorn with proxy support
# --proxy-headers: Trust X-Forwarded-* headers from reverse proxy
# --forwarded-allow-ips: Which IPs to trust for proxy headers
uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level "$LOG_LEVEL" \
    --proxy-headers \
    --forwarded-allow-ips '*' \
    --reload
