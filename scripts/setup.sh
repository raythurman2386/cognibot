#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3 and try again."
    exit
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the project directory."
    exit
fi

# Inform the developer that the setup is complete
echo "Setup complete. Virtual environment created and dependencies installed."

# Optional: Add a note about how to run the bot
echo "To run the bot, activate the virtual environment using 'source venv/bin/activate' and run 'python main.py'."
