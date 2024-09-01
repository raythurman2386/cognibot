# Check if Python is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Python3 could not be found. Please install Python3 and try again."
    exit
}

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the dependencies
if (Test-Path requirements.txt) {
    pip install -r .\requirements.txt
} else {
    Write-Host "requirements.txt not found. Please ensure it exists in the project directory."
    exit
}

# Inform the developer that the setup is complete
Write-Host "Setup complete. Virtual environment created and dependencies installed."

# Optional: Add a note about how to run the bot
Write-Host "To run the bot, activate the virtual environment using 'source venv\Scripts\Activate.ps1' and run 'python bot.py'."
