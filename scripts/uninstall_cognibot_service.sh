#!/bin/bash

# uninstall_cognibot_service.sh

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Define variables
SERVICE_NAME="cognibot"

# Stop and disable the service
systemctl stop ${SERVICE_NAME}
systemctl disable ${SERVICE_NAME}

# Remove the service file
rm /etc/systemd/system/${SERVICE_NAME}.service

# Reload systemd to recognize the changes
systemctl daemon-reload

echo "Cognibot service has been uninstalled."
