# Setting Up Your Discord Bot for Local Development

This guide will walk you through the process of creating a Discord application, setting up a bot, and obtaining the necessary token for local development of Cognibot.

## Prerequisites

- A Discord account
- Access to the Discord Developer Portal
- A Personal Discord Server of your own to invite the new development bot

## Steps to Create a Discord Application and Bot

1. **Access the Discord Developer Portal**

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Log in with your Discord account if you haven't already

2. **Create a New Application**

   - Click on the "New Application" button
   - Give your application a name (e.g., "Cognibot-Dev")
   - Click "Create"

3. **Create a Bot User**

   - In your new application's dashboard, click on the "Bot" tab in the left sidebar
   - Click "Add Bot"
   - Confirm by clicking "Yes, do it!"

4. **Configure Bot Settings**

   - Set a username for your bot
   - Optionally, upload an avatar
   - Under "Privileged Gateway Intents", enable:
     - Presence Intent
     - Server Members Intent
     - Message Content Intent
   - Save your changes

5. **Get Your Bot Token**

   - In the "Bot" tab, find the "Token" section
   - Click "Reset Token" to generate a new token
   - Copy the token and keep it secure (you'll need this for your `.env` file)

6. **Set Up Bot Permissions**

   - Go to the "OAuth2" tab in the left sidebar
   - Scroll down to "Scopes" and select "bot"
   - In "Bot Permissions", select the permissions your bot needs (e.g., "Send Messages", "Read Message History", etc.)

7. **Invite the Bot to Your Server**
   - Still in the "OAuth2" tab, copy the generated OAuth2 URL
   - Open this URL in a new browser tab
   - Select a server to add your bot to (you need "Manage Server" permissions)
   - Authorize the bot

## Setting Up Your Local Environment

1. **Clone the Cognibot Repository**

   ```
   git clone https://github.com/raythurman2386/cognibot.git
   cd cognibot
   ```

2. **Create a `.env` File**

   - In the root directory of the project, create a file named `.env`
   - Add the following content, replacing `YOUR_DISCORD_TOKEN` with the token you copied earlier:
     ```
     DISCORD_TOKEN=YOUR_DISCORD_TOKEN
     OPENAI_API_KEY=your_openai_api_key
     ANTHROPIC_API_KEY=your_anthropic_api_key
     ```

3. **Install Dependencies**

   ```
   bash scripts/setup.sh
   ```

   - This will install the required dependencies for Cognibot including virtual environment creation.
   - After this script runs successfully you can activate the virtual environment by running `source venv/bin/activate`.

4. **Run the Bot**
   ```
   python main.py
   ```

Your bot should now be running and connected to your Discord server!

## Troubleshooting

- If you encounter a Discord error related to the token, double-check that you've correctly copied the token into your `.env` file.
- Make sure all required environment variables are set in your `.env` file.
- If you're having issues with permissions, review the bot permissions you set in the Discord Developer Portal.

## Next Steps

- Explore the `env.py` file to understand how environment variables are used in the project.
- Check out the other configuration options available in `env.py`, such as model selection for GPT and DALL-E.

Remember to never share your bot token or API keys publicly. Always keep them secure and use environment variables to manage sensitive information.
