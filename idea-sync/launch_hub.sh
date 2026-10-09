#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/hub"

# Setup Venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment for AI Hub..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "Launching AI Grid Smartphone Hub on port 8888..."
./venv/bin/python3 hub.py
