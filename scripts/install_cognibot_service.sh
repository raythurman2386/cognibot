#!/bin/bash

# install_cognibot_service.sh

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Define variables
SERVICE_NAME="cognibot"
SERVICE_DESCRIPTION="Cognibot Discord Bot"
WORKING_DIRECTORY="/home/<user>/cognibot" # Update <user> to your Pi's user
EXEC_START="/home/<user>/cognibot/venv/bin/python /home/<user>/cognibot/main.py"
USER="pi"  # or whatever user you want the service to run as

# Create service file
cat << EOF > /etc/systemd/system/${SERVICE_NAME}.service
[Unit]
Description=${SERVICE_DESCRIPTION}
After=network.target

[Service]
ExecStart=${EXEC_START}
WorkingDirectory=${WORKING_DIRECTORY}
StandardOutput=inherit
StandardError=inherit
Restart=always
User=${USER}

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize the new service
systemctl daemon-reload

# Enable and start the service
systemctl enable ${SERVICE_NAME}
systemctl start ${SERVICE_NAME}

echo "Cognibot service has been installed and started."
echo "You can check its status with: bash scripts/status.sh"
