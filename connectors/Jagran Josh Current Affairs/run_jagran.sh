#!/bin/bash

# Navigate to the project directory
cd "/home/ubuntu/Edu_ai/eduai/connectors/Jagran Josh Current Affairs" || exit

# Activate the virtual environment
source "/home/ubuntu/Edu_ai/eduai/connectors/Jagran Josh Current Affairs/jagranjosh/bin/activate"

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment activated."
else
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Run the Python script
python3 "/home/ubuntu/Edu_ai/eduai/connectors/Jagran Josh Current Affairs/Jagran Josh_connector_main script_Edu.Ai.py"

# Deactivate the virtual environment only if it's activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    deactivate
    echo "Virtual environment deactivated."
else
    echo "No virtual environment to deactivate."
fi
