# Installing Cognibot on a Raspberry Pi

This guide will walk you through the process of installing Cognibot on your Raspberry Pi and setting it up as a system service for automatic startup and crash recovery.

## Prerequisites

- A Raspberry Pi (3 or 4 recommended) with Raspberry Pi OS installed
- SSH access to your Raspberry Pi or direct access via keyboard and monitor
- Git installed on your Raspberry Pi
- Python 3.8+ installed on your Raspberry Pi

## Installation Steps

1. **Clone the Cognibot Repository**

   Open a terminal on your Raspberry Pi and run:

   ```
   git clone https://github.com/raythurman2386/cognibot.git
   cd cognibot
   ```

2. **Set Up a Project**

   I have included bash scripts to simplify the process of setup and installation. Run the following script to set up a new project:

   ```
   bash scripts/setup.sh
   ```

3. **Activate Virtual Environment**

   Activate the virtual environment:

   ```
   source venv/bin/activate
   ```

4. **Configure Cognibot**

   Copy the example environment file and edit it with your settings:

   ```
   cp .env.example .env
   nano .env
   ```

   Add your Discord token, API keys, and other necessary configuration.

5. **Test the Bot**

   Run the bot to ensure it works correctly:

   ```
   python main.py
   ```

   If everything is set up correctly, your bot should come online in Discord.

6. **Install as a System Service**

   To install Cognibot as a system service, use the provided installation script:

   ```
   sudo ./install_cognibot_service.sh
   ```

   This script will create a systemd service that starts Cognibot automatically and restarts it if it crashes.

7. **Verify the Service**

   Check if the service is running:

   ```
   bash scripts/status.sh
   ```

   You should see that the service is active and running.

## Updating Cognibot

To update Cognibot to the latest version:

1. Stop the service:

   ```
   bash scripts/shutdown.sh
   ```

2. Pull the latest changes:

   ```
   bash scripts/update-repo.sh
   ```

3. Check if the service is running:
   ```
   bash scripts/status.sh
   ```

## Uninstallation

If you need to uninstall Cognibot:

1. Run the uninstallation script:

   ```
   sudo ./uninstall_cognibot_service.sh
   ```

   This will stop and remove the system service.

2. Delete the Cognibot directory:
   ```
   cd ..
   rm -rf cognibot
   ```

## Troubleshooting

- If the bot doesn't come online, check the logs:

  ```
  sudo journalctl -u cognibot
  ```

- Ensure all required environment variables are set correctly in the `.env` file.

- If you encounter permission issues, make sure the user specified in the service file has the necessary permissions to run the bot and access its files.

## Additional Notes

- The installation script assumes you're using the `pi` user. If you're using a different user, edit the `USER` variable in the `install_cognibot_service.sh` script.

- Make sure your Raspberry Pi has a stable internet connection for the bot to function properly.

- Consider setting up a backup solution for your bot's data, especially if you're using a local database.

For any further issues or questions, please open an issue on the GitHub repository or seek help in our community Discord server.
