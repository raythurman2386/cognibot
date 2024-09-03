# CogniBot

**Embark on a journey of intelligent conversations with CogniBot, a Discord companion powered by advanced GPT technology.** Crafted with precision using the robust Pycord framework, CogniBot seamlessly integrates into your server, bringing a new level of interactive engagement.

## Getting Started

Follow the instructions below to set up your environment, install the necessary dependencies, and prepare for development.

### Prerequisites

Ensure you have the following installed on your system:

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **git**: Version control system

### Cloning the Repository

Clone the repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/raythurman2386/cognibot.git
cd CogniBot
```

### Setting Up the Virtual Environment

Setting up a virtual environment helps in managing dependencies and isolating them from your global Python installation.

#### Automatic Setup (Recommended)

To simplify the setup process for new developers, use the provided `setup.sh` script in the `scripts` directory:

```bash
bash scripts/setup.sh
```

This script will:

1. Check if Python is installed.
2. Create and activate a virtual environment.
3. Upgrade `pip` and install all required dependencies.

#### Manual Setup

If you prefer to set up the environment manually, follow the steps below:

##### Windows (PowerShell)

1. **Create a virtual environment**:

   ```powershell
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Note**: If you encounter a security warning, you might need to change the execution policy temporarily:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

##### Windows (WSL)

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   ```bash
   source venv/bin/activate
   ```

##### Linux and Mac

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   ```bash
   source venv/bin/activate
   ```

### Installing Dependencies

Once your virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Deactivating the Virtual Environment

To deactivate the virtual environment, simply run:

```bash
deactivate
```

### Updating the Repository and Restarting the Bot

To update the repository with the latest changes and restart the bot, use the provided `update.sh` script in the `/scripts/` directory:

```bash
bash scripts/update.sh
```

This script will:

1. Stash any local changes.
2. Pull the latest changes from the remote repository.
3. Apply stashed changes.
4. Restart the bot.

## Commands

### Greetings Commands

- `/hello`: Simply says hello to test the bot.

### OpenAI Commands

- `/chatgpt`: Send a prompt to ChatGPT for a private dismissable response.
- `/dalle`: Send a prompt to ChatGPT to generate a DALL·E 3 AI image. The response is a Discord embed, and the image will only be valid for 1 hour. If you fail to download your image in time, all images are hosted at [Ravenwood AI Gallery](https://ravenwood-gallery.vercel.app).

### Anthropic Commands

- `/claude`: Send a prompt to Anthropics Claude for a private dismissable response, a conversational bot.

### Moderator Commands

- `/auth`: A moderator may add a user to the authorized user table for ChatGPT commands.
- `/addmod`: A moderator may add a user as a new moderator for the server.
- `/backup`: A moderator may backup the chat log.

---
### Contributing

We welcome contributions to CogniBot! Here are the steps to contribute:

- Join our Discord server: [CogniBot Discord](https://discord.gg/MxNVnrxJJw)
- Fork the repository and create your branch from main.
- Make your changes and ensure the code follows the project's style.
- Test your changes thoroughly.
- Create a pull request with a clear description of your changes.

*For any ideas, bugs, or discussion items, please create an issue in the GitHub repository.*

---
### Tips

- Always ensure you are in the correct directory (`CogniBot`) before creating and activating the virtual environment.
- Remember to activate your virtual environment each time you open a new terminal session to run the bot or make changes to it.
- Keep your dependencies up to date by running `pip install -r requirements.txt` after any updates.
- Use the provided scripts to simplify updates, backups, and environment setup.

### Additional Resources

- [Pycord Documentation](https://docs.pycord.dev/)
- [Discord API Documentation](https://discord.com/developers/docs/intro)
