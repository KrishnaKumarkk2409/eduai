#!/bin/bash

# Navigate to the project directory
cd "/home/ubuntu/Edu_ai/eduai/connectors/GK Today Website Data Extraction as Connector" || exit

# Activate the virtual environment
source "/home/ubuntu/Edu_ai/eduai/connectors/GK Today Website Data Extraction as Connector/gktoday/bin/activate"

# Run the Python script
python3 "/home/ubuntu/Edu_ai/eduai/connectors/GK Today Website Data Extraction as Connector/gkTodayData.py"

# Deactivate the virtual environment
deactivate
