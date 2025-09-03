#!/bin/bash
set -e

echo "🚀 Starting global setup for Crawlrice..."
echo "WARNING: This script will require sudo password and install packages globally."

echo "--- Checking for Python 3 and Pip3..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "❌ Error: python3 or pip3 not found."
    read -p "   Do you want to try installing them now? (y/n) " -n 1 -r
    echo "" 

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v apt-get &> /dev/null; then
            echo "   -> Installing Python 3, Pip, and Venv using apt-get..."
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv 
            echo "   ✅ Python 3 installed successfully."
        else
            echo "   ❌ Automatic installation is not supported on this OS (Debian/Ubuntu only)."
            echo "      Please install Python 3.7+ manually and rerun this script."
            exit 1
        fi
    else
        echo "   Installation cancelled by user."
        exit 1
    fi
else
    echo "✅ Python 3 and Pip3 found."
fi

echo "--- Installing dependencies from requirements.txt..."
sudo pip3 install -r requirements.txt --break-system-packages --ignore-installed
echo "✅ Dependencies installed successfully."

echo "--- Making 'crawlrice' a global command..."

SCRIPT_PATH=$(realpath "Main/Cli_Crawlrice/crawlrice.py")
chmod +x "$SCRIPT_PATH"

if [ -f "/usr/local/bin/crawlrice" ]; then
    echo "  > Removing old link..."
    sudo rm /usr/local/bin/crawlrice
fi
sudo ln -s "$SCRIPT_PATH" /usr/local/bin/crawlrice
echo "✅ 'crawlrice' command created successfully."

echo ""
echo "--- ✨ Setup Complete! ---"
echo "You can now open a new terminal and run the 'crawlrice' command from any directory."
echo "Example: crawlrice --help"
echo "--------------------------"