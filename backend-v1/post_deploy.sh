#!/bin/bash

# Run migrations
python manage.py migrate

# Create categories
python manage.py create_categories

# Fetch initial articles
python manage.py fetch_articles

echo "Post-deployment tasks completed successfully!" 