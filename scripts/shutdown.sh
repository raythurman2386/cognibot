#!/bin/bash

# Check if the bot is running
if sudo systemctl is-active --quiet cognibot.service
then
    echo "Shutting Bot down..."
    sudo systemctl stop cognibot.service
else
    echo "Bot is not running. Run the setup or update script to run the bot."
fi
