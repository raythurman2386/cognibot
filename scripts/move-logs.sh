#!/bin/bash

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