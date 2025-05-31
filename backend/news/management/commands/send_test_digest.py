from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.views import send_news_digest_email  # Adjust path if needed

User = get_user_model()

class Command(BaseCommand):
    help = 'Send a test news digest email to the first registered user.'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found.'))
            return

        articles = [
            {
                'title': 'Breaking: AI Revolution',
                'summary': 'Here’s how AI is taking over the world (and journalism).',
                'url': 'https://example.com/ai-news',
                'source': 'The AI Times'
            },
            {
                'title': 'Climate Watch',
                'summary': '2025 shows rising trends in global temperatures.',
                'url': 'https://example.com/climate',
                'source': 'EcoGlobal'
            }
        ]

        send_news_digest_email(user, articles)
        self.stdout.write(self.style.SUCCESS(f'Digest sent to {user.email}'))
