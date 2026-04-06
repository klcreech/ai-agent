#!/bin/bash
# Architect AI: Environment Setup Script
# Robust GitHub-friendly setup

set -e  # Exit on any error

echo "-----------------------------------------"
echo "--- Starting Architect AI Setup Script ---"
echo "-----------------------------------------"

# 1️⃣ Check Python version
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found. Please install Python 3.10+."
    exit 1
fi

PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[INFO] Detected Python version: $PYTHON_VER"

# 2️⃣ Create virtual environment
if [ ! -d "venv" ]; then
    echo "[INFO] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[INFO] Virtual environment already exists. Skipping creation."
fi

# 3️⃣ Activate venv and install dependencies
source venv/bin/activate
echo "[INFO] Upgrading pip..."
pip install --upgrade pip

echo "[INFO] Installing required Python packages: requests, rich..."
pip install requests rich

# 4️⃣ Check Ollama installation
if command -v ollama &> /dev/null; then
    echo "[INFO] Ollama CLI detected."
    echo "[INFO] Pulling required model: qwen2.5-coder:7b..."
    ollama pull qwen2.5-coder:7b || echo "[WARN] Model pull failed. Ensure network access."
else
    echo "[WARN] Ollama CLI not found in PATH."
    echo "       Ensure Docker container or remote instance is running if needed."
fi

echo "-----------------------------------------"
echo "[✓] Setup complete!"
echo "To start Architect AI, run:"
echo "    source venv/bin/activate"
echo "    python main.py"
echo "-----------------------------------------"