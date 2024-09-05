#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Not in the $EXPECTED_DIR directory. Changing directory..."
    cd ./cognibot
fi

git stash

git pull origin main

echo "Repo has been updated from GitHub, Cognibot will now update the environment and restart."

if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 and try again."
    exit
fi

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo -e "\n*** Setup complete. Virtual environment created and dependencies installed. ***\n"
else
    echo "requirements.txt not found. Please ensure it exists in the project directory."
    exit
fi

echo "The bot's service can be installed by running 'bash scripts/install_cognibot_service.sh'."
echo "If the service is installed, the bot will now be restarted. Otherwise, run the bot using 'python main.py'."

if sudo systemctl is-active --quiet cognibot.service; then
    echo "Restarting Cognibot..."
    sudo systemctl restart cognibot.service
else
    echo -e "\nBot service is not active, run the install script or run the bot with 'python main.py'.\n"
fi
