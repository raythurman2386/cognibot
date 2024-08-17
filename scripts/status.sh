#!/bin/bash

# Check if the bot is running
if ! pgrep -f "python3 /cognibot/main.py" > /dev/null
then
    echo "Bot is not running. Restarting..."
    sudo systemctl restart cognibot
else
    echo "Bot is running."
fi
