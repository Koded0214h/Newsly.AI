#!/bin/bash

# Activate virtual environment
source env310/bin/activate

# Change to the project directory
cd /Users/koded/Desktop/Code/Hackathon/Newsly.AI/backend

# Fetch latest articles
python manage.py fetch_articles

# Send daily digests
python manage.py send_digests --frequency daily

# Send weekly digests (only on Mondays)
if [ "$(date +%u)" = "1" ]; then
    python manage.py send_digests --frequency weekly
fi

# Deactivate virtual environment
deactivate 