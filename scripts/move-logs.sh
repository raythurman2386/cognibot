#!/bin/bash

EXPECTED_DIR="cognibot"
CURRENT_DIR=${PWD##*/}

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Not in the $EXPECTED_DIR directory. Changing directory..."
    cd ./cognibot
fi

LOG_DIR="Logs"
LOG_FILES=(*.log)

if [ ! -d "$LOG_DIR" ]; then
    mkdir "$LOG_DIR"
fi

for file in "${LOG_FILES[@]}"; do
  if [ -f "$file" ]; then
    mv "$file" "$LOG_DIR/"
  fi
done
