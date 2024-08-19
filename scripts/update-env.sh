#!/bin/bash

# Define the path to your virtual environment
VENV_DIR="/cognibot/venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Running setup script..."
    bash /cognibot/scripts/setup.sh
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and install/update dependencies
pip install --upgrade pip
pip install -r /cognibot/requirements.txt
