#!/bin/bash

# Backend Test Runner Script
# Executes the full FastAPI backend test suite

set -e

echo "================================"
echo "FastAPI Backend Test Suite"
echo "================================"

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing test dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run tests with coverage
echo ""
echo "Running tests..."
echo "--------------------------------"

# Run all tests
pytest -v --tb=short

echo ""
echo "================================"
echo "Test execution complete!"
echo "================================"
