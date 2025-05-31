# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # Revert to 465 for SSL
EMAIL_USE_SSL = True  # Enable SSL
EMAIL_USE_TLS = False  # Disable TLS
EMAIL_HOST_USER = 'coder0214h@gmail.com'
EMAIL_HOST_PASSWORD = 'onuopumpcgbwolbo'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER 