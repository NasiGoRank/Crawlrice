#!/bin/bash
set -e
MIN_PYTHON_VERSION="3.7"

echo "🚀 Starting global setup for Crawlrice Project..."
echo "WARNING: Installation will be performed globally without a virtual environment."

echo "--- [1/3] Checking Python version..."
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 not found. Please install Python 3 (version ${MIN_PYTHON_VERSION} or higher) first."
    exit 1
fi

CURRENT_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if [ "$(printf '%s\n' "$MIN_PYTHON_VERSION" "$CURRENT_VERSION" | sort -V | head -n1)" != "$MIN_PYTHON_VERSION" ]; then 
    echo "❌ Error: Your Python version is ${CURRENT_VERSION}, but this project requires at least version ${MIN_PYTHON_VERSION}."
    echo "   Please upgrade your Python 3."
    exit 1
fi
echo "✅ Python ${CURRENT_VERSION} found (meets requirement >= ${MIN_PYTHON_VERSION})."

echo "--- [2/3] Installing all libraries from requirements.txt globally..."
pip3 install -r requirements.txt
echo "✅ All dependencies successfully installed."

echo "--- [3/3] Installing the ‘crawlrice’ script as a global command..."
pip3 install -e .
echo "✅ Project successfully installed in editable mode."

echo ""
echo "--- ✨ Setup Complete! ---"
echo "You can now run the ‘crawlrice’ command from any directory."
echo "Example: crawlrice --help"
echo "--------------------------"