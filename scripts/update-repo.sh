#!/bin/bash

# Stash any local changes
git stash

# Pull the latest changes
git pull origin main

# Restart the bot
sudo systemctl restart cognibot.service
