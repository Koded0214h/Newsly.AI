# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # Changed from 587 to 465 for SSL
EMAIL_USE_SSL = True  # Changed from TLS to SSL
EMAIL_USE_TLS = False  # Disabled TLS since we're using SSL
EMAIL_HOST_USER = 'newslyai@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'  # Replace with your actual app password 