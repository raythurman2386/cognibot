#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Not in the $EXPECTED_DIR directory. Changing directory..."
    cd ./cognibot
fi

if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 and try again."
    exit
fi

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the project directory."
    exit
fi

echo "Setup complete. Virtual environment created and dependencies installed."
echo "To run the bot, activate the virtual environment using 'source venv/bin/activate' and run 'python main.py'."