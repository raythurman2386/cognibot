#!/bin/bash

# Activate the virtual environment
source /cognibot/venv/bin/activate

# Upgrade pip and install/update dependencies
pip install --upgrade pip
pip install -r /cognibot/requirements.txt
