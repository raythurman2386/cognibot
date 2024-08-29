#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    cd ./cognibot
fi

if sudo systemctl is-active --quiet cognibot.service; then
    echo "Bot is running."
else
    echo "Bot is not running. Restarting..."
    sudo systemctl restart cognibot.service
fi
