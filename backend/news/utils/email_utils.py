from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from news.models import Article, UserPreferences

def send_welcome_email(user):
    subject = 'Welcome to Newsly.AI!'
    html_message = render_to_string('emails/welcome_email.html', {
        'user': user,
        'site_url': settings.SITE_URL
    })
    
    send_mail(
        subject=subject,
        message='',  # Plain text version
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_news_digest():
    # Get all users with digest preferences
    users = UserPreferences.objects.filter(digest_enabled=True)
    
    for user_pref in users:
        # Get articles from the last 24 hours
        recent_articles = NewsArticle.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        ).order_by('-created_at')[:5]  # Get top 5 articles
        
        if recent_articles:
            subject = f'Your Newsly.AI Daily Digest - {timezone.now().strftime("%Y-%m-%d")}'
            html_message = render_to_string('emails/news_digest.html', {
                'user': user_pref.user,
                'articles': recent_articles,
                'site_url': settings.SITE_URL
            })
            
            send_mail(
                subject=subject,
                message='',  # Plain text version
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_pref.user.email],
                fail_silently=False,
            ) 