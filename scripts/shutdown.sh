#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Not in the $EXPECTED_DIR directory. Changing directory..."
    cd ./cognibot
fi

if sudo systemctl is-active --quiet cognibot.service; then
    echo "Shutting Bot down..."
    sudo systemctl stop cognibot.service
else
    echo "Bot is not running. Run the setup or update script to run the bot."
fi
