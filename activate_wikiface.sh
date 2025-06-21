#!/bin/bash

# WikiFace Virtual Environment Activator
# This script activates the WikiFace virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the virtual environment activate script
VENV_ACTIVATE="$SCRIPT_DIR/WikiFace/bin/activate"

# Check if the activate script exists
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "Error: Virtual environment activate script not found at $VENV_ACTIVATE"
    echo "Please make sure the WikiFace virtual environment is properly set up."
    exit 1
fi

# Activate the virtual environment
echo "Activating WikiFace virtual environment..."
source "$VENV_ACTIVATE"

# Verify activation
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ WikiFace virtual environment activated successfully!"
    echo "Virtual environment: $VIRTUAL_ENV"
    echo "Python version: $(python --version)"
    echo ""
    echo "To deactivate, run: deactivate"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi 