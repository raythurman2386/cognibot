#!/bin/bash

# Navigate to the bot directory
cd /cognibot

# Stash any local changes
git stash

# Pull the latest changes
git pull origin main

# Apply any stashed changes
git stash pop

# Restart the bot
sudo systemctl restart cognibot.service
