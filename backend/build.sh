python manage.py collectstatic --noinput 
echo "0 * * * * python manage.py send_digests" >> /etc/crontab 