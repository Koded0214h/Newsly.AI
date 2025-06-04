from django.core.management.base import BaseCommand
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from news.models import CustomUser, Article, UserPreference
from datetime import timedelta
import logging
import datetime
from news.utils.email_utils import send_news_digest

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends news digests to users based on their preferences'

    def handle(self, *args, **options):
        current_time = timezone.now().time()
        # Get users who want digest at current hour
        users_to_notify = UserPreference.objects.filter(
            digest_enabled=True,
            digest_time__hour=current_time.hour
        )
        
        if users_to_notify.exists():
            send_news_digest()
            self.stdout.write(self.style.SUCCESS('Successfully sent news digests'))

    def add_arguments(self, parser):
        parser.add_argument(
            '--frequency',
            type=str,
            choices=['daily', 'weekly'],
            help='Send digests for users with this frequency preference'
        )

    def handle(self, *args, **options):
        frequency = options.get('frequency')
        if not frequency:
            self.stdout.write(self.style.ERROR('Please specify frequency (daily/weekly)'))
            return

        # Get users with the specified frequency preference and is_subscribed=True
        users = CustomUser.objects.filter(
            frequency=frequency,
            is_subscribed=True
        ).distinct()

        self.stdout.write(f"Found {users.count()} users with {frequency} frequency")

        for user in users:
            try:
                # Calculate time range based on frequency
                if frequency == 'daily':
                    start_date = timezone.now() - timedelta(days=1)
                else:  # weekly
                    start_date = timezone.now() - timedelta(days=7)

                # Get articles based on user's interests
                articles = Article.objects.filter(
                    created_at__gte=start_date,
                    category__name__in=user.interests.values_list('name', flat=True)
                ).order_by('-created_at')[:5]  # Get top 5 articles

                if not articles:
                    self.stdout.write(f"No new articles for {user.email}")
                    continue

                # Create email content
                subject = f"Your {frequency.capitalize()} News Digest"

                # Render HTML content
                html_content = render_to_string('newsDigest.html', {
                    'user': user,
                    'articles': articles,
                    'frontend_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'),
                    'current_year': datetime.datetime.now().year,
                })

                # Create SMTP connection with timeout
                self.stdout.write(f"Connecting to SMTP server {settings.EMAIL_HOST}:{settings.EMAIL_PORT} using SSL")
                connection = get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=False,  # Disable TLS
                    use_ssl=True,   # Enable SSL
                    timeout=30      # 30 second timeout
                )

                # Create email message with HTML content
                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body='Your news digest is ready. Please view it in an HTML compatible email client.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                    connection=connection,
                )
                email_message.attach_alternative(html_content, "text/html")

                # Send email using the connection
                try:
                    self.stdout.write(f"Sending email to {user.email}")
                    email_message.send()
                    self.stdout.write(self.style.SUCCESS(f"Email sent successfully to {user.email}"))

                    # Update last digest sent timestamp
                    user.last_digest_sent = timezone.now()
                    user.save()

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to send email to {user.email}: {str(e)}"))
                    logger.error(f"Failed to send email to {user.email}: {str(e)}")
                finally:
                    connection.close()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing user {user.email}: {str(e)}"))
                logger.error(f"Error processing user {user.email}: {str(e)}")

        self.stdout.write(self.style.SUCCESS('Finished sending digests'))
