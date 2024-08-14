# CogniBot

Embark on a journey of intelligent conversations with CogniBot, a Discord companion powered by advanced chat GPT technology. Crafted with precision using the robust Pycord framework, CogniBot seamlessly integrates into your server, bringing a new level of interactive engagement.

## Getting Started

Follow the instructions below to set up your environment and install the necessary dependencies.

### Prerequisites

Ensure you have the following installed on your system:

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **git**: Version control system

### Cloning the Repository

```bash
git clone https://github.com/raythurman2386/cognibot.git
cd CogniBot
```

### Setting Up the Virtual Environment

Setting up a virtual environment helps in managing dependencies and isolating them from your global Python installation.

#### Windows (PowerShell)

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

#### Windows (WSL)

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   ```bash
   source venv/bin/activate
   ```

#### Linux and Mac

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   ```bash
   source venv/bin/activate
   ```

### Installing Dependencies

Once your virtual environment is activated, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### Deactivating the Virtual Environment

To deactivate the virtual environment, simply run:

```bash
deactivate
```

## Commands

### Greetings Commands

- `/hello`: Simply says hello to test the bot.

### OpenAI Commands

- `/chatgpt`: Send a prompt to chat gpt for a private dismissable response.
- `/dalle`: Send a prompt to chat gpt to generate a dall e 3 ai image. The response is a discord embed and the image will only be valid for 1 hour. If you fail to download your image in the proper amount of time, all images are hosted at [Ravenwood AI Gallery](https://ravenwood-gallery.vercel.app)

### Anthropic Commands

- `/claude`: Send a prompt to Anthropics Claude for a private dismissable response, conversational bot.

### Moderator Commands

- `/auth`: A moderator may add a user to the authorized user table for ChatGPT commands.
- `/addmod`: A moderator may add a user as a new moderator for the server.
- `/backup`: A moderator may backup the chat log.

---

### Tips

- Make sure you are in the right directory (`CogniBot`) before creating and activating the virtual environment.
- Remember to activate your virtual environment each time you open a new terminal session and want to run the bot or make changes to it.
- If you run into permission issues on Windows when activating the virtual environment, refer to the provided solution for changing the execution policy.
- Keep your dependencies up to date by running `pip install -r requirements.txt` after any updates.

### Additional Resources

- [Pycord Documentation](https://docs.pycord.dev/)
- [Discord API Documentation](https://discord.com/developers/docs/intro)