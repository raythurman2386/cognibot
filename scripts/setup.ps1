$ExpectedDir = "cognibot"
$CurrentDir = Split-Path -Leaf (Get-Location)

if ($CurrentDir -ne $ExpectedDir) {
    Write-Host "Not in the $ExpectedDir directory. Changing directory..."
    Set-Location .\cognibot
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python could not be found. Please install Python and try again."
    exit
}

python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

if (Test-Path .\requirements.txt) {
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Please ensure it exists in the project directory."
    exit
}

Write-Host "Setup complete. Virtual environment created and dependencies installed."
Write-Host "To run the bot, activate the virtual environment using '.\venv\Scripts\Activate.ps1' and run 'python main.py'."
