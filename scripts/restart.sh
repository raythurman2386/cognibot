#!/bin/bash

if sudo systemctl is-active --quiet cognibot.service; then
    echo "Restarting Cognibot..."
    sudo systemctl restart cognibot.service
else
    echo "Bot is not running. Run the setup or update script to run the bot."
fi
