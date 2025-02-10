#!/bin/bash

# Navigate to the project directory
cd "/home/ubuntu/Edu_ai/eduai/connectors/ADDA CONNECTOR" || exit

# Activate the virtual environment
source "/home/ubuntu/Edu_ai/eduai/connectors/ADDA CONNECTOR/adda/bin/activate"

# Run the Python script
python3 "/home/ubuntu/Edu_ai/eduai/connectors/ADDA CONNECTOR/adda_connector_current_affairs.py"

# Deactivate the virtual environment
deactivate
