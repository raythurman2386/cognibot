#!/bin/bash

# Check if the bot is running
if sudo systemctl is-active --quiet cognibot.service
then
    echo "Bot is running."
else
    echo "Bot is not running. Restarting..."
    sudo systemctl restart cognibot.service
fi
