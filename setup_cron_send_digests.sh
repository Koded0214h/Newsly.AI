#!/bin/bash

# This script sets up a cron job to run the send_digests Django management command every hour.

# Path to python3 executable
PYTHON_PATH="/usr/bin/python3"

# Path to your Django manage.py
MANAGE_PY_PATH="/Users/koded/Desktop/Code/Newsly.AI/backend/manage.py"

# Log file for cron output
LOG_FILE="/Users/koded/cron_send_digests.log"

# Cron job line to add
CRON_JOB="0 * * * * $PYTHON_PATH $MANAGE_PY_PATH send_digests --frequency=daily >> $LOG_FILE 2>&1"

# Check if the cron job already exists
crontab -l | grep -F "$CRON_JOB" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists."
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully."
fi

# Show current cron jobs
echo "Current cron jobs:"
crontab -l
